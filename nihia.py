# name=NIHIA Script (testing)
# url= 

# MIT License

# Copyright (c) 2020 Hobyst

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Library for using the NIHIA protocol on FL Studio's MIDI Scripting API

# This script contains all the functions and methods needed to take advantage of the deep integration
# features on Native Instruments' devices
# Any device with this kind of features will make use of this script

import device

import midi
import utils

import math


###########################################################################################################################################
# Dictionaries
###########################################################################################################################################

# Button name to button ID dictionary
# The button ID is the number in hex that is used as the DATA1 parameter when a MIDI message related to that button is
# sent or recieved from the device
buttons = {
    "PLAY": 16,
    "RESTART": 17,
    "REC": 18,
    "COUNT_IN": 19,
    "STOP": 20,
    "CLEAR": 21,
    "LOOP": 22,
    "METRO": 23,
    "TEMPO": 24,
    
    "UNDO": 32,
    "REDO": 33,
    "QUANTIZE": 34,
    "AUTO": 35,

    "MUTE": 67,
    "SOLO": 68,

    "MUTE_SELECTED": 102,
    "SOLO_SELECTED": 103,

    "ENCODER_BUTTON": 96,
    "ENCODER_BUTTON_SHIFTED": 97,
    
    # The 4D encoder events use the same data1, but different data2
    # For example, if you want to retrieve the data1 value for ENCODER_PLUS you would do nihia.buttons.get("ENCODER_PLUS")[0]
    # 
    # data1 values are inverted for the axis of the 4D Encoder between A/M devices and S devices
    # The values represented here correspond to A/M-Series
    # D-pad
    "ENCODER_X_A": 50,
    "ENCODER_X_S": 48,
    "RIGHT": 1,
    "LEFT": 127,
    
    "ENCODER_Y_A": 48,
    "ENCODER_Y_S": 50,
    "UP": 127,
    "DOWN": 1,

    # Jog / knob
    "ENCODER_GENERAL": 52,
    "ENCODER_VOLUME_SELECTED": 100,
    "ENCODER_PAN_SELECTED": 101,

    "PLUS": 1,
    "MINUS": 127,

}

# Knob to knob ID matrix
# Each knob has two possible DATA1 values, one for volume and another for pan adjustment
# The rows specify the knob mode (volume adjustment and shifted/pan adjustment knobs)
# The columns specify the knob
# Example:
#   knobs[0][0] --> First knob without shift. It is meant to adjust volume.
#   knobs[0][1] --> First knob shifted (SHIFT button is being held down while using the knob). It is meant to adjust panning.
knobs = [
    [80, 81, 82, 83, 84, 85, 86, 87],
    [88, 89, 90, 91, 92, 93, 94, 95]
]

# The DATA2 value of a knob turning message specifies the speed the user is turning the knob at
# On S-Series keyboards, the knobs are speed-sensitive and send different DATA2 values to specify the turning speed
# - If turned clockwise, the speed will go from 0 to 63 (slowest to fastest)
# - If turned counterclockwise, the speed will go from 127 to 65 (slowest to fastest, they are inverted)
# On A/M-Series, the knobs aren't speed-sensitive and they will always report the max value for each direction
# - If turned clockwise, the DATA2 value will be 63
# - If turned counterclockwise, the DATA2 value will be 65
KNOB_INCREASE_MIN_SPEED = 0     # DATA2 byte sent by the keyboard on clockwise knob turning messages at minimum speed
KNOB_INCREASE_MAX_SPEED = 63    # DATA2 byte sent by the keyboard on clockwise knob turning messages at maximum speed

KNOB_DECREASE_MIN_SPEED = 127   # DATA2 byte sent by the keyboard on counterclockwise knob turning messages at minimum speed
KNOB_DECREASE_MAX_SPEED = 65    # DATA2 byte sent by the keyboard on counterclockwise knob turning messages at maximum speed

