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

        for el in range(len(conta)):
            #print '[%s]'%conta[el].get_text()
            #extracting all the satellite parameters in a List
            #satelites=conta[el].find_all(['a','td'],class_='bld')
            satelites=conta[el].find_all('td')[:-1]
            satFreq=int(math.floor(float(satelites[2].string)))
            for headerElement in satelites:
                self.satParameters.setdefault(satFreq,{}).setdefault('transponderParameters',[]).append(headerElement.get_text())
            #print '  }'
            #print type(str(satelites[2].string))
        #All channels in a List
            prn=conta[el].next_sibling.next_sibling.find_all('a',class_='A3')
            try:
                #for chan in prn:
                ##    self.satParameters.setdefault(satFreq,{}).setdefault('tansponderChannels',[]).append(chan.string)
                for el1 in prn:
                    el=el1.parent.parent.find_all('td')
                    #for rd in (2,7,8,9,10,11):
                    chanName=el[2].get_text().strip()
                    provider='satoperator'
                    sid=el[7].get_text()
                    vpid=el[8].get_text()
                    apid=el[9].get_text().split()[0]

                    print 'channame: %s sid %s'%(chanName,sid)

            except Exception as e:
                print e
        #print '===> %s <===='%satelites
        print el
    def getParameters(self,transponder):
        for val in self.satParameters[transponder]['transponderParameters']:
            print val

        print 'number of channels on this transponder : [%s]'%len(self.satParameters[transponder]['tansponderChannels'])
        #for val in self.satParameters.keys():
        #    print val


    #def populate(self):



proba=Satellite('http://en.kingofsat.net/pos-13E.php')
proba.get()
#print proba.satParameters
baza=sqlite3.connect('bazata')
c=baza.cursor()
for trans in sorted(proba.satParameters):
    #c.execute('''insert into parameters('channel,transponder,fr,lnb,fec,degree,vpid,apid,sid,nid,tid')values('%s,%d,%d,%s,%s,%d,%d,%d,%d,%d,%d'%(trans)''')
    #print '[%s] : parameters: %s \n\t channels: %s '%(trans,proba.satParameters[trans]['transponderParameters'],proba.satParameters[trans].get('tansponderChannels'))


    #print 'trans -> %s'%trans
    #print 'insert : %s,%d,%d,%s,%s,%d,%d,%d,%d,%d,%d'%(proba.satParameters[trans])
    pass
    #for channel in proba.satParameters[trans]['tansponderChannels']:
    #    print '[ %% %s %% ]'%channel