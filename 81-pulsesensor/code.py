import time
import board
import neopixel
import analogio


pixel_pin = board.GP22
num_pixels = 6

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=True)

light = analogio.AnalogIn(board.A0)

# How many light readings per sample
NUM_OVERSAMPLE = 10

# How many samples we take to calculate 'average'
NUM_SAMPLES = 20
samples = [0] * NUM_SAMPLES

USE_SIMPLE_BPM = True

while True:

    if USE_SIMPLE_BPM:
        for i in range(NUM_SAMPLES):
            # Take NUM_OVERSAMPLE number of readings really fast
            oversample = 0
            for s in range(NUM_OVERSAMPLE):
                oversample += float(light.value)
            # and save the average from the oversamples
            samples[i] = oversample / NUM_OVERSAMPLE  # Find the average

            mean = sum(samples) / float(len(samples))  # take the average

            smoothvalue = samples[i] - mean # 'center' the reading
            print(smoothvalue)  

            # Simple smoothed bpm
            bpm = min(max(int(smoothvalue), 0), 255)

            # Turn only pixel #1 red
            pixels[0] = (bpm, 0, 0)
            pixels.show()

            time.sleep(0.025)  # change to go faster/slower
    
    else:
        # sophisticated algorithms etc.
        calculate_pulse_signal(light.value)
        if Pulse:
            pixels[0] = (255, 0, 0)
            pixels.show()
            time.sleep(0.2)
            pixels[0] = (0, 0, 0)
            Pulse = False

Pulse = False

# Source: https://learn.adafruit.com/pulse-sensor-displayed-with-neopixels/the-code
# THIS IS THE TIMER 2 INTERRUPT SERVICE ROUTINE. 
def calculate_pulse_signal(value):
    global sampleCounter, lastBeatTime, Pulse, value, thresh, N, P, T, IBI, BPM

    sampleCounter += 2                          # keep track of the time in mS with this variable
    N = sampleCounter - lastBeatTime            # monitor the time since the last beat to avoid noise

    # find the peak and trough of the pulse wave
    if value < thresh and N > (IBI/5)*3:        # avoid dichrotic noise by waiting 3/5 of last IBI
        if value < T:                           # T is the trough
            T = value                           # keep track of lowest point in pulse wave 
    if value > thresh and value > P:            # thresh condition helps avoid noise
        P = value                               # P is the peak
                                                # keep track of highest point in pulse wave
    # NOW IT'S TIME TO LOOK FOR THE HEART BEAT
    # signal surges up in value every time there is a pulse
    if N > 250:                                 # avoid high frequency noise
        if value > thresh and Pulse == False and N > (IBI/5)*3:        
            Pulse = True                        # set the Pulse flag when we think there is a pulse
            IBI = sampleCounter - lastBeatTime  # measure time between beats in mS
            lastBeatTime = sampleCounter        # keep track of time for next pulse
            if SecondBeat:                      # if this is the second beat, if secondBeat == TRUE
                SecondBeat = False              # clear secondBeat flag
                for i in range(0,10):           # seed the running total to get a realisitic BPM at startup
                    rate[i] = IBI
                BPM = 60000/((rate[0]+rate[1]+rate[2]+rate[3]+rate[4]+rate[5]+rate[6]+rate[7]+rate[8]+rate[9])/10)
            if FirstBeat:                       # if it's the first time we found a beat, if firstBeat == TRUE
                FirstBeat = False               # clear firstBeat flag
                SecondBeat = True               # set the second beat flag
                return
            # keep a running total of the last 10 IBI values
            runningTotal = 0                    # clear the runningTotal variable    
            for i in range(0,9):                # shift data in the rate array
                rate[i] = rate[i+1]             
                runningTotal += rate[i]         # add up the 9 oldest IBI values
            rate[9] = IBI                       # add the latest IBI to the rate array
            runningTotal += rate[9]             # add the latest IBI to runningTotal
            runningTotal /= 10                  # average the last 10 IBI values 
            BPM = 60000/runningTotal            # how many beats can fit into a minute? that's BPM!
