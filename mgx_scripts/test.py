
import sys

for p in sys.path:
    print(p)

if not hasattr(sys, 'argv'):
    sys.argv  = ['']

import Tkinter

Tkinter._test()
