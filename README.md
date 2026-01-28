# iPod dupe project

The long-term goal of this project is to create a working portable music player device. As I progress I am learning about various aspects of Python, Linux, file system management, basic hardware prototyping, and eventually PCB design, to name a few. The project is also meant to provide a learning opportunity based on and beyond knowledge I have gained/am currently acquiring through studying in a data science master's.

*Disclaimer: This project is using AI assitance and is primarily a learning project aimed at exploring Python and other parts of embedded development, and my intended device is not meant as a commercial product of any kind.*

Mental model of major parts of this project:

```         
+--------------------------------------------------+
|                  Application                     |
|                                                  |
|  - State machine (menu, playback, settings)      |
|  - Playlist logic                                |
|  - Metadata parsing                              |
|  - UI rendering                                  |
+-------------------+------------------------------+
                    |
+-------------------v------------------------------+
|          Platform Abstraction Layer              |
|                                                  |
|  - Input: buttons / wheel / bluetooth            |
|  - Output: screen / audio / haptics              |
|  - Timing / interrupts                           |
+-------------------+------------------------------+
                    |
+-------------------v------------------------------+
|            Linux + Drivers + Hardware            |
|                                                  |
|  - ALSA / PulseAudio / PipeWire                  |
|  - GPIO / SPI / I2C                              |
|  - DAC / Bluetooth / Storage                    |
+--------------------------------------------------+
```
