import gremlin
from gremlin.input_devices import keyboard, macro
import time
from vjoy.vjoy import AxisName

# used to allow the longer functions to not block the controllers while running
import threading

# define the controllers
right_t16000m = gremlin.input_devices.JoystickDecorator(name="T.16000M", device_id=(1325664945, 1), mode="Default")
arduino_leonardo_1 = gremlin.input_devices.JoystickDecorator(name="Arduino Leonardo", device_id=(1092826752, 4), mode="Default")
left_t16000m = gremlin.input_devices.JoystickDecorator(name="T.16000M", device_id=(1325664945, 0), mode="Default")

# Logging Methods:
import logging
# logging.getLogger("system").debug("System debug info.")
# logging.getLogger("user").debug("User debug info.")
# or
# gremlin.util.display_error("Error popup")

def non_blocking_qt_gtfo(): # "QT GTFO" FUNCTION
    # This function warps in the direction the ship is facing immediately. Used in emergencies.
    # logging.getLogger("user").debug("GTFO running.")  

    vjoy = gremlin.input_devices.VJoyProxy()
    joy = gremlin.input_devices.JoystickProxy()

    vjoy[2].button(30).is_pressed = True # ENABLE QT MODE
    time.sleep(0.25)
    vjoy[2].button(30).is_pressed = False
    time.sleep(1)
    vjoy[2].button(29).is_pressed = True # QT ENGAGE
    time.sleep(0.25)
    vjoy[2].button(29).is_pressed = False
   
# ARDUINO BUTTON 8 PRESS.
@arduino_leonardo_1.button(7)
def qt_gtfo(event, vjoy): # "QT GTFO" FUNCTION
    if event.is_pressed:
      logging.getLogger("user").debug("'QT Escape' button pressed.")
      threading.Timer(0.1, non_blocking_qt_gtfo).start()  
    
def non_blocking_all_cm_firing():
    # This function fires the selected counter measure, toggles countermeasure, fires that counter measure and toggles back.
    # logging.getLogger("user").debug("All CM running.")
    
    vjoy = gremlin.input_devices.VJoyProxy()
    joy = gremlin.input_devices.JoystickProxy()
    
    vjoy[1].button(38).is_pressed = True # FIRE COUNTER MEASURE
    time.sleep(0.1)
    vjoy[1].button(38).is_pressed = False
    time.sleep(2)
    
    vjoy[1].button(40).is_pressed = True # CYCLE COUNTER MEASURE
    time.sleep(0.1)
    vjoy[1].button(40).is_pressed = False
    time.sleep(1)
    
    vjoy[1].button(38).is_pressed = True # FIRE COUNTER MEASURE
    time.sleep(0.1)
    vjoy[1].button(38).is_pressed = False
    time.sleep(2)
    
    vjoy[1].button(40).is_pressed = True # CYCLE COUNTER MEASURE
    time.sleep(0.1)
    vjoy[1].button(40).is_pressed = False
    
# ARDUINO BUTTON 16 PRESS.
@arduino_leonardo_1.button(8)
def all_cm(event, vjoy): # "ALL CM" FUNCTION
    if event.is_pressed:
      logging.getLogger("user").debug("'All C.M.' button pressed.")
      threading.Timer(0.1, non_blocking_all_cm_firing).start()
  
  
######################################################
##                                                  ##
##  KEYBOARD MACROS ONLY WORK IN STAR CITIZEN IF    ##
##  JOYSTICK GREMLIN IS LAUNCHED AS ADMINISTRATOR   ##
##                                                  ##
######################################################
  
# This macro toggles the chat window.
macro_toggle_chat = macro.Macro()
macro_toggle_chat.tap("F12")

# ARDUINO BUTTON 54 PRESS.
@arduino_leonardo_1.button(54)
def custom_1(event, vjoy):
    if event.is_pressed:
      logging.getLogger("user").debug("Custom 1 button pressed.")
      macro_toggle_chat.run()

# This macro is the salute emote. It must be run with the chat window hidden.
macro_salute = macro.Macro()
macro_salute.tap(macro.Keys.F12)
macro_salute.tap(macro.Keys.Enter)
macro_salute.tap(macro.Keys.Slash)
macro_salute.tap(macro.Keys.S)
macro_salute.tap(macro.Keys.A)
macro_salute.tap(macro.Keys.L)
macro_salute.tap(macro.Keys.U)
macro_salute.tap(macro.Keys.T)
macro_salute.tap(macro.Keys.E)
macro_salute.tap(macro.Keys.Enter)
macro_salute.tap(macro.Keys.F12)

# ARDUINO BUTTON 55 PRESS.
@arduino_leonardo_1.button(55)
def custom_2(event, vjoy):
    if event.is_pressed:
      logging.getLogger("user").debug("Custom 2 button pressed.")
      macro_salute.run()

# This macro is the rude (flip the bird, etc) emote. It must be run with the chat window hiudden.
macro_rude = macro.Macro()
macro_rude.tap(macro.Keys.F12)
macro_rude.tap(macro.Keys.Enter)
macro_rude.tap(macro.Keys.Slash)
macro_rude.tap(macro.Keys.R)
macro_rude.tap(macro.Keys.U)
macro_rude.tap(macro.Keys.D)
macro_rude.tap(macro.Keys.E)
macro_rude.tap(macro.Keys.Enter)
macro_rude.tap(macro.Keys.F12)

# ARDUINO BUTTON 56 PRESS.
@arduino_leonardo_1.button(56)
def custom_3(event, vjoy):
    if event.is_pressed:
      logging.getLogger("user").debug("Custom 3 button pressed.")
      macro_rude.run()

# This macro toggles video recording.
macro_toggle_video_rec = macro.Macro()
macro_toggle_video_rec.press("RAlt")
macro_toggle_video_rec.tap("F7")
macro_toggle_video_rec.release("RAlt")

# ARDUINO BUTTON 57 PRESS.
@arduino_leonardo_1.button(57)
def custom_4(event, vjoy):
    if event.is_pressed:
      logging.getLogger("user").debug("Custom 4 button pressed.")
      macro_toggle_video_rec.run()

# This macro saves the last 5 minutes of video (or other duration in buffer).
macro_save_video_last_five = macro.Macro()
macro_save_video_last_five.press("RAlt")
macro_save_video_last_five.tap("F8")
macro_save_video_last_five.release("RAlt")
   
# ARDUINO BUTTON 58 PRESS.
@arduino_leonardo_1.button(58)
def custom_5(event, vjoy):
    if event.is_pressed:
      logging.getLogger("user").debug("Custom 5 button pressed.")
      macro_save_video_last_five.run()
