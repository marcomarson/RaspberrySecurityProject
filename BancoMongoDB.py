#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : Marco Marson

from pymongo import MongoClient
import gridfs
class BancoMongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/raspberry?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin")
        return self.client

    def insert(self, xT,UID, time_abertura_portao, time_fecha_portao, tempoaberto):
        self.fs=gridfs.GridFS(self.db)
        self.objeto= self.fs.put(xT,rfid=UID, horario_abertura= time_abertura_portao, horario_fecha = time_fecha_portao, tempo_portao_aberto=tempoaberto)
        return self.objeto

    def insertporta(self,xT, UID, time_abertura_portao, time_fecha_portao, tempoaberto):
        self.fs=gridfs.GridFS(self.db)
        self.objeto= self.fs.put(xT, rfid=UID, horario_abertura= time_abertura_portao, horario_fecha = time_fecha_portao, tempo_portao_aberto=tempoaberto)
        return self.objeto

    # def recoverPhoto(self, from, to):
    #     self.fs= gridfs.GridFS(self.db)
    #     self.fs.files.find().pretty()
    #     #im_stream = self.fs.get_last_version(filename)
    #     im = Image.open(im_stream)
    #     #return serve_pil_image(im)
