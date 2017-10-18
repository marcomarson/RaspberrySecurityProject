#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
import time
import sys
import RPi.GPIO as GPIO
from BancoMongoDB import BancoMongoDB
import timeit
from pirc522 import RFID
import pushbullet
from Variables import *
from threading import Thread
class mudaporta(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):

        while run:
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
                    GPIO.output(33, 1) ## Acionar circuito relé
                    time.sleep(2)
                    GPIO.output(33,0)## Desativar circuito relé
                    dataabertura= time.asctime(time.localtime(time.time()))
                    x=True
                    x1=True
                    while x:

                        input_state = GPIO.input(36)
                        if input_state == False:
                            print("Sensor IR acionado")
                            inicio = timeit.default_timer()

                            while x1:

                                fim= timeit.default_timer()

                                #print(int(fim-inicio))
                                input_state = GPIO.input(32)
                                if input_state == False:
                                    print("Chave fim de curso acionada")
                                    datafecha = time.asctime(time.localtime(time.time()))
                                    #print("Enviando informações para o banco de dados")
                                    #bid=bancodedados.insertporta(str(uid),dataabertura,datafecha, int(fim-inicio))
                                    #print(bid)
                                    print("Processo finalizado")

                                    break
                            break
