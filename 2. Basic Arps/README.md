# 2 - Basic Arps
This example waits for a trigger at the pulse 1 input and then:
1. Picks a random root note from the defined scale
2. Picks a random chord from the defined chords
3. Outputs CV (CV 1 Out) and gate (Pulse 1 Out) for each note of the chord with a short delay between each one

## Experiment
- Try changing *scale_root*, *scale_mode* and *chord* to see what effect it has
- Change *octave* to shift the output up or down an octave
- Reduce or increase the delay between notes

## Extend
- Repeat the notes of the chord until the next trigger is received at the pulse 1 input
- Show the current note of the chord using the LEDs
- Leave the output of the root note on pulse and CV 1 but change subsequent notes to use pulse and CV output 2
- Control the delay between notes using one of the knobs