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


###########################################################################################################################################
# Test tools
###########################################################################################################################################

test = ""
    
def OnInit():
        handShake()


def OnMidiIn(event):
    if test == "input":

        # Play button
        if event.data1 == buttons.get("PLAY"):
            print("PLAY button pressed.")

        # Restart button
        if event.data1 == buttons.get("RESTART"):
            print("RESTART button pressed.")

        # Record button
        if event.data1 == buttons.get("REC"):
            print("REC button pressed.")
        
        # Count-In button
        if event.data1 == buttons.get("COUNT_IN"):
            print("COUNT_IN button pressed.")

        # Stop button
        if event.data1 == buttons.get("STOP"):
            print("STOP button pressed.")

        # Clear button
        if event.data1 == buttons.get("CLEAR"):
            print("CLEAR button pressed.")
        
        # Loop button
        if event.data1 == buttons.get("LOOP"):
            print("LOOP button pressed.")

        # Metronome button
        if event.data1 == buttons.get("METRO"):
            print("METRO button pressed.")
        
        # Tempo button
        if event.data1 == buttons.get("TEMPO"):
            print("TEMPO button pressed.")

        # Undo button
        if event.data1 == buttons.get("UNDO"):
            print("UNDO button pressed.")
        
        # Redo button
        if event.data1 == buttons.get("REDO"):
            print("REDO button pressed.")

        # Quantize button
        if event.data1 == buttons.get("QUANTIZE"):
            print("QUANTIZE button pressed.")

        # Automation button
        if event.data1 == buttons.get("AUTO"):
            print("AUTO button pressed.")

        # Mute button
        if event.data1 == buttons.get("MUTE"):
            print("MUTE button pressed.")

        # Solo button
        if event.data1 == buttons.get("SOLO"):
            print("SOLO button pressed.")

        # 4D Encoder +
        if event.data1 == buttons.get("ENCODER_PLUS")[0] and event.data2 == buttons.get("ENCODER_PLUS")[1]:
            print("ENCODER [+] pressed.")

        # 4D Encoder -
        if event.data1 == buttons.get("ENCODER_MINUS")[0] and event.data2 == buttons.get("ENCODER_MINUS")[1]:
            print("ENCODER [-] pressed.")
        
        # 4D Encoder up
        if event.data1 == buttons.get("ENCODER_UP")[0] and event.data2 == buttons.get("ENCODER_UP")[1]:
            print("ENCODER UP pressed.")
        
        # 4D Encoder down 
        if event.data1 == buttons.get("ENCODER_DOWN")[0] and event.data2 == buttons.get("ENCODER_DOWN")[1]:
            print("ENCODER DOWN pressed.")
        
        # 4D Encoder left
        if event.data1 == buttons.get("ENCODER_LEFT")[0] and event.data2 == buttons.get("ENCODER_LEFT")[1]:
            print("ENCODER LEFT pressed.")
        
        # 4D Encoder right
        if event.data1 == buttons.get("ENCODER_RIGHT")[0] and event.data2 == buttons.get("ENCODER_RIGHT")[1]:
            print("ENCODER RIGHT pressed.")

        # 4D Encoder buttons
        if event.data1 == buttons.get("ENCODER_BUTTON"):
            print("ENCODER BUTTON pressed.")


        # Knobs
        if event.data1 == knobs.get("KNOB_1A_PLUS")[0] and event.data2 == knobs.get("KNOB_1A_PLUS")[1]:
            print("KNOB 1 [+] pressed.")

        if event.data1 == knobs.get("KNOB_1A_MINUS")[0] and event.data2 == knobs.get("KNOB_1A_MINUS")[1]:
            print("KNOB 1 [-] pressed.")

        if event.data1 == knobs.get("KNOB_2A_PLUS")[0] and event.data2 == knobs.get("KNOB_2A_PLUS")[1]:
            print("KNOB 2 [+] pressed.")

        if event.data1 == knobs.get("KNOB_2A_MINUS")[0] and event.data2 == knobs.get("KNOB_2A_MINUS")[1]:
            print("KNOB 2 [-] pressed.")

        if event.data1 == knobs.get("KNOB_3A_PLUS")[0] and event.data2 == knobs.get("KNOB_3A_PLUS")[1]:
            print("KNOB 3 [+] pressed.")

        if event.data1 == knobs.get("KNOB_3A_MINUS")[0] and event.data2 == knobs.get("KNOB_3A_MINUS")[1]:
            print("KNOB 3 [-] pressed.")

        if event.data1 == knobs.get("KNOB_4A_PLUS")[0] and event.data2 == knobs.get("KNOB_4A_PLUS")[1]:
            print("KNOB 4 [+] pressed.")
        
        if event.data1 == knobs.get("KNOB_4A_MINUS")[0] and event.data2 == knobs.get("KNOB_4A_MINUS")[1]:
            print("KNOB 4 [-] pressed.")

        if event.data1 == knobs.get("KNOB_5A_PLUS")[0] and event.data2 == knobs.get("KNOB_5A_PLUS")[1]:
            print("KNOB 5 [+] pressed.")

        if event.data1 == knobs.get("KNOB_5A_MINUS")[0] and event.data2 == knobs.get("KNOB_5A_MINUS")[1]:
            print("KNOB 5 [-] pressed.")

        if event.data1 == knobs.get("KNOB_6A_PLUS")[0] and event.data2 == knobs.get("KNOB_6A_PLUS")[1]:
            print("KNOB 6 [+] pressed.")

        if event.data1 == knobs.get("KNOB_6A_MINUS")[0] and event.data2 == knobs.get("KNOB_6A_MINUS")[1]:
            print("KNOB 6 [-] pressed.")

        if event.data1 == knobs.get("KNOB_7A_PLUS")[0] and event.data2 == knobs.get("KNOB_7A_PLUS")[1]:
            print("KNOB 7 [+] pressed.")

        if event.data1 == knobs.get("KNOB_7A_MINUS")[0] and event.data2 == knobs.get("KNOB_7A_MINUS")[1]:
            print("KNOB 7 [-] pressed.")

        if event.data1 == knobs.get("KNOB_8A_PLUS")[0] and event.data2 == knobs.get("KNOB_8A_PLUS")[1]:
            print("KNOB 8 [+] pressed.")

        if event.data1 == knobs.get("KNOB_8A_MINUS")[0] and event.data2 == knobs.get("KNOB_8A_MINUS")[1]:
            print("KNOB 8 [-] pressed.")
        

        
        if event.data1 == knobs.get("KNOB_1B_PLUS")[0] and event.data2 == knobs.get("KNOB_1B_PLUS")[1]:
            print("SHIFT + KNOB 1 [+] pressed.")

        if event.data1 == knobs.get("KNOB_1B_MINUS")[0] and event.data2 == knobs.get("KNOB_1B_MINUS")[1]:
            print("SHIFT + KNOB 1 [-] pressed.")

        if event.data1 == knobs.get("KNOB_2B_PLUS")[0] and event.data2 == knobs.get("KNOB_2B_PLUS")[1]:
            print("SHIFT + KNOB 2 [+] pressed.")

        if event.data1 == knobs.get("KNOB_2B_MINUS")[0] and event.data2 == knobs.get("KNOB_2B_MINUS")[1]:
            print("SHIFT + KNOB 2 [-] pressed.")

        if event.data1 == knobs.get("KNOB_3B_PLUS")[0] and event.data2 == knobs.get("KNOB_3B_PLUS")[1]:
            print("SHIFT + KNOB 3 [+] pressed.")

        if event.data1 == knobs.get("KNOB_3B_MINUS")[0] and event.data2 == knobs.get("KNOB_3B_MINUS")[1]:
            print("SHIFT + KNOB 3 [-] pressed.")

        if event.data1 == knobs.get("KNOB_4B_PLUS")[0] and event.data2 == knobs.get("KNOB_4B_PLUS")[1]:
            print("SHIFT + KNOB 4 [+] pressed.")
        
        if event.data1 == knobs.get("KNOB_4B_MINUS")[0] and event.data2 == knobs.get("KNOB_4B_MINUS")[1]:
            print("SHIFT + KNOB 4 [-] pressed.")

        if event.data1 == knobs.get("KNOB_5B_PLUS")[0] and event.data2 == knobs.get("KNOB_5B_PLUS")[1]:
            print("SHIFT + KNOB 5 [+] pressed.")

        if event.data1 == knobs.get("KNOB_5B_MINUS")[0] and event.data2 == knobs.get("KNOB_5B_MINUS")[1]:
            print("SHIFT + KNOB 5 [-] pressed.")

        if event.data1 == knobs.get("KNOB_6B_PLUS")[0] and event.data2 == knobs.get("KNOB_6B_PLUS")[1]:
            print("SHIFT + KNOB 6 [+] pressed.")

        if event.data1 == knobs.get("KNOB_6B_MINUS")[0] and event.data2 == knobs.get("KNOB_6B_MINUS")[1]:
            print("SHIFT + KNOB 6 [-] pressed.")

        if event.data1 == knobs.get("KNOB_7B_PLUS")[0] and event.data2 == knobs.get("KNOB_7B_PLUS")[1]:
            print("SHIFT + KNOB 7 [+] pressed.")

        if event.data1 == knobs.get("KNOB_7B_MINUS")[0] and event.data2 == knobs.get("KNOB_7B_MINUS")[1]:
            print("SHIFT + KNOB 7 [-] pressed.")

        if event.data1 == knobs.get("KNOB_8B_PLUS")[0] and event.data2 == knobs.get("KNOB_8B_PLUS")[1]:
            print("SHIFT + KNOB 8 [+] pressed.")

        if event.data1 == knobs.get("KNOB_8B_MINUS")[0] and event.data2 == knobs.get("KNOB_8B_MINUS")[1]:
            print("SHIFT + KNOB 8 [-] pressed.")


