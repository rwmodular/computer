import random
import time
from machine import Pin, PWM

# setup pulse 1 input
# if it goes low (gets a pulse), set pulse1_got
# use an interupt for this so we don't miss it but keep it short so we don't block further interrupts
pulse1_got = False
def got_pulse(self):
    global pulse1_got
    pulse1_got = True

pulse1_in = Pin(2, Pin.IN, Pin.PULL_UP)
pulse1_in.irq(handler=got_pulse, trigger=Pin.IRQ_FALLING)

# setup pulse 1 output
pulse1_out = Pin(8, Pin.OUT)

# setup cv output
# -6v = 0, 0v = 32768, +6v = 65535
# TODO: change to 23 for actual cv1 out
cv1_out = PWM(Pin(22), freq=60000, duty_u16=32768)

# pwm value for each semitone 32768 for 6 volts/octaves or 72 semitones
pwm_semi = 32768 / 72

# define a root (C), scale (maj pentatonic) and some chords
scale_root = 0
scale_mode = [0, 2, 4, 7, 9]
chords = [[0, 4, 7], [0, 4, 7, 9], [0, 4, 7, 11], [0, 4, 7, 9, 14]]

# octave offset = 2 octaves down
octave = 0 - int(pwm_semi * 24)

# the current chord, chord root
# and note we're playing in that chord
chord = chords[0]
chord_root = 0
chord_note = 0

# pulse off and next note timers
pulse1_out_off_time = 0
next_note_time = 0

# play a semitone (0 = C = 0v)
def play_semitone(st):
    global pulse1_out_off_time, next_note_time

    # output the desired note
    # 0v (32768) + the requested note + our octave modifier
    output_val = 32768 + int(st * pwm_semi) + octave
    cv1_out.duty_u16(output_val)
    
    # output pulse (output is inverted)
    pulse1_out.value(0)
    
    # figure out when to end the pulse out and when to play the next note
    now = time.ticks_ms()
    pulse1_out_off_time = time.ticks_add(now, 10)
    next_note_time = time.ticks_add(now, 300)

while True:
    # if we should end pulse output
    if pulse1_out.value() == 0 and time.ticks_diff(pulse1_out_off_time, time.ticks_ms()) > 0:
        pulse1_out.value(1)

    # if we got a pulse start playing a new chord
    if pulse1_got:
        # clear the flag so we don't trigger again
        pulse1_got = False

        # pick a new root and chord
        chord_root = scale_root + random.choice(scale_mode)
        chord = random.choice(chords)
        
        # play the root & advance to the next note for next time
        play_semitone(chord_root)
        chord_note = 1

    # if we are playing a chord and its time to play the next note
    if chord_note > 0 and time.ticks_diff(next_note_time, time.ticks_ms()) <= 0:
        # play next note in chord
        play_semitone(chord_root + chord[chord_note])
        
        # advance to the next note for next time
        chord_note += 1
        if chord_note >= len(chord):
            chord_note = 0