---
layout: default
title: SC Joystick Configuration
tagline: DRAFT
description: >-
  This page is a tutorial I wrote to document the development of my inputs to
  Star Citizen.
projpath: SC-Joystick-Configuration
version: 0.0.1 Beta
author: danricho
permalink: /index.html
published: true
---

# Introduction 

When I started playing **Star Citizen [\[1\]](#reference-list "Reference List: [1]")** (SC) I found the key combinations required during "flight" overwhelming. I saw this problem as something that could be overcome by designing a physical "control panel" which would have the most important functions mapped to a dedicated button.

*Note: I only outline setting up the SC "flight" functionality as I primarily use keyboard and mouse for other parts of the game such as First-Person Shooting (FPS).*

# Development Log

## Joysticks

The first thing I decided was that I wanted my flight control to be a **HOSAS** (Hands On Stick And Stick) rather than the perhaps more common HOTAS (Hand On Throttle And Stick) setup. 
My rationale is that the game is primarily space based and the additional axes that the dual sticks afford, provide fine control of all three "strafing" directions as well as all three rotational "Pitch, Roll and Yaw" rotations.

Having decided on the HOSAS setup, the next question was which joysticks I wanted to use. I decided upon two **Thrustmaster T.16000m** joysticks. The factors that decided this choice were:

  - they are very affordable,
  - they are quite easily sourced, 
  - they can be configured as left or right handed, and
  - they are very accurate.
  
![My Dual T.16000m Layout][IMG-STICK_LAYOUT]

## Control Panel

The first step in designing the control panel was to determine how many buttons I wanted to implement. I settled at around 60 after deciding which SC functions would be mapped to the panel itself, the buttons on the sticks, neither or both.

![My Control Panel Layout][IMG-PANEL_LAYOUT]

Next, I chose the type of buttons and the enclosure I wanted and ordered those. Whilst I was waiting I started thinking about how to drive it. For this, I chose the Arduino as the micro-controller platform as I've used them previously, they are simple, and they work straight out of the box. 

The specific Arduino I chose was an "eBay knockoff" of the **5V/16MHz Pro Micro [\[4\]](#reference-list "Reference List: [4]")**. This is based on the **Leonardo** range of Arduinos which allow Human Interface Device (HID) emulation as the micro-controller itself (ATmega32u4) has built-in USB communication, which eliminates the need for a secondary processor. 

The only limitation with Arduinos for a project like this is that they provide limited general purpose Input/Output (GPIO or I/O) pins. There are many workarounds including wiring the buttons in a matrix to and cyclically read them by row. This would've added complexity so the workaround I chose for this was to use external devices to add more, as this reduced the complexity of the Arduino software and the hardware required to support the switches.

The Microchip **MCP23017 IC [\[2\]](#reference-list "Reference List: [2]")** is a 16-bit I/O expander with an I<sup>2</sup>C serial control interface. It works in a similar manner to s standard parallel to serial shift register. The differences (and the reasons I chose these chips) are as follows:

  - Multiple chips can be used on the serial bus and each adds 16 additional I/O pins;
  - The 16 I/O pins include pull-up resistors meaning that discrete resistors for each button weren't needed; and,
  - Adafruit's MCP23017 Library makes interfacing with these pins as easy as it is with the built-in Arduino pins.

![Control Panel Driver Board][IMG-PANEL_DRV_BOARD]

I have used four MCP23017 ICs giving me 64 additional I/O pins, sacrificing only 2 of the Arduino GPIO pins for I<sup>2</sup>C serial communication with the chips.

With sufficient I/O pins available (and my buttons and enclosure in-hand), I assembled amd wired it all up.

![Control Panel Wiring][IMG-PANEL_WIRING]

### Firmware

I am providing basic examples of how to use the libraries in this section.

Here is a bare-basic example of how to use the **MCP23017 Library [\[3\]](#reference-list "Reference List: [3]")**:

~~~c++
#include <Wire.h>
#include "Adafruit_MCP23017.h"

// Create a MCP23017 object
Adafruit_MCP23017 myMCP;

void setup() {
  // Setup the MCP with address 0
  myMCP.begin(0);
  // Sets pin 0 of the MCP 
  // to be an input with pull-up resistor
  myMCP.pinMode(0, INPUT); 
  myMCP.pullUp(0, HIGH);
}

void loop() {
  // Reads the current state of pin 0 on the MCP
  bool currentInputState = myMCP.digitalRead(0)
  // Do something with it...
}
~~~

Initially, the Arduino HID emulation was limited to Keyboard and Mouse functionality but MHeironimus has developed the HID Joystick Library.

At the time I am writing this, the release version of the Joystick Library is v1.0.1 which allows multiple or single joysticks with a maximum or 32 buttons to be emulated by the Arduino. I wanted to emulate only one joystick but I wanted at least 60 buttons. Luckily, the library has a (currently Beta) version 2.0 which allows the number of buttons to be specified. 

*Note: Arduino IDE 1.6.6 (or above) is required for this library.*

Here is a bare-basic example of how to use the **HID Joystick Library [\[5\]](#reference-list "Reference List: [5]")**:

~~~c++
#include <Joystick.h>

// Create a Joystick object
Joystick_ myJoystick;

void setup() {
  // Setup the Joystick
  myJoystick.begin();
}

void loop() {
  // State of the button (read something)...
  bool buttonState = true;
  // Report the first (0) button state to buttonState
  myJoystick.setButton(0, buttonState);
}
~~~

My Arduino firmware is available [here][LINK-REPO-ARDFW]. When loaded, the Arduino is listed as a standard USB Game Controller in Windows (run command: `joy.cpl`). The standard utility shows only the first 32 buttons. To see more, I had success with **Pointy's Joystick Test [\[6\]](#reference-list)**. 

## Controller Fusion

At this point three controllers were visible to the computer; two T.16000m joysticks and the control panel. There were multiple limitations to simply mapping these three controllers directly:

  1. A maximum of 50 buttons are allowed per joystick in SC which means that not all buttons on the control panel could be used.
  2. Only one button can be mapped to each function.
  3. Any custom button functions must be implemented on the Arduino, requiring all actions be mapped to an Arduino "joystick button".

To remove these limitations, multiple options exist. The solution I chose is one I discovered on the SC forums. WhiteMagic's Joystick Gremlin was developed to utilize "virtual joysticks" which can be linked to the physical joysticks in many ways.

### vJoy

Once configured, vJoy is a set and forget tool. It creates the virtual joysticks and unless troubleshooting or changing the vJoy parameters, there is little evidence that it is even installed. I set it up as follows:

  1. Install **vJoy [\[8\]](#reference-list "Reference List: [8]")**.
  2. Launch to configuration interface and create 2 virtual joysticks (1 tab each).
  3. For each joystick, allocate:  
     - 3 axis (X, Y, Z)
     - 3 rotations (Rx, Ry, Rz)
     - Slider
     - Hat
     - 50 buttons (maximum allowed in SC)  
  4. Activate vJoy.
  
vJoy also include a utility to monitor the states of the vJoy joysticks. This is found in the start menu as `Monitor vJoy`.

The virtual joysticks were now shown in the list of USB game controllers.

### Joystick Gremlin

Joystick Gremlin allows mapping of joystick controls to the virtual joysticks' controls. This mapping can take many forms. Step 2 below describes the types of mapping possible with this tool.

  1. Install **Joystick Gremlin [\[7\]](#reference-list "Reference List: [7]")**.
  2. Assign the buttons/axes/sliders/hats of each physical controller (accessible by tabs) to vJoy or keyboard actions. This can be done in various ways:  
     - **Remap**: physical action (eg: button press) is cloned to the virtual action (eg: vJoy button press, keyboard button press, etc.  
     - **Macro**: physical action triggers a pre-programmed sequence of virtual actions.  
     - **Custom Modules**: allow a vast array of options by writing code which performs virtual actions using various triggers including physical actions and time cycles. These modules are limited only by your familiarity with python code (see my modules for examples).  
  3. Activate Joystick Gremlin (or trigger activation by focus on Star Citizen.
  
Extensive documentation on the use of Joystick Gremlin is available on WhiteMagic's [project page][LINK-EXT-7].

My Joystick Gremlin configuration (.xml) and and custom modules (.py) are available [here][LINK-REPO-JGCONF] and need to be placed in the directory:  
`%userprofile%\Joystick Gremlin\`  
*Note: These files are created for Joystick Gremlin v5 which is pre-release at the time of writing. Thanks for all of your help WhiteMagic!*

### SC Joystick Mapper

To map the virtual joysticks (vJoy 1 & 2) to SC keybindings, **SC Joystick Mapper [\[9\]](#reference-list "Reference List: [9]")** can be helpful. It creates an XML file which can be imported into the game.

My SC keybinding (.xml) is available [here][LINK-REPO-SCXML], and needs to be placed in the directory:   
`StarCitizen\CitizenClient\USER\Controls\Mappings\`

The keymapping is loaded by navigating in the menu to: Options, Keybinding, Advanced Controls Customization.
Under Control Profiles, select the keymapping and chose the controllers to load.

# Result

The end result is that I can now utilise all of the functions that the ships provide in Star Citizen with the added bonus of some specialised custom functions.

![Finished Panel][IMG-PANEL_FINISHED]

## Mapping Matrix

I have reworked the spreadsheet I used to keep track of the various functions whilst I was developing this project. It traces each button through it's various representations from physical button all the way to the key binding it controls in SC. I also includes the type of mapping I've used for each within Joystick Gremlin. 
It is available [here][LINK-REPO-MAPPING].


**Lastly, in case you are wondering, my in game moniker is [danricho][LINK-EXT-10].  
See you 'round the 'verse!**

# Reference List

[1]  [Star Citizen][LINK-EXT-1] by *Cloud Imperium Games*  
[2]  [MCP23017 datasheet][LINK-EXT-2] by *Microchip*  
[3]  [MCP23017 Arduino Library][LINK-EXT-3] by *Adafruit*  
[4]  [5V/16MHz Pro Micro product page][LINK-EXT-4] by *Sparkfun*  
[5]  [HID Joystick Arduino Library][LINK-EXT-5] by *MHeironimus*  
[6]  [Pointy's Joystick Test][LINK-EXT-6] by *Pointy*  
[7]  [Joystick Gremlin][LINK-EXT-7] by *WhiteMagic*  
[8]  [vJoy][LINK-EXT-8] by *Shaul Eizikovich*  
[9]  [SC Joystick Mapper][LINK-EXT-9] by *SCToolsfactory*  




[comment]: # (==========================================================)
[comment]: # (REFERENCED LINKS AND IMAGES)
[comment]: # (==========================================================)


[IMG-STICK_LAYOUT]: images/sticks_layout.jpg
[IMG-PANEL_LAYOUT]: images/panel_layout.jpg
[IMG-PANEL_DRV_BOARD]: images/panel_driver_board.jpg
[IMG-PANEL_WIRING]: images/panel_wiring.jpg
[IMG-PANEL_FINISHED]: images/panel_finished.jpg
[IMG-PLACEHOLDER]: images/placeholder.jpg


[LINK-REPO-ARDFW]: https://github.com/danricho/SC-Joystick-Configuration/tree/master/ArduinoFirmware "Repo Link: Arduino Firmware"
[LINK-REPO-JGCONF]: https://github.com/danricho/SC-Joystick-Configuration/tree/master/Joystick%20Gremlin "Repo Link: Joystick Gremlin"
[LINK-REPO-SCXML]: https://github.com/danricho/SC-Joystick-Configuration/blob/master/dual_t16000m_leonardo_SCmap.xml "Repo Link: SC XML Map"
[LINK-REPO-MAPPING]: https://raw.githubusercontent.com/danricho/SC-Joystick-Configuration/master/Mapping%20Summary.xlsx "Repo Link: Mapping Spreadsheet"


[LINK-EXT-1]: https://robertsspaceindustries.com/ "'Roberts Space Industries' website"
[LINK-EXT-2]: http://ww1.microchip.com/downloads/en/DeviceDoc/21952b.pdf "'MCP23017' datasheet"
[LINK-EXT-3]: https://github.com/adafruit/Adafruit-MCP23017-Arduino-Library "'MCP23017' Arduino Library repo"
[LINK-EXT-4]: https://www.sparkfun.com/products/12640 "'Pro Micro' Sparkfun product page"
[LINK-EXT-5]: https://github.com/MHeironimus/ArduinoJoystickLibrary "'HID Joystick' Arduino Library repo"
[LINK-EXT-6]: http://www.planetpointy.co.uk/joystick-test-application/ "'Pointys Joystick Test' tool"
[LINK-EXT-7]: http://whitemagic.github.io/JoystickGremlin/ "'Joystick Gremlin' project page"
[LINK-EXT-8]: http://vjoystick.sourceforge.net/ "'vJoy' Sourceforge page"
[LINK-EXT-9]: https://github.com/SCToolsfactory/SCJMapper-V2 "'SCJMapper' repo"
[LINK-EXT-10]: https://robertsspaceindustries.com/citizens/danricho "My Star Citizen profile"
