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


def initializePorta(): #__init__
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') #pt_br.utf-8
    global contapessoas=0
    global counter_IR = 0
    global counter_while=True
    global counter_RFID=0
    global counter_mudanca=0
    global counter_interfone=0
    GPIO.add_event_detect(36, GPIO.RISING, callback=infraRedPortaPorta, bouncetime=300) # Botão Infravermelho porta
    GPIO.add_event_detect(32, GPIO.BOTH, callback=chaveFimCursoPorta, bouncetime=300) # Botão Chave fim de curso porta
    GPIO.add_event_detect(35, GPIO.BOTH, callback=botaoMudancaPorta, bouncetime=300) # Botão Mudança
    GPIO.add_event_detect(37, GPIO.RISING, callback=interFonePorta, bouncetime=300) #Interfone
    GPIO.add_event_detect(40, GPIO.RISING, callback=interFonePorta, bouncetime=300) #Interfone 2
    #carregar tags RFID do banco

def interFonePorta():
    counter_interfone=1
    print ("Interfone Ligado")
    print ("Abrindo porta")
    dataabertura= time.strftime("%d %b %Y %H:%M:%S")
    inicio = timeit.default_timer()
    GPIO.output(33, 1) # aciona sistema relé por 1 segundo
    time.sleep(1)
    GPIO.output(33,0) # desativa sistema relé por 1 segundo

def CameraPorta():
    os.system('fswebcam -r 320x240 -S 3 --jpeg 50 --save /home/pi/PhotosMAM/%H%M%S.jpg') #editar endereço de onde salvar e salvar com ID da pessoa


def infraRedPortaPorta():
    if(contapessoas=0):
        if(counter_RFID == 1):
            print ("Infravermelho detectado após RFID")
        else:
            if(counter_interfone ==1):
                print("Infravermelho acionado após interfone")
                CameraPorta()
            else:
                print ("Infravermelho detectado após chave")
def botaoMudancaPorta():
    input_state = GPIO.input(35)
    if(input_state == False):
        counter_mudanca=1
    else:
        counter_mudanca=0

def chaveFimCursoPorta():
    input_state = GPIO.input(32)
    if(input_state == False):
        contapessoas=0
        if(counter_RFID==1):
            counter_RFID=0
            datafecha = time.strftime("%d %b %Y %H:%M:%S")
            fim= timeit.default_timer()
            #enviabancodedados
            #funcaopraenviardemadrugada
            #print("Enviando informações para o banco de dados")
            #bid=bancodedados.insertporta(str(uid),dataabertura,datafecha, int(fim-inicio))
            #print(bid)
        #gravaInformacoesPorta(str(uid),dataabertura,datafecha, int(fim-inicio))
        print ("Processo finalizado")
    else:
        contapessoas=1


def gravaInformacoesPorta(uid,dataab,dataf,x):
    path = 'portalog.txt'
    txt_porta = open(path,'a+')
    txt_porta.write("%s %s %s %d" % uid,dataab,dataf,x)
    #salvar imagens

def runPorta(run_once):
    if(run_once==1):
        initializePorta()
        run_once=0
    while(counter_RFID==0 and counter_mudanca==0):
        try:
            rdr2.wait_for_tag()
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
                counter_RFID=1
                GPIO.output(33, 1) # aciona sistema relé por 1 segundo
                time.sleep(1)
                GPIO.output(33,0) # desativa sistema relé por 1 segundo
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
        runPorta()
    except KeyboardInterrupt:
        GPIO.cleanup()