# Dictionary that goes between the different kinds of information that can be sent to the device to specify information about the mixer tracks
# and their corresponding identification bytes
mixerinfo_types = {
    "VOLUME": 70,
    "PAN": 71,
    "IS_MUTE": 67,
    "IS_SOLO": 68,
    "NAME": 72,
    
    # This one makes more sense on DAWs that create more tracks as the user requests it, as there might be projects (for example) on Ableton Live
    # with only two tracks
    # However, since FL Studio has all playlist and mixer tracks created, it has no use at all (maybe on the channel rack) and all tracks should have
    # their existance reported as 1 (which means the track exists) in order to light on the Mute and Solo buttons on the device
    "EXIST": 64,
    "SELECTED": 66,

    "SELECTED_AVAILABLE": 104,
    "SELECTED_MUTE_BY_SOLO": 105,

    # This one only will make an effect on devices with full feature support, like the S-Series MK2 and it's used to send the peak meter information
    "PEAK": 73,

    # Serves to tell the device if there's a Komplete Kontrol instance added in a certain track or not
    # In case there's one, we would use mixerSendInfo("KOMPLETE_INSTANCE", trackID, info="NIKBxx")
    # In case there's none, we would use mixerSendInfo("KOMPLETE_INSTANCE", trackID, info="")
    # NIKBxx is the name of the first automation parameter of the Komplete Kontrol plugin
    "KOMPLETE_INSTANCE": 65,

    # The S-Series keyboard have two arrows that graphically show the position of the volume fader and the pan on the screen
    # These definitions have the MIDI values that have to be set as the data1 value of a simple MIDI message to tell the device where the volume arrow
    # or the pan arrow should be for the first track
    # For the rest of the tracks, you sum incrementally
    # Example:
    # ----------------------------------------------------
    # BF 50 00  // Moves the volume fader of the first track down to the bottom 
    # BF 50 40  // Moves the volume fader of the first track to the middle
    # 
    # BF 51 00  // Moves the volume fader of the second track down to the bottom 
    # BF 51 40  // Moves the volume fader of the second track to the middle
    # 
    # BF 58 00  // Moves the pan fader of the first track down to the bottom 
    # BF 58 40  // Moves the pan fader of the first track to the middle
    # 
    # BF 59 00  // Moves the pan fader of the second track down to the bottom 
    # BF 59 40  // Moves the pan fader of the second track to the middle    
    
    "VOLUME_GRAPH": 80,
    "PAN_GRAPH": 88,
}

# Track types dictionary
# Used when reporting existance of tracks
track_types = {
    "EMPTY": 0,
    "GENERIC": 1,
    "MIDI": 2,
    "AUDIO": 3,
    "GROUP": 4,
    "RETURN_BUS": 5,
    "MASTER": 6
}



# Method to make talking to the device less annoying
# All the messages the device is expecting have a structure of "BF XX XX"
# The STATUS byte always stays the same and only the DATA1 and DATA2 vary
def dataOut(data1: int or hex, data2: int or hex):
    """ Function for easing the communication with the device. By just entering the DATA1 and DATA2 bytes of the MIDI message that has to be sent to the device, it 
    composes the full message in order to satisfy the syntax required by the midiOutSysex method, 
    as well as setting the STATUS of the message to BF as expected and sends the message. 
    
    data1, data2 -- Corresponding bytes of the MIDI message."""
    
    # Composes the MIDI message and sends it
    device.midiOutSysex(bytes([240, 191, data1, data2, 247]))

# Method to enable the deep integration features on the device
def handShake():
    """ Acknowledges the device that a compatible host has been launched, wakes it up from MIDI mode and activates the deep
    integration features of the device. TODO: Then waits for the answer of the device in order to confirm if the handshake 
    was successful and returns True if affirmative."""

    # Sends the MIDI message that initiates the handshake: BF 01 01
    dataOut(1, 3)

    # TODO: Waits and reads the handshake confirmation message
   

