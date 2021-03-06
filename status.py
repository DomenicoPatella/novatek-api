#!/usr/bin/env python
import os
import subprocess
import sys
import time


try:
  ok_models = [
    'Raspberry Pi 3 Model B Rev 1.2\0',
  ]
  with open('/sys/firmware/devicetree/base/model') as f:
    assert f.read() in ok_models
except:
    raise RuntimeError(
      '''
      This module is ONLY for the Raspberry Pi 3 Model B! You can comment out
      this error if you think it will work on your device; if it does, please
      send me a note, but if it doesn't, I can't help, sorry.
      '''
    )


abyss = open(os.devnull, 'w')

def led_control(flag):
  '''This function is specific to the Raspberry Pi 3B!'''
  subprocess.check_call(
    ['/opt/vc/bin/vcmailbox', '0x00038041', '8', '8', '130', flag],
    stdout=abyss
  )

def led_on():
  led_control(flag='1')

def led_off():
  led_control(flag='0')

def get_network():
  return subprocess.check_output(['iwgetid', '-r']).rstrip()

def blink(duration=1.0, after=0.0, repeat=1, between=1.0):
  for i in range(repeat):
    led_on()
    time.sleep(duration)
    led_off()
    time.sleep(between if i < repeat - 1 else after)

def blink_yes(after=1.0):
  blink(repeat=3, duration=0.125, between=0.125, after=after)

def blink_no(after=1.0):
  blink(repeat=3, duration=0.25, between=0.25, after=after)


def report_status(healthy=True):
  for _ in range(3):
    blink(repeat=2, duration=0.25, between=0.25, after=1.0)

    if get_network() == 'SakuraCam':
      blink_yes()
    else:
      blink_no()
  
    if healthy:
      blink_yes()
    else:
      blink_no()


if __name__ == '__main__':
  report_status(healthy=sys.argv[1] == '1')
