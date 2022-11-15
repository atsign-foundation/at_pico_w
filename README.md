<img width=250px src="https://atsign.dev/assets/img/atPlatform_logo_gray.svg?sanitize=true">


# at_pico_w

For UMass 2022 IoT Projects.

# Table of Contents

- [Prerequisites](#prerequisites)
- [Instructions](#instructions)
  * [Forking the Project](#forking-the-project)
  * [Setting up Micropython on your Pico W](#setting-up-micropython-on-your-pico-w)
  * [Getting Started - Blinking the LED](#getting-started---blinking-the-led)
  * [Connecting to the atPlatform](#connecting-to-the-atplatform)
  * [Libraries](#libraries)

# Prerequisites

- [VSCode](https://code.visualstudio.com/Download) with the [Pico-W-Go extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)
- [Git](https://git-scm.com/) and your own [GitHub](https://github.com) account
- A [Raspberry Pi Pico W](https://www.canakit.com/raspberry-pi-pico-w.html) and [a data micro-USB to USB-A cable](https://m.media-amazon.com/images/I/61kT7kpt2hL._AC_SY450_.jpg) (to connect your Pico to your Computer)
- [FileZilla](https://filezilla-project.org/) or any other FTP software.
- Two [atSigns](https://my.atsign.com/go) and their [.atKeys files](https://www.youtube.com/watch?v=2Uy-sLQdQcA&ab_channel=Atsign)

# Instructions

## 0. Introduction

Hi UMass students! I've wrote some code for you to get your Pico Ws setup with the atPlatform. Big shoutout to @realvarx on GitHub for developing AES CTR and RSA-2048 private key signing on the Pico W. 

Let me know if you have any questions on Discord (Jeremy#7970) or by email (jeremy.tubongbanua@atsign.com) or just on our [discord](https://discord.atsign.com).

Be sure to get the first 3 prerequisites under [Prerequisites](#prerequisites) before you start. The last 2 prerequisites (FTP software and 2 atSigns) can be done later.

## 1. Getting the right Micropython Firmware for your Pico W

1. Go to [atsign-foundation/micropython/releases](https://github.com/atsign-foundation/micropython/releases) and download the `.uf2` file. This `.uf2` file is specially built firmware to allow a certain encryption that Atsign uses (AES-256 CTR mode) to work on the Pico W. Big shoutout to @realvarx for developing all the Atsign encryption for the Pico W. 

2. Unplug your Pico W from your computer. Hold down the BOOTSEL button on the Pico W and then plug back the Pico W into your computer (all while holding down the BOOTSEL button). Once the Pico W is plugged in, you can let go of the BOOTSEL button. Your Pico W should now be in bootloader mode. 

You should see the Pico on your computer as a USB drive (see image below).

<img src="https://i.imgur.com/msoBukM.png" />

3. Drag and drop the `firmware.uf2` file into the Pico W. This will flash the Pico W with the new firmware. Now the Pico W should automatically restart so no need to unplug/replug it.

## 2. Getting Started - Blinking the LED

Now let's create our first project.

1. Open VSCode and create and open an empty folder where your project will be.

2. Get the [Pico-W-Go extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)

3. Create a file named `blink.py` and write the following code:

```py
# blink.py

import machine
import time

led = machine.Pin("LED", machine.Pin.OUT) # "LED" is the on board LED

# blink ten times
for i in range(10):
    print('Blinking... %s' %str(i+1))
    led.toggle()
    time.sleep(0.5)
```

Note: You could also name this file- `main.py`. However, `main.py` is the default file that the Pico W will run when it starts up. But with the [Pico-W-Go extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go), you can choose *when* to run a file (regardless of name) which is how we will be running our files from here on out. I recommend not having a `main.py` at all since it tends to bug out the Pico W trying to run your experimental code as soon as it boots which can get annoying.


4. Open the command pallette via `Ctrl + Shift + P` (or `Cmd + Shift + P` if you are on a Mac) and type `Configure Project` and press Enter. The extension should setup your current folder as a Pico W project by initializing a `.vscode/` hidden folder and a `.picowgo` hidden file. Now, any Pico-W-Go commands should work. You can also access Pico-W-Go commands by clicking on "All Commands" at the bottom of VSCode.

VSCode bottom toolbar with Pico-W-Go commands:

<img width=500px src="https://i.ibb.co/g3jm53c/image.png">

6. Now try connecting to your Pico W and see if it works. You can do this by clicking on the "Connect" button.

7. Make sure you have your `blink.py` python file open in the editor and Run the "Run current file" command. You should see the onboard LED blink 10 times.

## 3. Forking the Project

Now we know your Pico W is working swell, let's get into some atPlatform.

First, let's create a fork of this repository branch on your own GitHub account. This gives you a copy of the code that you can edit on your own system.

1. Fork this repository by clicking "Fork" on our [at_pico_w](https://github.com/atsign-foundation/at_pico_w/tree/umass2022) repository.
2. Create the fork by pressing "Create fork" and untick the box that says "Include all branches". This will fork all the branches, specifically the `umass2022` branch.
3. Open VSCode and open an empty folder where you will be creating a new project.
4. Git clone your fork via `git clone <https://github.com/<YOUR_GITHUB_NAME>/at_pico_w.git> .` (clone your fork into the folder you've created)
5. `git checkout -b umass2022` (create a new branch called umass2022 and go into it)
6. `git remote add upstream https://github.com/atsign-foundation/at_pico_w.git` (add the original repository as a remote called upstream)
7. `git fetch upstream` (update with latest upstream)
8. `git reset --hard upstream/umass2022` (reset the branch to the origin)

Now you should have all of the code in your folder. This is the fork you created on your GitHub account. Your folder should look something like this:

<img width=250px src="https://i.imgur.com/CC7bEFI.png">

## 4. Connecting to WiFi

1. Edit the `settings.json` by adding your WiFi and Password, leave the atSign blank for now.

settings.json

```json
{
	"ssid": "********",
	"password": "&&&&",
	"atSign": ""
}
```


2. You should see a file called `test_1_wifi.py` in your project (since you forked the repository). Open this file in VSCode and run the Pico-W-Go command "Run this current file".

3. The code is:
```py
def main():
    from lib.at_client import io_util
    from lib import wifi

    # Add your SSID an Password in `settings.json`
    ssid, password, atSign = io_util.read_settings()
    del atSign # atSign not needed in memory right now

    print('\nConnecting to %s (Ctrl+C to stop)...' % ssid)
    wlan = wifi.init_wlan(ssid, password)

    if not wlan == None:
        print('Connected to WiFi %s: %s' %(ssid, str(wlan.isconnected())))
    else:
        print('Failed to connect to \'%s\'... :(' %ssid)

if __name__ == '__main__':
    main()
```

4. Your output should be similar to:

```
Connecting to Soup (Ctrl+C to stop)...
Connected to WiFi Soup: True
```

## 5. Connecting to your device atSign's atServer.

1. If you do not have all of the prerequisites, it is time to get them, especially: [FileZilla](https://filezilla-project.org/) or any other FTP software and two [atSigns](https://my.atsign.com/go) and their [.atKeys files](https://www.youtube.com/watch?v=2Uy-sLQdQcA&ab_channel=Atsign). Continue reading to find out how to get your .atKeys files.

2. Add the atSign you wish your device's atSign to be in the `settings.json`. This is an atSign you own and got from [my.atsign.com/go](https://my.atsign.com/go).

settings.json

```
{
	"ssid": "******",
	"password": "***",
	"atSign": "@alice"
}

```

3. To get an .atKeys file belonging to an atSign, go to 0:54 of this [video](https://youtu.be/2Uy-sLQdQcA?t=54). The easiest way is to download [atmospherePro](https://atsign.com/apps/atmospherepro/) on your computer (via Microsoft Store on Windows or the Appstore if you're on Mac) and onboarding your atSign via the onboarding widget in the app. There are other ways to generate the encryption .atKeys file for an atSign (such as the [at_onboarding_cli on Dart](), [RegisterCLI on Java](), the [sshnp_register_tool in at_tools](), [OnboardingCLI in Java]()) but generating it through [atmospherePro](https://atsign.com/apps/atmospherepro/) is the easiest if you don't want to deal with any code. If you have an .atKeys file (like '@bob232.atKeys'), then move onto the next step. We are going to put our atKeys on the Pico W.

4. Run the "Start FTP server" command to start the FTP server on your Pico W Go. You should be given an address in the terminal (similar to the image below):

<img width=500px src="https://i.ibb.co/89mpzBh/image.png">

5. Open [FileZilla](https://filezilla-project.org/) and connect to this address. If it asks for a password, the password should be `pico`. If you've uploaded and files to the Pico before, you should see them once you've connected. Similar to below:

<image src="https://i.imgur.com/UaLQVdu.png" />

6. Create a `keys/` directory. This is where you will drag and drop the .atKeys file. Your `/keys/` directory should look like this:

<image src="https://i.imgur.com/wl2rIk8.png" />

7. Close the FTP server by pressing "Stop" on the bottom toolbar on VSCode.

Stop button:

<image src="https://i.imgur.com/RcxeSV5.png" />

Yay our FTP server is closed:

<image src="https://i.imgur.com/3FJg4Lc.png" />

7. Now let's initialize our keys in the Pico W by running `test_3_initializing_keys.py`. This decrypts the encryption keys and converts them to their n, e, p, d, q parameters which can be understood by the RSA library.

8. Now we can test PKAM authenticating by running `test_4_pkam_authenticate.py`.  PKAM authenticating is essentially authenticating ourselves to the server so we can run commands like updating, deleting, and seeing values.

Output should be similar to:

<image src="https://i.imgur.com/01zt1BN.png">

If you don't see this, ensure your settings.json looks like this (with an atSign you own):

```json
{
	"ssid": "****",
	"password": "****",
	"atSign": "@fascinatingsnow"
}
```

and that you have the .atKeys file in the `/keys/` directory.

<image src="https://i.imgur.com/wl2rIk8.png" />

## 6. Sending end-to-end encrypted data