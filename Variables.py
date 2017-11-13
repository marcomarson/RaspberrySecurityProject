#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import time
import sys
import RPi.GPIO as GPIO
import timeit
from pirc522 import RFID
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
rdr = RFID()
rdr2 = RFID(0,1, pin_rst=16, pin_irq=15)
util1 = rdr.util()
util1.debug = True
util = rdr2.util()
util.debug = True

rfid1=[166,2,217,160,221]
rfid2=[54,109,54,94,51]

GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_UP) #IR 1
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_UP) #CFC 1
GPIO.setup(36,GPIO.IN, pull_up_down=GPIO.PUD_UP) # IR 2
GPIO.setup(32,GPIO.IN, pull_up_down=GPIO.PUD_UP) #CHFC 2
GPIO.setup(31,GPIO.OUT) #relé portão
GPIO.setup(33,GPIO.OUT) # relé porta
GPIO.setup(35,GPIO.IN, pull_up_down=GPIO.PUD_UP) ##Botão mudança
GPIO.setup(37,GPIO.IN, pull_up_down=GPIO.PUD_UP) ##Botão mudança
GPIO.setup(40,GPIO.IN, pull_up_down=GPIO.PUD_UP) ##Botão mudança
def end_read(signal,frame):
    global run
    print("\nCtrl+C encontrado, processo finalizado.")
    run = False
    rdr.cleanup()
    rdr2.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)
mudancatexto=True
