#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2,sqlite3
import math

### Extract all the transponders from the given satellite + channels ###

class Satellite:


    def __init__(self,sat=''):

        self.sat=sat
        self.satFreq=''
        self.satParameters={

            #'transponderParameters':[],
            #'tansponderChannels':[]

        }

        self.channels=[]
    def get(self):
        #self.sat=sat
        if self.sat:
            self.page=urllib2.urlopen(self.sat)
            self.soup=BeautifulSoup(self.page,"html5lib")
            conta=self.soup.find_all('table',class_='frq')
        baza=sqlite3.connect('bazata2')
        c=baza.cursor()
        c.execute('drop table if exists parameters')
        c.execute('CREATE TABLE parameters(id integer primary key autoincrement,channel text,transponder text,fr int,lnb character,fec text,degree int,vpid int,apid int,sid int,nid int,tid int);')
        for el in range(len(conta)):
            satelites=conta[el].find_all('td')[:-1]
            satFreq=int(math.floor(float(satelites[2].string)))
            for headerElement in satelites:
                self.satParameters.setdefault(satFreq,{}).setdefault('transponderParameters',[]).append(headerElement.get_text())

            prn=conta[el].next_sibling.next_sibling.find_all('a',class_='A3')
            try:

                for el1 in prn:
                    el=el1.parent.parent.find_all('td')
                    chanName=el[2].get_text().strip()
                    provider='satoperator'
                    transponder=satFreq
                    fr=self.satParameters[satFreq]['transponderParameters'][3]
                    lnb=self.satParameters[satFreq]['transponderParameters'][4]
                    fec=self.satParameters[satFreq]['transponderParameters'][8][-3:]
                    deg=self.satParameters[satFreq]['transponderParameters'][0][:4]+self.satParameters[satFreq]['transponderParameters'][0][5:]
                    sid=el[7].get_text()
                    vpid=el[8].get_text()
                    apid=el[9].get_text().split()[0]
                    nid=self.satParameters[satFreq]['transponderParameters'][10][4:]
                    tid=self.satParameters[satFreq]['transponderParameters'][11][4:]
                    c.execute('''insert into parameters(channel,transponder,fr,lnb,fec,degree,vpid,apid,sid,nid,tid) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'''%(chanName,transponder,fr,lnb,fec,deg,vpid,apid,sid,nid,tid))


            except Exception as e:
                print e
        baza.commit()
        baza.close()
        #print self.satParameters
    def getParameters(self,transponder):
        for val in self.satParameters[transponder]['transponderParameters']:
            print val

        print 'number of channels on this transponder : [%s]'%len(self.satParameters[transponder]['tansponderChannels'])

proba=Satellite('http://en.kingofsat.net/pos-13E.php')
proba.get()
