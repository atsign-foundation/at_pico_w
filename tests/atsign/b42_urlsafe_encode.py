import os
import sys
TEST_PATH = os.getcwd()
sys.path.append(TEST_PATH+'/../../src')
sys.path.append(TEST_PATH+'/../../src/lib')
import atclient

print(atclient.b42_urlsafe_encode("abc"))
print(atclient.b42_urlsafe_encode("1"))
print(atclient.b42_urlsafe_encode("The quick brown fox jumps over the lazy dog!"))
print(atclient.b42_urlsafe_encode("These characters are {, }, |, \, ^, ~, [, ], and `."))
print(atclient.b42_urlsafe_encode('The characters ";", "/", "?", ":", "@", "=" and "&" are the characters which may be reserved for special meaning within a scheme.'))
