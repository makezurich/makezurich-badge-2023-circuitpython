import mz_badge,time

leds = mz_badge.LEDs()
leds.gauge(20)
time.sleep(1)
leds.traffic_light_pixel(0,1,50)
leds.traffic_light_pixel(1,0,30)
time.sleep(1)
leds.show_info()
time.sleep(1)
leds.fade_pixel(0,0,0.1)
leds.fade_pixel(0,1,0.3)
leds.fade_pixel(0,2,0.5)
leds.fade_pixel(1,0,0.7)
leds.fade_pixel(1,1,0.9)
leds.fade_pixel(1,2,1)
time.sleep(1)
leds.clear()

from analogio import AnalogIn

potentiometer = AnalogIn(mz_badge.ADC_1)

while True:
    leds.fade_pixel(0,0,potentiometer.value/65535)
    time.sleep(0.25)

