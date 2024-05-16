from machine import Pin, ADC

# setup an array of the LEDs and set them all to off
leds = [None] * 6
for i in range(6):
    leds[i] = Pin(i + 10, Pin.OUT)
    leds[i].value(0)

# setup the audio inputs
left_in = ADC(27)
right_in = ADC(26)

# sample the inputs 10 times each
# get the max and min for each 
# return max - min for each
def readSample():
    lmin = 65535
    rmin = 65535
    lmax = 0
    rmax = 0
    
    for i in range(10):
        lval = left_in.read_u16()
        rval = right_in.read_u16()
        if lval < lmin:
            lmin = lval
        if lval > lmax:
            lmax = lval
        if rval < rmin:
            rmin = rval
        if rval > rmax:
            rmax = rval
        
    return lmax - lmin, rmax - rmin

# display the level (val) using the provded leds
def showVal(val, display_leds):
    for led in display_leds:
        led.value(0)
    if val > 2000:
        display_leds[0].value(1)
    if val > 8000:
        display_leds[1].value(1)
    if val > 20000:
        display_leds[2].value(1)

# loop forever reading samples and showing the values
# LEDs are numbers
# 0 1
# 2 3
# 4 5
while True:
    val = readSample()
    showVal(val[0], [leds[4], leds[2], leds[0]])
    showVal(val[1], [leds[5], leds[3], leds[1]])