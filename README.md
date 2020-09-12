# RaspBeats

RaspBeats is a Raspberry-Pi based live looper with support for up to 7 channels and multiple midi inputs


## Installation

Once the repository has been cloned, use pip to install the requirements for Raspbeats.

```bash
pip install -r requirements.txt
```

Next, create two fifos in the same directory.

```bash
$ mkfifo record_fifo
$ mkfifo playback_fifo
```

Update the constants.py file to reflect accurate directories for record_fifo and playback_fifo
At the end of your ~./bashrc file add the following line:

```bash
python /your_directory_here/main.py
```

## Usage

Currently the application is designed to work with the Akai MPK Mini MKII Midi keyboard and the Alessis Q49 Midi keyboard. The Akai keyboard controls most of the functions and the Q49 keyboard is used purely for note input. To start the application, restart the Raspberry Pi after installation. Make sure that the Bank A/B is green on the Akai keyboard. A metronome sound should be outputted via the speakers (By default this is outputted on channel 7). 

Initially, the application is in playback mode where all notes from both keyboards are played based on the default instrument on channel 1. In order to change the current instrument/channel selected, enter program change mode by pressing the button on the Akai and tap any of the pads from 1-7 to switch to that channel. Each channel can be customized to its own instrument. 

The volume for each channel can be adjusted via the knobs on the Akai keyboard. Each knob from 1-7 controls the corresponding channel volumes. Knob 8 has no function.

In order to enter record mode, enter prgram change mode by pressing the button on the Akai and tap pad 8. At this point, any note you play for 16 bars will be recorded. At the end of the recording, record mode is turned off and the recording is looped.

## Customization

Raspbeats can be customized for any song. You can change both the record length and the preset instruments by editing the labeled variables in the constants.py file.