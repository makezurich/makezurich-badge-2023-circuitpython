# MZ Badge Examnple

## lib

`mz_badge` is a smol lib to help you with the badge

It contains (as of now) two classes:

- *Neopixel*: just a helper for the onboard neopixels, setting them up for easy use. It has some colors defined, as well as some functions.
 
  - chase_color(color,wait): fill the pixel to new color
  - rainbow_cycle(wait): cycle trough the colors

- *LoRa_module: class to talk to the LoRa module. :
