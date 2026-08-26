# Lighting Framework Definition

The lighting framework is a loose set of methods to allow for simple abstraction of common functionality across different lighting control systems.

## Minimum to be Shipped

### Playback Control

The following commands are the minimum required for a device to be eligible for the `PlaybackControl` class.

- [ ] Send a GO command
- [ ] Send a Stop command
- [ ] Send a Goto Cue command

### Cue Control

The following commands are the minimum required for a device to be eligible for the `CueControl` class.

- [ ] Change Cue Time
- [ ] Change Cue Label
- [ ] Record Cue
- [ ] Delete Cue
- [ ] Copy Cue
- [ ] Move Cue

### Programmer Control

The following commands are the minimum required for a device to be eligible for the `ProgrammerControl` class.

- [ ] Basic Channel Control (Intensity)
- [ ] Basic Address Control (0–255 & 0%–100%)
- [ ] Drop Channel from the Programmer (return to the next layer of the desk)
- [ ] Clear the programmer (Sneak on Eos, Clear on Chamsys Magic Q & Avolitse Titan)