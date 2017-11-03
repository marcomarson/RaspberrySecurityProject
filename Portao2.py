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
locale.setlocale(locale.LC_ALL, 'Portuguese')
run_once_portao=1

def initialize():
    counter_IR = 0
    counter_while=True
    counter_RFID=0
    counter_mudanca=0
    GPIO.add_event_detect(13, GPIO.RISING, callback=infraRedPortao, bouncetime=300) # infravermelho
    #GPIO.add_event_detect(11, GPIO.FALLING, callback=chaveFimCurso, bouncetime=300) #chave fim de curso
    GPIO.add_event_detect(35, GPIO.RISING, callback=botaoMudancaAtiva, bouncetime=300) # mudanca
    GPIO.add_event_detect(35, GPIO.FALLING, callback=botaoMudancaDesativa, bouncetime=300) #mudanca
    GPIO.add_event_detect(37, GPIO.RISING, callback=interFone, bouncetime=300) #Interfone
    GPIO.add_event_detect(40, GPIO.RISING, callback=interFone, bouncetime=300) #Interfone 2
    #carregar tags RFID do banco
def interFone():
    print ("Interfone Ligado")
    print ("Abrindo portão")
    dataabertura= time.strftime("%d %b %Y %H:%M:%S")
    inicio = timeit.default_timer()
    GPIO.output(31, 1) # aciona sistema relé por 1 segundo
    time.sleep(1)
    GPIO.output(31,0) # desativa sistema relé por 1 segundo


def CameraPhoto(contafoto):
    camera= Camera()
    try:
        nomefoto='imagem'+str(contafoto)+'.jpg'
        print (nomefoto)
        camera.tirafoto(nomefoto)
        contafoto=contafoto+1
        iniciofoto = timeit.default_timer()
        fimfoto= timeit.default_timer()
    finally:
        camera.fecha()


def infraRedPortao():
    if(counter_RFID == 1):
        print ("Infravermelho detectado após RFID")
        print ("Acionar câmera")
        contafoto=0
        input_state = GPIO.input(11)
        while(input_state == True):
            CameraPhoto(contafoto)
            contafoto=contafoto+1
        chaveFimCurso()
    else:
        input_state = GPIO.input(32)
        if(input_state == False):
            print ("Infravermelho detectado pela chave ou pelo interfone - Saindo")
        else:
            print ("Infravermelho detectado pelo interfone - Entrando")
            print ("Acionar câmera")
            contafoto=0
            input_state = GPIO.input(11)
            while(input_state == True):
                CameraPhoto(contafoto)
                contafoto=contafoto+1
            chaveFimCurso()



def botaoMudancaAtiva():
    counter_mudanca=1
def botaoMudancaDesativa():
    counter_mudanca=0

def chaveFimCurso():
    if(counter_RFID==1):
        counter_RFID=0
        datafecha = time.strftime("%d %b %Y %H:%M:%S")
        fim= timeit.default_timer()
        #enviabancodedados
        #funcaopraenviardemadrugada
        #print("Enviando informações para o banco de dados")
        #bid=bancodedados.insertporta(str(uid),dataabertura,datafecha, int(fim-inicio))
        #print(bid)
    print ("Processo finalizado")

def run():
    if(run_once_portao==1):
        initialize()
        run_once_portao=0
    while(counter_RFID==0 and counter_mudanca==0):
        try:

            (error, data) = rdr.request()
            if not error:
                print("\nRfid detectado: " + format(data, "02x"))

            (error, uid) = rdr.anticoll()
            if not error:
                if( uid == rfid1):
                    print("Acesso permitido - Isabel ( Ap12 ),RFID com UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                elif(uid == rfid2):
                    print("Acesso permitido - Rogério ( Ap30), RFID com UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
                print ("Sistema Porta")
                counter_RFID=1
                GPIO.output(31, 1) # aciona sistema relé por 1 segundo
                time.sleep(1)
                GPIO.output(31,0) # desativa sistema relé por 1 segundo
                dataabertura= time.strftime("%d %b %Y %H:%M:%S")
                inicio = timeit.default_timer()


        except KeyboardInterrupt:
            GPIO.cleanup()
    try:
        #GPIO.wait_for_edge(13, GPIO.RISING)
        #print "Infravermelho detectado"
        #camera action
        #send email/information about door  . Utilizar site online para enviar email, pois raspberry pi vai travar.
        #print "Esperando sinal chave fim de curso "
        #GPIO.wait_for_edge(11, GPIO.RISING)
        #print("Processo finalizado")
        run()
    except KeyboardInterrupt:
        GPIO.cleanup()
