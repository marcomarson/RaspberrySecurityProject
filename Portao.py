#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
import time
import sys
import RPi.GPIO as GPIO
from BancoMongoDB import BancoMongoDB
from Camera import Camera
import timeit
from pirc522 import RFID
import pushbullet
from Variables import *
from threading import Thread
class mudaportao(Thread):
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
                #variavel p/ enviar email
                enviamail=0
                    
                (error, data) = rdr.request()
                if not error:
                    print("\nRFID detectado: " + format(data, "02x"))

                (error, uid) = rdr.anticoll()
                if not error:
                    if( uid == rfid1):
                        print("Acesso permitido - Isabel ( Ap12 ),RFID com UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                    elif(uid == rfid2):
                        print("Acesso permitido - Rogério ( Ap30), RFID com UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

                    print("Portão")
                    GPIO.output(31, 1)
                    time.sleep(3)
                    GPIO.output(31,0)##acionar circuito relé
                    dataabertura= time.asctime(time.localtime(time.time()))
                    x=True
                    x1=True
                    contafoto=1
                    while x:
                            
                        input_state = GPIO.input(13)
                        if input_state == False:
                            print("Sensor IR acionado")
                            inicio = timeit.default_timer()
                            iniciofoto = timeit.default_timer()
                                
                            while x1:
                                    
                                fim= timeit.default_timer()
                                fimfoto= timeit.default_timer()
                                #print(int(fim-inicio))
                                if((contafoto==1 or int(fimfoto-iniciofoto) >30)):
                                    camera=Camera()
                                    try:
                                        
                                        
                                        nomefoto='imagem'+str(contafoto)+'.jpg'
                                        print (nomefoto)
                                        camera.tirafoto(nomefoto)
                                        contafoto=contafoto+1
                                        iniciofoto = timeit.default_timer()
                                        fimfoto= timeit.default_timer()
                                    finally:
                                        camera.fecha()
                                if(fim-inicio > 30 and enviamail==0):
                                    enviamail=1
                                    #envia email
                                    title= "Portão aberto por muito tempo"
                                    body="Teste"
                                    print("Portão aberto por mto tempo")
                                    #pushbullet.send_notification_via_pushbullet(title,body)
                                input_state = GPIO.input(11)
                                if input_state == False:
                                    print("Chave fim de curso acionada")
                                    datafecha = time.asctime(time.localtime(time.time()))
                                    print("Enviando informações para o banco de dados")
                                    #f= open('/home/pi/projeto/imagem1.jpg', 'r+')
                                    #jpgdata=f.read()
                                    #f.close
                                    xT="Teste"
                                    bid=bancodedados.insert(xT,uid,dataabertura,datafecha, int(fim-inicio))
                                    print(bid)
                                    print("Processo finalizado")

                                    break
                            break