def OnDeInit():
    goodBye()
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

    "ENCODER_BUTTON": 96,
    "ENCODER_BUTTON_SHIFTED": 97,
    
    # The 4D encoder events use the same data1, but different data2
    # For example, if you want to retrieve the data1 value for ENCODER_PLUS you would do nihia.buttons.get("ENCODER_PLUS")[0]
    "ENCODER_RIGHT": [50, 1],
    "ENCODER_LEFT": [50, 127],
    
    "ENCODER_UP": [48, 127],
    "ENCODER_DOWN": [48, 1],

    "ENCODER_PLUS": [52, 1],
    "ENCODER_MINUS": [52, 127]
}


# Knob to knob ID dictionary
# The number in the name of the knob refers to the physical knob in the device from left to right
# The letter at the end represents whether the knob is being shifted or not
# Example:
#   KNOB_1A --> First knob without shift. It is meant to adjust volume
#   KNOB_1B --> First knob shifted (SHIFT button is being held down while using the knob). It is meant to adjust panning
knobs = {
    "KNOB_1A": 80,
    "KNOB_2A": 81,
    "KNOB_3A": 82,
    "KNOB_4A": 83,
    "KNOB_5A": 84,
    "KNOB_6A": 85,
    "KNOB_7A": 86,
    "KNOB_8A": 87,
    
    "KNOB_1B": 88,
    "KNOB_2B": 89,
    "KNOB_3B": 90,
    "KNOB_4B": 91,
    "KNOB_5B": 92,
    "KNOB_6B": 93,
    "KNOB_7B": 94,
    "KNOB_8B": 95,

    "INCREASE": 1,
    "DECREASE": 127

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
    dataOut(1, 1)

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
        1: 1
    }

    # Then sends the MIDI message using dataOut
    dataOut(buttons.get(buttonName), lightModes.get(lightMode))


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
    "EXIST": 64,
    "SELECTED": 66,

    # This one only will make an effect on devices with full feature support, like the S-Series MK2 and it's used to send the peak meter information
    "PEAK": 73
}


