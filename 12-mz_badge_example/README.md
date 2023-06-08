# MZ Badge Examnple

## lib

`mz_badge` is a smol lib to help you with the badge

Classes:

- *LEDs:* just a helper for the onboard neopixels, setting them up for easy use. It has some colors defined, as well as some functions.
 
  - `chase_color(color,wait)`: Sets all the LEDs to *color* one for one
  - `rainbow_cycle(wait)`: Cycle trough the colors 
  - `set_pixel(x,y,color)`: Sets LED at (*x*,*y*) to *color*
  - `clear()`: Sets all the LEDs to off
  - `fill(color)`: Sets all the leds to *color*
  - `show_info()`: Shows info about the badge bearer, as given in **settings.toml**. the roles on the top row, if it's allowed to take a picture from the badge_bearer is the first LED of the bottom row
      - *role_1*, *role_2*,*role_3*: "hw","sw","design" or "business"
      - *photo_allowed*: true or false
  - `traffic_light(val,threshold_1=33,threshold_2=66)`: Sets all the LEDs to green, yellow or red depnding on *val* and *threshold_1* and *threshold_2*
  - `traffic_light_pixel(x,y,val,threshold_1=33,threshold_2=66)`: Same as *traffic_light* but for the LED at (*x*,*y*).
  - `gauge(val,min=0,max=100,color=BLUE)`: shows *val* on 0 to 6 LEDs, if the *val* is between values the last LED is dimmed.
  - `fade_pixel(x,y,val,color1=GREEN,color2=RED)`: Sets LED at (*x*,*y*) to the color between *color1* and *color2* according to *val* between 0.0 and 1.0.

- *LoRaModule:* class to talk to the LoRa module.

  - `show_information()`: shows some info about the module
  - `set_mode(mode)`: sets the join mode, 'OTAA' is recommended
  - `join()`: joins using the set join mode
  - `send(mode,data)`: sends data using mode over LoRaWAN, better use the dedicated `send_hex(data)`, `send_string(data)`, `send_confirmed_hex(data)` or `send_confirmed_string(data)`
  - `at_send(cmd)`: send the AT command to the LoRa module. Mostly used internally, but see the protocol manual for what can be done:
  https://files.seeedstudio.com/products/317990687/res/LoRa-E5%20AT%20Command%20Specification_V1.0%20.pdf
 - `setup_and_join_otaa(self,appkey, appeui)`: sets up the appkey and appeui and joins using  OTAA

 TODO:
 [] implemnt ABP setup