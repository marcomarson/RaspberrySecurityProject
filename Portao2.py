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
from Camera import Camera
from Notifications import sendemail

contapessoas=0
counter_IR = 0
counter_while=True
counter_RFID=0
counter_mudanca=0
ap=0
inicio=0
fim=0
counter_email=0
def initialize():
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    GPIO.setmode(GPIO.BOARD)
    global counter_IR, counter_RFID, counter_while, counter_mudanca, counter_interfone, contapessoas
    GPIO.add_event_detect(13, GPIO.BOTH, callback=infraRedPortao, bouncetime=300) # infravermelho
    GPIO.add_event_detect(11, GPIO.FALLING, callback=chaveFimCurso, bouncetime=300) #chave fim de curso
    GPIO.add_event_detect(35, GPIO.BOTH, callback=botaoMudanca, bouncetime=300) # mudanca
    GPIO.add_event_detect(37, GPIO.RISING, callback=interFone, bouncetime=300) #Interfone
    GPIO.add_event_detect(40, GPIO.RISING, callback=interFone, bouncetime=300) #Interfone 2
    #carregar tags RFID do banco
    chaveFimCurso(11)

def interFone(channel):
    global ap,counter_IR, counter_RFID, counter_while, counter_mudanca, counter_interfone, contapessoas
    print ("Interfone Ligado")
    print ("Abrindo portão")
    GPIO.output(31, 1) # aciona sistema relé por 1 segundo
    time.sleep(1)
    GPIO.output(31,0) # desativa sistema relé por 1 segundo

    if(channel==37): ##procurar no banco de dados
        ap=1
    elif(channel==40):
        ap=2


def CameraPhoto():
    global ap
    try:
        camera= Camera()
        camera.tirafoto(ap)
    finally:
        camera.fecha()


def infraRedPortao(channel):
    global ap, counter_IR, counter_RFID, counter_while, counter_mudanca, counter_interfone, contapessoas
    if(contapessoas==0):
        if(counter_RFID == 1):
            print ("Infravermelho detectado após RFID")
            print ("Acionar câmera")
            input_state = GPIO.input(11)
            while(input_state == True):
                CameraPhoto()
        else:
            input_state = GPIO.input(32)
            if(input_state == False):
                print ("Infravermelho detectado pela chave ou pelo interfone - Saindo")
            else:
                print ("Infravermelho detectado pelo interfone - Entrando")
                print ("Acionar câmera")
                input_state = GPIO.input(11)
                while(input_state == True):
                    CameraPhoto()



def botaoMudanca(channel):
    global counter_IR, counter_RFID, counter_while, counter_mudanca, counter_interfone, contapessoas
    input_state = GPIO.input(35)
    if(input_state == False):
        counter_mudanca=1
    else:
        counter_mudanca=0

def chaveFimCurso(channel):
    global ap,counter_email,inicio,dataabertura,counter_IR, counter_RFID, counter_while, counter_mudanca, counter_interfone, contapessoas
    input_state = GPIO.input(11)
    if(input_state == False):
        contapessoas=0
        fim= timeit.default_timer()
        datafecha = time.strftime("%d %b %Y %H:%M:%S")
        if(counter_RFID==1):
            counter_RFID=0
        gravaInformacoesPorta(ap,dataabertura,datafecha, int(fim-inicio))
        print ("Processo finalizado")
    else:
        inicio=timeit.default_timer()
        dataabertura= time.strftime("%d %b %Y %H:%M:%S")
        contapessoas=1
        counter_mudanca=0
        counter_email=0

def gravaInformacoesPortao(ap,dataab,dataf,x):
    path = 'portaolog.txt'
    txt_porta = open(path,'a+')
    instr = "{0},{1},{2},{3}\n".format(ap, dataab, dataf,x)
    txt_porta.write(instr)
    #salvar imagens
def run(run_once_portao):
    global counter_email,inicio,fim,ap,counter_IR, counter_RFID, counter_while, counter_mudanca, counter_interfone, contapessoas
    if(run_once_portao==1):
        initialize()
        run_once_portao=0
    while(True):

        while(counter_RFID==0 and counter_mudanca==0):
            try:
                if(int(fim-inicio)>30 and counter_email==0):
                    sendemail(ap)
                    counter_email=1


                (error, data) = rdr.request()
                if not error:
                    print("\nRfid detectado: " + format(data, "02x"))

                (error, uid) = rdr.anticoll()
                if not error:
                    if( uid == rfid1):
                        print("Acesso permitido - Isabel ( Ap1 )")
                        ap=1
                    elif(uid == rfid2):
                        print("Acesso permitido - Rogério ( Ap30)")
                        ap=2
                    print ("Sistema Portão")
                    counter_RFID=1
                    GPIO.output(31, 1) # aciona sistema relé por 1 segundo
                    time.sleep(1)
                    GPIO.output(31,0) # desativa sistema relé por 1 segundo


            except Exception, e:
                datenow = time.strftime("%d %b %Y %H:%M:%S")
                GPIO.cleanup()
                error=str(e)
                path = 'portalogerrors.txt'
                txt_portaerror = open(path,'a+')
                instr = "{0},{1}\n".format(error, datenow)
                txt_portaerror.write(instr)
        continue
