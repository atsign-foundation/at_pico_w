<img width=250px src="https://atsign.dev/assets/img/atPlatform_logo_gray.svg?sanitize=true">

# at_pico_w
Communicate with the atPlatform using a Raspberry Pi Pico W.

Developed with [MicroPython](https://micropython.org/).

## Usage
- Install the latest `firmware.uf2` onto your Pico W from [atsign-foundation/micropython Releases](https://github.com/atsign-foundation/micropython/releases), as this is patched to enable AES CTR, which is used by atSigns.
- Fill all the fields of the `settings.json` file (ssid/passw of your Wi-Fi network and atSign). 
- Download [Thonny IDE](https://thonny.org/) and place all the files of this repository in the Pico W file system.
- Place your `.atKeys` file in the `~/keys/` directory (if the folder doesn't exist, create it manually)
- Run `main.py` and select option `3` in the REPL ("Get privateKey for @[yourAtSign]")
- Re-launch the REPL (run `main.py` again)
- Now you can select option `2` in the REPL to automatically get authenticated in your DESS
- Enjoy!  :)

(If you get an error when attempting to find the secondary or when trying to connect to it, run again the REPL)

(You can uncomment a few commented lines in the `send_verb` method to see the llookup verb answer content decrypted. Warning: some stored keys are not encrypted, if you try to see the decrypted content of one of those stored keys, you will get an error. This exception will be handled in the future)

## Libraries
- [iot-core-micropython](https://github.com/GoogleCloudPlatform/iot-core-micropython)
- [uasn1](https://github.com/mkomon/uasn1)
