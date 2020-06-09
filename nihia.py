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

import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist

import midi
import utils


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

    "DPAD_X": 50,
    "DPAD_Y": 48
}


# Method to make talking to the device less annoying
# All the messages the device is expecting have a structure of "BF XX XX"
# The STATUS byte always stays the same and only the DATA1 and DATA2 vary
def dataOut(data1, data2):
    """ Function for easing the communication with the device. By just entering the DATA1 and DATA2 bytes of the MIDI message that has to be sent to the device, it 
    composes the full message in order to satisfy the syntax required by the midiOutSysex method, 
    as well as setting the STATUS of the message to BF as expected and sends the message. 
    
    data1, data2 -- Corresponding bytes of the MIDI message in hex format."""
    
    # Composes the MIDI message and sends it
    device.midiOutSysex(bytes([240, 191, data1, data2, 247]))

# Method to enable the deep integration features on the device
def handShake():
    """ Acknowledges the device that a compatible host has been launched, wakes it up from MIDI mode and activates the deep
    integration features of the device. TODO: Then waits for the answer of the device in order to confirm if the handshake 
    was successful and returns True if affirmative."""

    # Sends the MIDI message that initiates the handshake: BF 01 01
    dataOut(1, 1)

    # TODO: Waits and reads the handshake confirmation message
   

# Method to deactivate the deep integration mode. Intended to be executed on close.
def goodBye():
    """ Sends the goodbye message to the device and exits it from deep integration mode. 
    Intended to be executed before FL Studio closes."""

    # Sends the goodbye message: BF 02 01
    dataOut(0x02, 1)


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
def buttonSetLight(buttonName, lightMode):
    """ Method for controlling the lights on the buttons of the device. 
    
    buttonName -- Name of the button as shown in the device in caps and enclosed in quotes. ("PLAY", "AUTO", "REDO"...)

    EXCEPTION: declare the Count-In button as COUNT_IN
    
    lightMode -- If set to 0, sets the first light mode of the button. If set to 1, sets the second light mode."""

    #Light mode integer to light mode hex dictionary
    lightModes = {
        0: 0,
        1: 1
    }

    # Then sends the MIDI message using dataOut
    dataOut(buttons.get(buttonName, ""), lightModes.get(lightMode, ""))


# Dictionary that goes between the different kinds of information that can be sent to the device to specify information about the mixer tracks
# and their corresponding identificative bytes
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
    "EXIST": 64
}


# Method for reporting information about the mixer tracks
# Couldn't make this one as two different functions under the same name since Python doesn't admit function overloading
def mixerInfo(info_type: str, trackID: int, **kwargs: int or str):
    """ Sends info about the mixer tracks to the device.
    
    info_type -- The kind of information you're going to send. ("VOLUME", "PAN"...)
    
    trackID -- From 0 to 0x07. Tells the device which track from the ones that are showing up in the mixer you're going to tell info about.

    value -- Can be 0 (no) or 1 (yes). Used for two-state properties like to tell if the track is solo-ed or not.
    
    info -- Used for track name, track pan and track volume.
    """

    #Gets the inputed values for the optional arguments from **kwargs
    value = kwargs.get("value", 0)
    info = kwargs.get("info", None)

    # Defines the behaviour for when additional info is reported (for track name, track pan and track volume)
    if info != None:

        # Tells Python that the additional_info argument is in UTF-8
        info = info.encode("UTF-8")
        
        # Conforms the kind of message midiOutSysex is waiting for
        msg = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type, 0), value, trackID] + list(bytes(info)) + [247]

        # Warps the data and sends it to the device
        device.midiOutSysex(bytes(msg))

    # Defines how the method should work normally
    else:
        
        # Takes the information and wraps it on how it should be sent and sends the message
        device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type, 0), value, trackID, 247]))