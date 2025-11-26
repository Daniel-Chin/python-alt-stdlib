from pickle import dump
with open('Pickle','wb') as SaveFile:
    dump((1,1,3,'Holy Sickle',21,.1,2,\
          False,'',0,0,0,'',\
          0,0,10,1000),SaveFile)
    SaveFile.close()
