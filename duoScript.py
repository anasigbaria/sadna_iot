#!/usr/bin/python
# Ensure PyUserInput is installed
# Ensure Duo is running full screen and audio sources are set

from pymouse import PyMouse
from pykeyboard import PyKeyboard
from time import sleep





def main():
    sleep(3)
    m = PyMouse()
    k = PyKeyboard()
    m.click(470,540) # Click in the Duo text box
    sleep(0.5)
    k.tap_key('BackSpace',n=6,interval=0.05) # Delete existing characters
    sleep(0.5)
    k.type_string("Omar") # Type name of Duo contact
    sleep(0.2)
    k.tap_key('Return') # Hit Return to select contact
    sleep(1.5)
    m.click(750,650) # Click on Video Call button












if __name__ == "__main__":
    main()
  # main(sys.argv[1:])