# Method to deactivate the deep integration mode. Intended to be executed on close.
def goodBye():
    """ Sends the goodbye message to the device and exits it from deep integration mode. 
    Intended to be executed before FL Studio closes."""

    # Sends the goodbye message: BF 02 01
    dataOut(2, 1)


# Method for restarting the protocol on demand. Intended to be used by the end user in case the keyboard behaves 
# unexpectedly.
def restartProtocol():
    """ Sends the goodbye message to then send the handshake message again. """

    # Turns off the deep integration mode
    goodBye()

    # Then activates it again
    handShake()

    
# Method for controlling the lighting on the buttons (for those who have idle/highlighted two state lights)
# Examples of this kind of buttons are the PLAY or REC buttons, where the PLAY button alternates between low and high light and so on.
# SHIFT buttons are also included in this range of buttons, but instead of low/high light they alternate between on/off light states.
def buttonSetLight(buttonName: str, lightMode: int):
    """ Method for controlling the lights on the buttons of the device. 
    
    ### Parameters

     - buttonName: Name of the button as shown in the device in caps and enclosed in quotes. ("PLAY", "AUTO", "REDO"...)
        - EXCEPTION: declare the Count-In button as COUNT_IN
    
     - lightMode: If set to 0, sets the first light mode of the button. If set to 1, sets the second light mode."""

    #Light mode integer to light mode hex dictionary
    lightModes = {
        0: 0,
        1: 1,

        # For setting lights on of the right and down dot lights of the 4D Encoder on S-Series devices
        127: 127
    }

    # Then sends the MIDI message using dataOut
    dataOut(buttons.get(buttonName), lightModes.get(lightMode))



# Method for reporting information about the mixer tracks, which is done through SysEx
# Couldn't make this one as two different functions under the same name since Python doesn't admit function overloading
def mixerSendInfo(info_type: str, trackID: int, **kwargs):
    """ Sends info about the mixer tracks to the device.
    
    ### Parameters

     - info_type: The kind of information you're going to send as defined on `mixerinfo_types`. ("VOLUME", "PAN"...)
         - Note: If declared as `"EXIST"`, you can also declare the track type on the `value` argument as a string (values are contained in `track_types` dictionary).
    
     - trackID: From 0 to 7. Tells the device which track from the ones that are showing up in the screen you're going to tell info about.

    The third (and last) argument depends on what kind of information you are going to send:

     - value (integer): Can be 0 (no) or 1 (yes). Used for two-state properties like to tell if the track is solo-ed or not (except `"EXIST"`).

     - info: Used for track name, track pan, track volume and the Komplete Kontrol instance ID.

     - peakValues: For peak values. They can be neither integers or floats, and they will get reformated automatically. You can
    also use the `mixer.getTrackPeaks` function directly to fill the argument, but remember you have to specify the left and the right channel separately. You have to 
    report them as a list of values: `peak=[peakL_0, peakR_0, peakL_1, peakR_1 ...]`
    """

    # Gets the inputed values for the optional arguments from **kwargs
    value = kwargs.get("value", 0)
    info = kwargs.get("info", None)

    peakValues = kwargs.get("peakValues", None)

    # Compatibility behaviour for older implementations of the layer before the addition of track_types
    # This will retrieve the correct value in case the developer used the string based declaration
    if type(value) == str:
        value = track_types.get(value, 0)


    # Defines the behaviour for when additional info is reported (for track name, track pan, track volume and peak values)
    if info != None:
        # Tells Python that the additional_info argument is in UTF-8
        info = info.encode("UTF-8")

        # Converts the text string to a list of Unicode values
        info = list(bytes(info))
        
        # Conforms the kind of message midiOutSysex is waiting for
        msg = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type), value, trackID] + info + [247]

        # Warps the data and sends it to the device
        device.midiOutSysex(bytes(msg))

    # For peak values
    # Takes each value from the dictionary and rounds it in order to avoid conflicts with hexadecimals only being "compatible" with integer numbers 
    # in case peak values are specified
    elif peakValues != None:
            
        for x in range(0, 16):
            # Makes the max of the peak meter on the device match the one on FL Studio (values that FL Studio gives seem to be infinite)
            if peakValues[x] >= 1.1:
                peakValues[x] = 1.1
        
            # Translates the 0-1.1 range to 0-127 range
            peakValues[x] = peakValues[x] * (127 / 1.1)
        
            # Truncates the possible decimals and declares the number as an integer to avoid errors in the translation of the data
            peakValues[x] = int(math.trunc(peakValues[x]))

        # Conforms the kind of message midiOutSysex is waiting for
        msg = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type), 2, trackID] + peakValues + [247]

        # Warps the data and sends it to the device
        device.midiOutSysex(bytes(msg))

    # Defines how the method should work normally
    elif info == None:
        
        # Takes the information and wraps it on how it should be sent and sends the message
        device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type), value, trackID, 247]))


