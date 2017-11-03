#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pirc522 import RFID
from Porta2 import *
from Portao2 import *
from Interfone import mudainterfone
from multiprocessing import Process



if __name__ == '__main__':

    print("Sistema Iniciando")
    p1 = Process(target=runPorta())
    p1.start()
    p2 = Process(target=run())
    p2.start()
    p1.join()
    p2.join()
