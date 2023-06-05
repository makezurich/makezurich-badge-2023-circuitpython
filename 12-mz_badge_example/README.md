# MZ Badge Examnple

## lib

`mz_badge` is a smol lib to help you with the badge

It contains (as of now) two classes:

- *Neopixel:* just a helper for the onboard neopixels, setting them up for easy use. It has some colors defined, as well as some functions.
 
  - `chase_color(color,wait)`: fill the pixel to new color
  - `rainbow_cycle(wait)`: cycle trough the colors

- *LoRa_module:* class to talk to the LoRa module.

  - `show_information()`: shows some info about the module
  - `set_mode(mode)`: sets the join mode, OTAA is recommended
  - `join()`: joins using the set join mode
  - `send(mode,data)`: sends data using mode over LoRaWAN, better use the dedicated `send_hex(data)`, `send_string(data)`, `send_confirmed_hex(data)` or `send_confirmed_string(data)`
  - `at_send(cmd)`: send the AT command to the LoRa module. Mostly used internally, but see the protocol manual for what can be done:
  https://files.seeedstudio.com/products/317990687/res/LoRa-E5%20AT%20Command%20Specification_V1.0%20.pdf
 - `setup_and_join_otaa(self,appkey, appeui)`: sets up the 