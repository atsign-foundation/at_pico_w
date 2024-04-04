<a href="https://atsign.com#gh-light-mode-only"><img width=250px src="https://atsign.com/wp-content/uploads/2022/05/atsign-logo-horizontal-color2022.svg#gh-light-mode-only" alt="The Atsign Foundation"></a><a href="https://atsign.com#gh-dark-mode-only"><img width=250px src="https://atsign.com/wp-content/uploads/2023/08/atsign-logo-horizontal-reverse2022-Color.svg#gh-dark-mode-only" alt="The Atsign Foundation"></a>

[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/atsign-foundation/at_pico_w/badge)](https://securityscorecards.dev/viewer/?uri=github.com/atsign-foundation/at_pico_w&sort_by=check-score&sort_direction=desc)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8277/badge)](https://www.bestpractices.dev/projects/8277)

# at_pico_w

Communicate with the atPlatform using a Raspberry Pi Pico W.

Developed with [MicroPython](https://micropython.org/).

## Usage

### Raspberry Pi Pico W

- Install the latest `firmware.uf2` onto your Pico W from
[atsign-foundation/micropython Releases](https://github.com/atsign-foundation/micropython/releases)
, as this is patched to enable AES CTR, which is used by atSigns.
- Fill all the fields of the `settings.json` file (ssid/passw of your Wi-Fi
network and atSign).
- Run `python3 build.py` to generate .mpy files
- Download [Thonny IDE](https://thonny.org/) and place all the files of the
built directory onto the Pico W file system.
- Place your `.atKeys` file in the `~/.atsign/keys/` directory (if the folder
doesn't exist, create it manually)
- Run `main.py` and select option `3` in the REPL ("Get privateKey for
@[yourAtSign]")
- Re-launch the REPL (run `main.py` again)
- Now you can select option `2` in the REPL to automatically get
authenticated in your DESS
- Enjoy!  :)

(If you get an error when attempting to find the atServer or when trying to
connect to it, run the REPL again)

### Micropython on Linux

- Compile micropython with coverage enabled (to get AES CTR) and place the
binary somewhere on the PATH (e.g. ~/.local/bin/)
- `micropython main.py`

## Libraries

- [iot-core-micropython](https://github.com/GoogleCloudPlatform/iot-core-micropython)
- [uasn1](https://github.com/mkomon/uasn1)
