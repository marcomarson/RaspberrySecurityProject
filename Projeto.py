#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pirc522 import RFID
from Porta2 import *
from multiprocessing import Process



if __name__ == '__main__':

    print("Sistema Iniciando")
    run=1
    p1 = Process(target=runPorta(run))
    p1.start()
    p1.join()
