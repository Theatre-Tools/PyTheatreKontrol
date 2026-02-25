# Eos Roadmap
This is where the roadmap for Eos family support can be found. Due to the scale of this project, it's important for me to plan and breakdown my development choices, and my priorities.

## Minimum Viable Product (MVP)
- Basic Cue List TX/RX:
    - Interrogate the console for information about cue list counts, cue counts, and cue details.
    - Interrogate the console for information about active and pending cues, and handle those in the background with queues.
    - Record Cues to the active Cue list, with properties like labels and fade times.
    - Fire Cues on the active cue list.
    - GoTo_Cue on the active cue list.
- Basic Submaster TX/RX:
    - Interrogate the console for information regarding submaster properties, fader levels, etc.
    - Set submaster levels.
- Basic Preset and Pallete RX/TX:
    - Interrogate the console on information regarding recorded presets and palletes (Names, counts, fixture types, etc.)
    - Interrogate the console for information regarding active presets and palletes.
    - Record presets and palletes.


## Long term goals
- Implement event driven support for actions such as cue firing, submaster level changes, cue updates, file saves, etc.
- Implement support for selecting groups and channels, and recording cues with those selections.
- Implement setting executors on specific cues or submasters, or events.
- Implement support for more complex cue properties such as follow, fade times, etc.
- Implement support for more complex preset and pallete properties, such as fixture selections, etc.