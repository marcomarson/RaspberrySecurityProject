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
class mudainterfone(Thread):
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
                finaliza=True
                mudancatexto=True
                input_state = GPIO.input(37)
                input_state2 = GPIO.input(40)
                if(input_state == False or input_state2 == False):
                    
                    #variavel p/ enviar email
                    enviamail=0

                    #verificar botao interfone
                    print("Botão Interfone - Entrada")
                    GPIO.output(31, 1)
                    GPIO.output(33, 1)
                    time.sleep(3)
                    GPIO.output(31,0)##acionar circuito relé
                    GPIO.output(33,0)##acionar circuito relé
                    dataaberturaporta= time.asctime(time.localtime(time.time()))
                    dataaberturaportao=dataaberturaporta
                    x=True
                    x1=True
                    x2=True
                    x3=True
                    contafoto=1
                    while x:
                                
                        input_state = GPIO.input(13)
                        if input_state == False:
                            print("Sensor IR acionado - Entrada pelo interfone")
                            contafoto=1
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
                                    print "Portao aberto por muito tempo"
                                    title= "Portão aberto por muito tempo"
                                    body="Teste"
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
                                    bid=bancodedados.insert(xT,rfid1,dataaberturaportao,datafecha, int(fim-inicio))
                                    print(bid)
                                    print("Processo portao finalizado, inicio porta")
                                    while x2:
                                
                                        input_state = GPIO.input(36)
                                        if input_state == False:
                                            print("Sensor IR- Porta acionado")
                                            inicio = timeit.default_timer()
                                                
                                            while x3:
                                                    
                                                fim= timeit.default_timer()
                                                    
                                                #print(int(fim-inicio))
                                                input_state = GPIO.input(32)
                                                if input_state == False:
                                                    print("Chave fim de curso acionada")
                                                    datafechaporta = time.asctime(time.localtime(time.time()))
                                                    #print("Enviando informações para o banco de dados")
                                                    #bid=bancodedados.insertporta(str(uid),dataaberturaporta,datafechaporta,int(fim-inicio))
                                                    #print(bid)
                                                    print("Processo finalizado")
                                                    finaliza=False

                                                    break

                                        if finaliza == False:
                                            break
                                if finaliza == False:
                                    break
                        input_state = GPIO.input(36)
                        if input_state == False:
                            print("Sensor IR-Porta acionado, Interfone saída")
                            contafoto=1
                            inicio = timeit.default_timer()
                                               
                            while True:                   
                                fim= timeit.default_timer()
                                                    
                                #print(int(fim-inicio))
                                input_state = GPIO.input(32)
                                if input_state == False:
                                    print("Chave FDC-porta")
                                    datafechaporta = time.asctime(time.localtime(time.time()))
                                    #print("Enviando informações para o banco de dados")
                                    #bid=bancodedados.insertporta(str(uid),dataaberturaports,datafechaporta,int(fim-inicio))
                                    #print(bid)
                                    print("Processo finalizado")
                                    while True:
                                        input_state = GPIO.input(13)
                                        if input_state == False:
                                            print("Sensor IR-portao acionado")
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
                                                    print "Portao aberto por muito tempo"
                                                    title= "Portão aberto por muito tempo"
                                                    body="Teste"
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
                                                    bid=bancodedados.insert(xT,rfid1,dataaberturaportao,datafecha, int(fim-inicio))
                                                    print(bid)
                                                    print("Processo interfone saída realizado")
                                                    finaliza=False  
                                                    break
                                                
                                        if finaliza == False:
                                            break
                                if finaliza == False:
                                    break
                        if finaliza == False:
                            break
