import os
from pymongo import MongoClient
import gridfs
import datetime
def savelogportao(ap,datai,dataf,tempototal):
    client = MongoClient("mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/projeto?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin")
    db=client.projeto
    db.data.insert({'apartamento' : ap, 'horario_abertura' : datai, 'horario_fecha': dataf, 'tempo_portao_aberto' : tempototal})



def savelogporta(ap,datai,dataf,tempototal):
    client = MongoClient("mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/projeto?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin")
    db=client.projeto
    db.data.insert({'apartamento' : ap, 'horario_abertura' : datai, 'horario_fecha': dataf, 'tempo_porta_aberto' : tempototal})

def save(ap,dia,foto):
    client = MongoClient("mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/projeto?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin")
    db=client.projeto
    fs=gridfs.GridFS(db)
    objeto= fs.put(foto,apartamento=ap, dia=dia)



for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".jpg"):
            name=file.split(".")
            ap,dia,versao=name[0].split("-")
            #save(ap,dia,file)
            # interpreta o nome da fimfoto

path = 'portalog.txt'
f = open(path,'r')
if f.mode == 'r':
    fl =f.readlines()
    for line in fl:
        x=line.split(",")
        ap=x[0]
        datai=datetime.datetime.strptime(x[1],"%d %b %Y %H:%M:%S")
        dataf=datetime.datetime.strptime(x[2],"%d %b %Y %H:%M:%S")
        tempototal=x[3]
        savelogporta(ap,datai,dataf,tempototal)
    f.close()
open(path, 'w').close()


path = 'portaolog.txt'
f = open(path,'r')
if f.mode == 'r':
    fl =f.readlines()
    for line in fl:
        x=line.split(",")
        ap=x[0]
        datai=datetime.datetime.strptime(x[1],"%d %b %Y %H:%M:%S")
        dataf=datetime.datetime.strptime(x[2],"%d %b %Y %H:%M:%S")
        tempototal=x[3]
        savelogportao(ap,datai,dataf,tempototal)
    f.close()
open(path, 'w').close()