# Method for reporting information about the mixer tracks, which is done through SysEx
# Couldn't make this one as two different functions under the same name since Python doesn't admit function overloading
def mixerSendInfo(info_type: str, trackID: int, **kwargs):
    """ Sends info about the mixer tracks to the device.
    
    ### Parameters

     - info_type: The kind of information you're going to send. ("VOLUME", "PAN"...) Defined on `nihia.mixerinfo_types`
    
     - trackID: From 0 to 7. Tells the device which track from the ones that are showing up in the screen you're going to tell info about.

    The third (and last) argument depends on what kind of information you are going to send:

     - value (integer): Can be 0 (no) or 1 (yes). Used for two-state properties like to tell if the track is solo-ed or not.

    or

     - info: Used for track name, track pan, track volume and peak values.
        - For peak values: Report them as `info=[LEFT_PEAK, RIGHT_PEAK]`. They can be neither integers or floats, and they will get reformated automatically. You can
        also use the `mixer.getTrackPeaks` function directly to fill the argument, but remember you have to specify the left and the right channel separately.
        - For everything else: Report the info as `info=TEXT_STRING`.
    """

    # Gets the inputed values for the optional arguments from **kwargs
    value = kwargs.get("value", 0)
    info = kwargs.get("info", None)

    # Defines the behaviour for when additional info is reported (for track name, track pan, track volume and peak values)
    if info != None:

        # Bifurcation of behaviour to stablish the different treatment(s) that certain type of data has to recieve before being sent to the device
        
        # For peak values
        # Takes each value from the dictionary and rounds it in order to avoid conflicts with hexadecimals only being "compatible" with integer numbers 
        # in case peak values are specified
        if info_type == "PEAK":
            
            # Makes the max of the peak meter on the device match the one on FL Studio (values that FL Studio gives seem to be infinite)
            if info[0] >= 1.1:
                info[0] = 1.1
            
            if info[1] >= 1.1:
                info[1] = 1.1
            
            # Translates the 0-1.1 range to 0-127 range
            info[0] = info[0] * (127 / 1.1)
            info[1] = info[1] * (127 / 1.1)
            
            # Truncates the possible decimals and declares the number as an integer to avoid errors in the translation of the data
            info[0] = round(info[0])    # Left peak
            info[1] = round(info[1])    # Right peak
            

        # For string-based data
        else:
            # Tells Python that the additional_info argument is in UTF-8
            info = info.encode("UTF-8")

            # Converts the text string to a list of Unicode values
            info = list(bytes(info))
        
        # Conforms the kind of message midiOutSysex is waiting for
        msg = [240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type), value, trackID] + info + [247]

        # Warps the data and sends it to the device
        device.midiOutSysex(bytes(msg))

    # Defines how the method should work normally
    else:
        
        # Takes the information and wraps it on how it should be sent and sends the message
        device.midiOutSysex(bytes([240, 0, 33, 9, 0, 0, 68, 67, 1, 0, mixerinfo_types.get(info_type), value, trackID, 247]))
