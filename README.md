<img src="/docs/fjlogo.png" alt="Flow Jam Logo" width="128" height="128" />

# Flow Jam

Flow Jam is a little Python toy I hacked together in an evening that provides some flow-following background jams for when you're really in the zone.

## How does it work?
1. It captures your global keypresses (what! yeah, I know, but it's a toy, and the source is here!)
2. Based on the number of keypresses you've had in the fall-off period, the app will overlay tracks of music on top of each other that falls in line with your "flow."

## System requirements
1. macOS (only played with on Sonoma)
2. Python 3 & pip

## How do I get started?
1. `pip install -r requirements.txt`
2. `python app.py`
3. Start typing anywhere.

There are a few command-line arguments you can provide. Take a look at them by running `python app.py -h`, or:

`-t, --threshold`
* *Default: 300*
* Number of events to trigger to reach the maximum level, within the falloff period

`-f, --falloff`
* *Default: 2*
* Number of minutes in the falloff period

`-j, --jamspath`
* *Default: jam_library*
* The path which is searched to find jam manifests

I encourage playing around with the thresholds and falloff to find something that works well for your typing speed and patterns.

These settings can also be tweaked while your jam is playing with a little in-app menu.

## Can I add my own music?
Yeah! Take a look at jam_library/flowjam and copy the layout into another directory, tweaking the manifest.json and providing your own audio files.

I've tested with wave and mp3 files, but wave files worked better (in my experience) to create a more seamless loop due to their very simple encoding.

## What else should I know?
1. I hacked this together pretty quickly. I wasn't aiming for pretty code or a well-organized solution.
2. I used the pyobjc-framework-Quartz package to interact with Quartz APIs directly in a real kludgy way to capture keypresses, but hey - it works!
  1. ⚠️ **PLEASE** ⚠️ check out flowjam/key_event_manager.py to review the source for the listener before running, so you know nothing nefarious is going on.
3. You'll have to grant whatever terminal you're using to run this Accessibility permissions, because of the Quartz API use. Leave those permissions at your own risk!
  1. The first time you start this, you'll probably need to grant permissions then restart the app.
4. I'm sure there are weird things with this project I haven't encountered, yet. Here are some I *have* encountered:
  1. The keypress events stopped working, and restarting the app didn't help. I had to reboot my computer. Something at the Quartz layer? Who knows!
  2. One time, my terminal kept stealing window focus. I assume it was because of this, but it only happened once, which was weird.
5. I'm not at all talented at making music, but I was able to find some nice royalty-free stuff that overlaid quite nicely for the demo jam.
6. I was inspired by games and other media that build up the intensity of music based on events happening. When I looked around my room for an orchestra to do the same for me, I was sorely disappointed, and decided to throw this together instead.

Have fun!
