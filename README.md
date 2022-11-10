<img width=250px src="https://atsign.dev/assets/img/atPlatform_logo_gray.svg?sanitize=true">


# at_pico_w for UMass 2022 IoT projects

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
- Two [atSigns](https://my.atsign.com/go) and their [.atKeys files](https://www.youtube.com/watch?v=2Uy-sLQdQcA&ab_channel=Atsign)
- [FileZilla](https://filezilla-project.org/) or any other FTP software.
- A [Raspberry Pi Pico W](https://www.canakit.com/raspberry-pi-pico-w.html) and [a micro-USB to USB-A cable](https://m.media-amazon.com/images/I/61kT7kpt2hL._AC_SY450_.jpg) (to connect your Pico to your Computer)

# Instructions

Hi UMass students! I've wrote some code for you to get your Pico Ws setup with the atPlatform. Big shoutout to @realvarx for developing AES CTR and RSA-2048 private key signing on the Pico W. Let me know if you have any questions on Discord (Jeremy#7970) or by email (jeremy.tubongbanua@atsign.com) or just on our [discord](https://discord.atsign.com)

## Forking the Project

First, let's create a fork of this repository branch on your own GitHub account. This gives you a copy of the code that you can edit on your own system.

1. Fork this repository by clicking "Fork"
2. Go into your terminal where you like to keep your code projects and do the following:
- `mkdir at_pico_w` (make an at_pico_w folder) 
- `cd at_pico_w` (change directories) 
- `git clone <https://github.com/<YOUR_GITHUB_NAME>/at_pico_w.git> .` (clone your fork into the folder you've created)

Now you should have all of the code in your folder. Your folder should look something like this:

<img width=250px src="https://i.imgur.com/CC7bEFI.png">

## Setting up Micropython on your Pico W

1. In the folder, you will get a copy of the `rp2-pico-w-20221108-aes-ctr-enabled.uf2`. This .uf2 file is specially built firmware to allow special encryption that Atsign uses (AES CTR and RSA-2048) to work on the Pico W. Big shoutout to @realvarx for developing all the Atsign encryption for the Pico W. 

2. Unplug your Pico W from your computer. Hold down the BOOTSEL button on the Pico W and then plug back the Pico W into your computer (all while holding down the BOOTSEL button). Once the Pico W is plugged in, you can let go of the BOOTSEL button. Your Pico W should now be in bootloader mode. 

You should see the Pico on your computer as a USB drive (see image below).

<img src="https://i.imgur.com/msoBukM.png" />

3. Drag and drop the `rp2-pico-w-20221108-aes-ctr-enabled.uf2` file into the Pico W. This will flash the Pico W with the new firmware. Now the Pico W should automatically restart so no need to unplug/replug it.

## Getting Started - Blinking the LED

1. Open the `at_pico_w` folder on VSCode. 

2. Get the [Pico-W-Go extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go)

3. Create a file named `blink.py` and copy and paste the following code into it:

```py
# blink.py
import machine
import time

led = machine.Pin("LED", machine.Pin.OUT)

for i in range(10):
    print('Blinking... %s' %str(i+1))
    led.toggle()
    time.sleep(0.5)
```


4. Open the command pallette via `Ctrl + Shift + P` (or `Cmd + Shift + P` if you are on a Mac) and type `Configure Project` and press Enter. The extension should setup your current folder as a Pico W project. Now, any Pico-W-Go commands should work. You can also access Pico-W-Go commands by clicking on "All Commands" at the bottom of VSCode.

VSCode bottom toolbar with Pico-W-Go commands:

<img width=500px src="https://i.ibb.co/g3jm53c/image.png">

6. Now try connecting to your Pico W and see if it works. You can do this by clicking on the "Connect" button.

7. Make sure you have your `blink.py` python file open in the editor and Run the "Run current file" command. You should see the onboard LED blink 10 times.

## Connecting to the atPlatform

1. You will notice there's a `main2.py` file in your project. Running this file via the "Run current file" command will connect your Pico W to the atPlatform. But there is some setup that needs to be done first:

2. Edit `settings.json` by inputting your WiFi ssid, WiFi password, and the device atSign that you own and have the .atKeys to. To get an .atKeys file, go to 0:54 of this [video](https://youtu.be/2Uy-sLQdQcA?t=54). The easiest way is to download [atmospherePro](https://atsign.com/apps/atmospherepro/) on your computer (via Microsoft Store on Windows or the Appstore if you're on Mac) and onboarding your atSign via the onboarding widget in the app. There are other ways to generate the encryption .atKeys file for an atSign (such as the [at_onboarding_cli on Dart](), [RegisterCLI on Java](), the [sshnp_register_tool in at_tools](), [OnboardingCLI in Java]()) but generating it through atmospherePro is the easiest if you don't want to deal with any code.

3. Run the "Start FTP server" command. You should be given an address in the terminal (similar to the image below):

<img width=500px src="https://i.ibb.co/89mpzBh/image.png">

4. Open [FileZilla](https://filezilla-project.org/) and connect to this address. If it asks for a password, the password should be `pico`. If you've uploaded and files to the Pico before, you should see them once you've connected. Similar to below:

<image src="https://i.imgur.com/UaLQVdu.png" />

5. Create a `keys/` directory. This is where you will drag and drop the .atKeys file. Your `/keys/` directory should look like this:

<image src="https://i.imgur.com/wl2rIk8.png" />

6. Close the FTP server by pressing "Stop" on the bottom toolbar on VSCode.

Stop button:

<image src="https://i.imgur.com/RcxeSV5.png" />

Yay our FTP server is closed:

<image src="https://i.imgur.com/3FJg4Lc.png" />

7. Now we have to put our keys in the Pico W, it's time to run `main2.py`. First upload all dependencies and files by running the command "Upload project". This will upload all the files in your project to the Pico W. You may run into some freezing and errors, but just keep trying by disconnecting/reconnecting and unplugging/replugging the Pico W.

8. Now open `main2.py` and run the "Run current file" command. You should see something similar to this: If your code has 1. connected to the Internet and 2. found the address of your secondary server, then move onto the next step!

<image src="https://i.imgur.com/njQ8D4s.png">

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

9. This is the tricky part. Now we are going to write some atProtocol. Go into `main2.py` and this part of the code:

<image src="https://i.imgur.com/iaXhE7T.png" />

10. Depending on what you are doing, you will need to comment A) and edit B) or vice versa. If you are trying to receive data from another atSign's secondary, you will use code under A), and if you are sending data to another atSign's secondary, you will use code under B). 

## Libraries
- [iot-core-micropython](https://github.com/GoogleCloudPlatform/iot-core-micropython)
- [uasn1](https://github.com/mkomon/uasn1)
