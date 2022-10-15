# at_pico_w
Communicate with the atPlatform using a Raspberry Pi Pico W.

Developed with [MicroPython](https://micropython.org/).

## Usage
- Fill all the fields of the `settings.json` file (ssid/passw of your Wi-Fi network, atSign and privateKey). 
- Download [Thonny IDE](https://thonny.org/) and place all the files of this repository in the Pico W file system.
- Run `main.py` and enjoy!

## How to obtain privateKey
- Run [at_rsa_parameters](https://github.com/realvarx/at_rsa_parameters) tool (hint: run with "-p .atKeysFilePath" option)
- Place the output of the tool in the "privateKey" field of your settings.json file.

( `~/keys/` directory will be used in the future )
