import RPi.GPIO as GPIO
import time
import threading
import numpy as np
import sounddevice as sd

LR = 3
LB = 5
RR = 8
RB = 10

pins = [LR, LB, RR, RB] # pins = [3,5,7,8,10,12]

GPIO.setmode(GPIO.BOARD) # choose the pin numbering

# initialize pins
for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)

def turn_on_led(pin, seconds):
        # RED
        GPIO.output(pin, 1)
        time.sleep(seconds)
        GPIO.output(pin, 0)
        # BLUE
        GPIO.output(pin+2, 1)
        time.sleep(seconds)
        GPIO.output(pin+2, 0)

def turn_off_led():
        for pin in pins:
                GPIO.output(pin, 0)

def assign_value(value):
      # size
      if value == 'l':
            return 4
      elif value == 'm':
            return 2
        # side
      elif value == 'L':
            return LR 
      elif value == 'R':
            return RR
      else:
            return 

def sound_alarm(size, seconds):
    try:
        # Audio parameters
        sample_rate = 44100  # Standard audio sample rate
        frequency = 440 * assign_value(size)  # A4 note frequency in Hz
        t = np.linspace(0, seconds, int(sample_rate * seconds))
        waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
        with sd.OutputStream(samplerate=sample_rate, channels=1) as stream:
            # Write the waveform to the stream
            stream.write(waveform.astype(np.float32))
            # Wait for the specified duration
            time.sleep(seconds)
      #   sd.play(waveform, sample_rate)
      #   time.sleep(seconds)
      #   sd.stop()
    except Exception as e:
        raise RuntimeError(f"Error playing sound: {str(e)}")
          
# def sound_alarm(size):
#     # Generate a simple sine wave
#     sample_rate = 44100 
#     frequency = 440 * assign_value(size) 
#     t = np.linspace(0, 1, int(sample_rate))
#     waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    
#     # Play the sound
#     sd.play(waveform, sample_rate)
#     sd.wait()

if __name__ == "__main__":

        # alarm example usage:
        sound_alarm('m',1) 
        sound_alarm('l',1) 

        # activate lights
        turn_on_led(LR,0.1)
        # turn_on_led(LB,0.1)
        turn_on_led(RR,0.1)
        # turn_on_led(RB,0.1)

        GPIO.cleanup()


        # Create threads for each function
        # if (LR or RR)
        sound_arg = (2,)
        light_arg = (RR,0.1)

        t1 = threading.Thread(target=sound_alarm, args=sound_arg)
        t2 = threading.Thread(target=turn_on_led, args=light_arg)

        # Start the threads
        t1.start()
        t2.start()

        # Wait for both threads to finish   

        t1.join()
        t2.join()
