#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : Marco Marson
import signal
import time
import sys
import timeit
import RPi.GPIO as GPIO
from BancoMongoDB import BancoMongoDB
from pirc522 import RFID
import pushbullet
from Variables import *
import locale
import os
contapessoas=0
counter_IR = 0
counter_while=True
counter_RFID=0
counter_mudanca=0
counter_interfone=0
dataabertura=0
inicio=0
ap=0

def initializePorta(): #__init__
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') #pt_br.utf-8
    global contapessoas, counter_IR, counter_while, counter_RFID, counter_mudanca, counter_interfone
    GPIO.add_event_detect(36, GPIO.RISING, callback=infraRedPortaPorta, bouncetime=300) # Botão Infravermelho porta
    GPIO.add_event_detect(32, GPIO.BOTH, callback=chaveFimCursoPorta, bouncetime=300) # Botão Chave fim de curso porta
    GPIO.add_event_detect(35, GPIO.BOTH, callback=botaoMudancaPorta, bouncetime=300) # Botão Mudança
    GPIO.add_event_detect(37, GPIO.RISING, callback=interFonePorta, bouncetime=300) #Interfone
    GPIO.add_event_detect(40, GPIO.RISING, callback=interFonePorta, bouncetime=300) #Interfone 2
    #carregar tags RFID do banco

def interFonePorta(channel):
    global ap,dataabertura,inicio,contapessoas, counter_IR, counter_while, counter_RFID, counter_mudanca, counter_interfone
    counter_interfone=1
    print ("Interfone Ligado")
    print ("Abrindo porta")
    dataabertura= time.strftime("%d %b %Y %H:%M:%S")
    inicio = timeit.default_timer()
    GPIO.output(33, 1) # aciona sistema relé por 1 segundo
    time.sleep(1)
    GPIO.output(33,0) # desativa sistema relé por 1 segundo
    if(channel==37):
        ap=1
    elif(channel==40):
        ap=2
    #db=BancoMongoDB()
    #users =db.users
    #login_user = users.find_one({'a' : request.form['username']})
    #if login_user:

def CameraPorta(ap):
    os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --no-timestamp --save /home/pi/PhotosMAM/'+ap+'-%d_%m_%y-%H%M.jpg')


def infraRedPortaPorta(channel):
    global ap,dataabertura,inicio,contapessoas, counter_IR, counter_while, counter_RFID, counter_mudanca, counter_interfone
    if(contapessoas==0):
        if(counter_RFID == 1):
            print ("Infravermelho detectado após RFID")
        else:
            if(counter_interfone ==1):
                print("Infravermelho acionado após interfone")
                CameraPorta(ap) # change version
            else:
                print ("Infravermelho detectado após chave")
                CameraPorta(ap)

def botaoMudancaPorta(channel):
    global contapessoas, counter_IR, counter_while, counter_RFID, counter_mudanca, counter_interfone
    chaveFC = GPIO.input(35)
    if(chaveFC == False):
        counter_mudanca=1
    else:
        counter_mudanca=0

def chaveFimCursoPorta(channel):
    global ap,dataabertura,inicio,contapessoas, counter_IR, counter_while, counter_RFID, counter_mudanca, counter_interfone
    chaveFC = GPIO.input(35)
    if(chaveFC == False):
        input_state = GPIO.input(32)
        if(input_state == False):
            contapessoas=0
            if(counter_RFID==1):
                counter_RFID=0
                datafecha = time.strftime("%d %b %Y %H:%M:%S")
                fim= timeit.default_timer()
                gravaInformacoesPorta(ap,dataabertura,datafecha, int(fim-inicio))
                ap=0
            elif(counter_interfone==1):
                counter_interfone=0
                datafecha = time.strftime("%d %b %Y %H:%M:%S")
                fim= timeit.default_timer()
                gravaInformacoesPorta(ap,dataabertura,datafecha, int(fim-inicio))
                ap=0
            else:
                ap=0
                datafecha = time.strftime("%d %b %Y %H:%M:%S")
                fim= timeit.default_timer()
                gravaInformacoesPorta(ap,dataabertura,datafecha, int(fim-inicio))


            print ("Processo finalizado")
        else:
            contapessoas=1


def gravaInformacoesPorta(ap,dataab,dataf,x):
    path = 'portalog.txt'
    txt_porta = open(path,'a+')
    instr = "{0},{1},{2},{3}\n".format(ap, dataab, dataf,x)
    txt_porta.write(instr)

    #salvar imagens

def runPorta(run_once):
    global ap,dataabertura, inicio,contapessoas, counter_IR, counter_while, counter_RFID, counter_mudanca, counter_interfone
    if(run_once==1):
        initializePorta()
        run_once=0
    while(True):
        while(counter_RFID==0 and counter_mudanca==0):
            try:
                rdr2.wait_for_tag()
                (error, data) = rdr2.request()
                if not error:
                    print("\nRfid detectado: " + format(data, "02x"))

                (error, uid) = rdr2.anticoll()
                if not error:
                    if( uid == rfid1):
                        print("Acesso permitido - Isabel ( Ap 1 ),RFID com UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                        ap=1
                    elif(uid == rfid2):
                        print("Acesso permitido - Rogério ( Ap 2), RFID com UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                        ap=2
                    print ("Sistema Porta")
                    counter_RFID=1
                    GPIO.output(33, 1) # aciona sistema relé por 1 segundo
                    time.sleep(1)
                    GPIO.output(33,0) # desativa sistema relé por 1 segundo
                    dataabertura= time.strftime("%d %b %Y %H:%M:%S")
                    inicio = timeit.default_timer()


            except Exception, e:
                datenow = time.strftime("%d %b %Y %H:%M:%S")
                GPIO.cleanup()
                error=str(e)
                path = 'portalogerrors.txt'
                txt_portaerror = open(path,'a+')
                instr = "{0},{1}\n".format(error, datenow)
                txt_portaerror.write(instr)
        try:
            continue
        except KeyboardInterrupt:
            datenow = time.strftime("%d %b %Y %H:%M:%S")
            GPIO.cleanup()
            error=str(e)
            path = 'portalogerrors.txt'
            txt_portaerror = open(path,'a+')
            instr = "{0},{1}\n".format(error, datenow)
            txt_portaerror.write(instr)
