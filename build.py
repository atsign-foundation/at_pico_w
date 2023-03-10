import os
import shutil
import subprocess
import sys
import shutil
import time

def runCross(src, dst, fname) -> (bool, str):
    print("mpy-cross : "+fname)
    sp = subprocess.run(["mpy-cross", "-o", dst, "-s", fname, src, "-march=armv6m"], capture_output=True, text=True)
    return (sp.returncode==0, sp.stdout)

def isNewer(f1, f2):
    if os.path.exists(f2):
        return (os.path.getmtime(f1) > os.path.getmtime(f2))
    return True

def parseArgs(aa, minArgs:int) -> dict:
    ret = {}
    ai = 0
    curarg = None
    for a in aa:
        if a.startswith('-'):
            if curarg is not None:
                ret[curarg] = True
            curarg = a
        else:
            if curarg is not None:
                ret[curarg] = a
                curarg=None
            else:
                ai+=1
                ret[str(ai)] = a
    if curarg is not None:
        ret[curarg] = True
    if ai < minArgs:
        raise Exception("Require at least "+minArgs+" arguments")
    return ret

def getEnvOrDef(vn, d) -> str:
    return os.environ.get(vn, d)

def make_build_version(srcd) -> None:
    vd = "major = '{}'\nminor='{}'\nbuild='{}'\ndate='{}'\n".format(
        getEnvOrDef('RELEASE_MAJOR', "0"),
        getEnvOrDef('RELEASE_MINOR', "0"),
        getEnvOrDef('CI_COMMIT_SHORT_SHA', getEnvOrDef('USER', getEnvOrDef('USERNAME', 'anon')+'@'+time.strftime("%y-%m-%d %H:%M", time.localtime()))),
        getEnvOrDef('CI_JOB_STARTED_AT', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    )
    with open(srcd+"/version.py", "w") as fh:
        fh.write(vd)
    print("Wrote version info: {}".format(vd))

def dobuild(srcd, dstd, faillogf, clean) -> bool:
    if clean:
        if os.path.exists(dstd):
            shutil.rmtree(dstd)

    if os.path.exists(dstd) is False:
        os.mkdir(dstd)

    # put build dates etc into version.py before builing
    make_build_version(srcd)

    failedPy = []
    for root, dirs, files in os.walk(srcd):
        ddir = dstd+root[len(srcd):]
        #    ddir = os.path.join(dstd, root[len(srcd):])
        for d in dirs:
            pd = os.path.join(ddir, d)
            if os.path.exists(pd) is False:
                print("mkdir "+pd)
                os.mkdir(pd)
        for f in files:
            inf = os.path.join(root,f)
            # if a python file, cross-compile UNLESS its boot.py/main.py as these MUST be straight python files for pycom boot process
            if f.endswith('.py') and f!="main.py" and f!="boot.py":
                outf = os.path.join(ddir,f[:-3]+".mpy")
                if isNewer(inf, outf):
                    print("mpy-cross -o "+outf+" "+inf)
                    res, out = runCross(inf, outf, f)
                    if not res:
                        print(inf+" failed python cross compilier.")
                        failedPy.append(inf)
                        failedPy.append(out)
                else:
                    print(inf+" unchanged")
            else:
                outf = os.path.join(ddir,f)
                if isNewer(inf, outf):
                    print("cp "+inf+" "+outf)
                    shutil.copyfile(inf, outf)
                else:
                    print(inf+" unchanged")

    if len(failedPy)==0:
        print("Project built successfully")
        return True
    else:
        print("Project has {} python cross-compile failures:".format(len(failedPy)))
        if faillogf is not None:
            with open(faillogf, "w") as fh:
                for f in failedPy:
                    fh.write("{}\n".format(f))
            print("Fix and rebuild...logs in {}".format(faillogf))
        else:
            for f in failedPy:
                print(f)
            print("Fix and rebuild...")
        return False

if __name__ == '__main__':
    # start script
    argd = parseArgs(sys.argv, 0)
    SRC=argd.get("-s", "src")
    DST=argd.get("-d", "built")
    OUTF = argd.get("-o", None)

    # check if clean run required
    CLEAN = argd.get("-clean", False)!=False

    if dobuild(SRC, DST, OUTF, CLEAN):
        sys.exit(0)
    else:
        sys.exit(1)
