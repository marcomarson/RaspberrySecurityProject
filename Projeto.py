#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pirc522 import RFID
from Porta2 import mudaPorta
from Portao2 import mudaPortao
from Interfone import mudainterfone
from Variables import *
from multiprocessing import Process



if __name__ == '__main__':

    print("Sistema Iniciando")
    processPorta = mudaPorta()
    processPortao = mudaPortao()
    p1 = Process(target=processPorta.run())
    p1.start()
    p2 = Process(target=processPortao.run())
    p2.start()
    p1.join()
    p2.join()
