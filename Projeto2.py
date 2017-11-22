#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pirc522 import RFID
from Portao2 import *
from multiprocessing import Process



if __name__ == '__main__':

    print("Sistema Iniciando")
    run=1
    p2 = Process(target=run())
    p2.start()
    p2.join()
