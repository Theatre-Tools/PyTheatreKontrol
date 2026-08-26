# ETC Eos Driver

This is a proof-of-concept driver. I chose Eos to build the first driver for because I understand it, and because I have an understanding of what OSC features are commonly used.

As this is the first driver, there is a good chance that the architecture of how drivers are built will change throughout this driver's development, as we settle on the best structure. Please bear with me as I figure out how this will be built, and as I document it accordingly. Hopefully, once this driver is in a shippable and stable state, it will become much easier to build drivers for similar hardware.

This will all make much more sense when I document the architecture of the framework, and how drivers will be defined to interface with the existing standards laid out in the framework.

Below is a list of requirements that I want to have implemented before we ship the driver as stable.

## Extensions to Basic Control

Outside of the default Control Classes provided by PyTK, the following methods will be available specifically for Eos consoles.

### Playback Control

The following commands are the minimum for a device to be eligible for the `PlaybackControl` class.

### Cue Control

The following commands are the minimum for a device to be eligible for the `CueControl` class.

- [ ] Up time
- [ ] Down time
- [ ] Focus time
- [ ] Color time
- [ ] Beam time
- [ ] Follow / Hang configuration
- [ ] Scene attribute configuration
- [ ] Executor configuration

### Programmer Control

The following commands are the minimum for a device to be eligible for the `ProgrammerControl` class.

- [ ] Channel control of Color, Beam, and Focus
- [ ] Sneak (including per-group / per-channel Sneak)
- [ ] Groups
- [ ] Palettes and Preset recording
- [ ] Write to the command line (not advised)

### Desk Control

A new Eos-specific device class, `DeskControl`, will handle administrative tasks as well as any tasks that don't fit within another scope.

- [ ] Macro control, initially running macros but eventually expanding to creating macros
- [ ] Desk health

## The Future

Long term, I would love to support a lot more. Things like getting more advanced data out of Eos are a big one for me, but that's a longer-term goal.

Please open an issue if you want support for a specific feature. If you tag it appropriately, I will take a look at it.