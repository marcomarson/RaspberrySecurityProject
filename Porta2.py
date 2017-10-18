#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : Marco Marson
import signal
import time
import sys
import RPi.GPIO as GPIO
from BancoMongoDB import BancoMongoDB
from pirc522 import RFID
import pushbullet
from Variables import *
from threading import Thread
import locale
locale.setlocale(locale.LC_ALL, 'Portuguese')
class mudaPorta(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        counter_IR = 0
        counter_RFID= 0
        counter_CFC = 0
        counter_while=True
        while(counter_while):
            try:
                input_state = GPIO.input(35)
                if(input_state == False):
                    if(mudancatexto==True):
                        print("Mudança em andamento")
                        mudancatexto=False

                else:
                    mudancatexto=True
                    (error, data) = rdr2.request()
                    if not error:
                        print("\nRfid detectado: " + format(data, "02x"))

                    (error, uid) = rdr2.anticoll()
                    if not error:
                        if( uid == rfid1):
                            print("Acesso permitido - Isabel ( Ap12 ),RFID com UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                        elif(uid == rfid2):
                            print("Acesso permitido - Rogério ( Ap30), RFID com UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                        print ("Sistema Porta")

                        GPIO.output(33, 1) # aciona sistema relé por 1 segundo
                        time.sleep(1)
                        GPIO.output(33,0) # desativa sistema relé por 1 segundo
                        dataabertura= time.strftime("%d %b %Y %H:%M:%S")
                        counter_while=False;


            except KeyboardInterrupt:
                GPIO.cleanup()
                   # clean up GPIO on CTRL+C exit
        try:
            GPIO.wait_for_edge(36, GPIO.RISING)
            print "Infravermelho detectado"
            print "Esperando sinal chave fim de curso "
            GPIO.wait_for_edge(32, GPIO.RISING)
            print("Processo finalizado")
            run()
        except KeyboardInterrupt:
            GPIO.cleanup()
