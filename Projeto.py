#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pirc522 import RFID
from Porta import mudaporta
from Portao import mudaportao
from Interfone import mudainterfone
from Variables import *
from threading import Thread



if __name__ == '__main__':
    
    print("Sistema Iniciando")
    
    
    a=mudaportao()
    #b= mudaporta()
    #c=mudainterfone()
    

    a.start()
    #b.start()
    #c.start()
        