# Method for changing the locations of the pan and volume arrows on the screen of S-Series devices to graphically show where the pan and volume faders are
def mixerSetGraph(trackID: int, graph: str, location: float):
    """ Method for changing the locations of the pan and volume arrows on the screen of S-Series devices to graphically show where the pan and volume faders are.
    ### Parameters
    
     - trackID: From 0 to 7, the track whose the graph you want to update belongs to.
     - graph: The graph you are going to change. Can be VOLUME or PAN.
     - location: Can be filled using `mixer.getTrackVolume()` and `mixer.getTrackPan()`.
         - `graph = "VOLUME"`: From 0  to 1.
         - `graph = "PAN"`: From -1 to 1.
    """
    # Gets the right data1 value depending on the graph that has to be updated
    if graph == "VOLUME":
        graphValue = mixerinfo_types.get("VOLUME_GRAPH")
    
    elif graph == "PAN":
        graphValue = mixerinfo_types.get("PAN_GRAPH")
    
    # Adapts the given location value to MIDI values depending on the graph that is going to be updated
    if graph == "VOLUME":
        # Translates the 0-1 range to 0-127 range
        location = location * 127
    
    elif graph == "PAN":
        # Translates the -1 to 1 range to 0-127 range
        if location < 0:  # If the pan is negative, for hence is set to the left
            location = abs(location)    # Gets the absolute value of the location
            location = 64 - location * 64
        
        elif location == 0: # If the pan is negative, for hence is set to the center
            location = 64
        
        elif location > 0:  # If the pan is positive, for hence is set to the right
            location = 64 + location * 63
    

    # Truncates the possible decimals and declares the number as an integer to avoid errors in the translation of the data
    location = int(math.trunc(location))

    # Reports the change of the desired graph to the device
    dataOut(graphValue + trackID, location)
    

def mixerSendInfoSelected(info_type: str, info: str):
    """ Makes the device report MIDI messages for volume and pan adjusting for the selected track when exsitance of this track is reported as true.
    ### Parameters
     - info_type: The data you are going to tell about the selected track.
         - SELECTED: If there's a track selected on the mixer or not.
         - MUTE_BY_SOLO: To tell if it's muted by solo.
     - info: The value of the info you are telling.
         - `info_type = SELECTED`: The track type as defined on `track_types`.
         - `info_type = MUTE_BY_SOLO`: Yes or no.
    """
    if info_type == "SELECTED":
        info_type = mixerinfo_types.get("SELECTED_AVAILABLE")

        info = track_types.get(info)
    
    # Not implemented yet in FL Studio
    elif info_type == "MUTE_BY_SOLO":
        info_type = mixerinfo_types.get("SELECTED_MUTE_BY_SOLO")
    

    # Sends the message
    dataOut(info_type, info)