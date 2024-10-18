import time
from machine import Pin, PWM

# setup pulse 1 output
pulse1_out = Pin(8, Pin.OUT)

# setup the mux logic pins
# we use them to control which analog input to read
mux_logic_a = Pin(24, Pin.OUT)
mux_logic_b = Pin(25, Pin.OUT)
# set them so we can read the big knob
mux_logic_a.value(0)
mux_logic_b.value(0)
# setup the adc pin to read the big knob
mux_val_x = machine.ADC(28)

# the next time we should output a pulse
pulse1_next_on_time = 0

# when the current pulse should end
pulse1_off_time = 0

while True:
    now = time.ticks_ms()
    
    # if we should start a pulse
    if time.ticks_diff(now, pulse1_next_on_time) > 0:
        # pulse outputs are inverted
        pulse1_out.value(0)
        
        # set the time for the next pulse
        # knob value will be 0 to 65535
        # so divide it down to get a usable milliseconds value
        pulse_gap = int(mux_val_x.read_u16() / 20)
        pulse1_next_on_time = time.ticks_add(now, pulse_gap)
        
        # end the pulse in 10ms
        pulse1_off_time = time.ticks_add(now, 10)
    
    # if we should end pulse output
    elif pulse1_out.value() == 0 and time.ticks_diff(now, pulse1_off_time) > 0:
        pulse1_out.value(1)
