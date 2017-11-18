import os
from pymongo import MongoClient
import gridfs
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".jpg"):
            name=file.split(".")
            ap,dia,versao=name[0].split("-")
            save(ap,dia,foto)
            # interpreta o nome da fimfoto




def save(ap,dia,foto):
    client = MongoClient("mongodb://marcomarson:naruto18@raspberry-shard-00-00-h82fm.mongodb.net:27017,raspberry-shard-00-01-h82fm.mongodb.net:27017,raspberry-shard-00-02-h82fm.mongodb.net:27017/teste?ssl=true&replicaSet=Raspberry-shard-0&authSource=admin")
    db=client.projeto
    fs=gridfs.GridFS(db)
    objeto= fs.put(foto,apartamento=ap, dia=dia)
    return objeto
