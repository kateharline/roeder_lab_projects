
import sys
import Tkinter

for p in sys.path:
    print(p)

if not hasattr(sys, 'argv'):
    sys.argv  = ['']

Tkinter._test()
