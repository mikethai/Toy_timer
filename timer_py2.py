#coding=utf-8
import time
import string
from datetime import datetime,timedelta

mytime = datetime(2015,1,1)
print mytime.strftime('%Y/%m/%d %H:%M:%S')

time_list =list()
excute_time = 0
phead_time = 0

class Timer_Object:  
    def __init__(self, ptag, ticks, events):  
        self.ptag = ptag  
        self.ticks = ticks  
        self.events = events  
    def set_tag(self, ptag):  
        self.ptag = ptag
    def set_ticks(self, ticks):  
        self.ticks = ticks
    def cut_1s_ticks(self):
        self.ticks= self.ticks-1
    def set_events(self,events):
        self.events=events
    def return_value(self,whi):
        if whi == "tag":
            return self.ptag
        elif whi == "tick":
            return self.ticks
        elif whi == "events":
            return self.events
    def show_parmr(self):
        print self.ptag,self.ticks,self.events

def Do_What(events,num):
    if num ==0 :
        print "Run events " , events , ":We are the world! at ",mytime
    elif num ==1:
        print "Run events " , events , " :Trust me! You can make it! at ",mytime
    else:
        print "Run events " , events , " :Just do it now! at ",mytime
        
def removeTimer(tag_name):
    for obj in time_list:
        if obj.return_value("tag") == tag_name:
            idix=time_list.index(obj)
            time_list.pop(idix)
            
def runto(ticks):
    global mytime,excute_time
    while excute_time < ticks:
        if len(time_list)!=0:
            time_list[0].cut_1s_ticks()
            mytime = mytime + timedelta(seconds=1)
            while len(time_list)!=0 and time_list[0].return_value("tick")==0:                  #####
                print "Timer  " , time_list[0].return_value("tag") , "  at " , mytime
                Do_What(time_list[0].return_value("tag"),time_list[0].return_value("events"))
                time_list.pop(0)       
        excute_time+=1   
        
def dumpTimer():
    global mytime
    t=0
    print "Dump timer chain at" ,mytime
    for obj in time_list:
        t+=obj.return_value("tick")
        print "Timer " , obj.return_value("tag") ,": has " , obj.return_value("tick"), "/" ,t

def Insert_Timer(object_name):
    global phead_time
    if len(time_list)==0:
       phead_time= object_name.return_value("tick")    #第一個先push進來,當phead
       time_list.append(object_name)
    elif phead_time > object_name.return_value("tick"): #如果比phead小
        phead_time = object_name.return_value("tick")
        time_list[0].set_ticks(time_list[0].return_value("tick")-object_name.return_value("tick"))
        time_list.insert(0,object_name)
    else:
        object_name.set_ticks(object_name.return_value("tick")-time_list[0].return_value("tick"))
        time_list.append(object_name)

def read_input(txt_name):
    "讀檔案進來"
    file = open(txt_name)
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            sub_ary = line.split()  
            #0:執行指令時間  1:指令   2:程式ID   3:執行程式時間
            sub_ary[0] = int(sub_ary[0])
            ticka= sub_ary[0]
            if sub_ary[1]=="insert":
                object_name=sub_ary[2]
                object_ticks=int(sub_ary[3])
                object_evebt=int(sub_ary[4])
                newobject=Timer_Object(object_name,object_ticks ,object_evebt)
                Insert_Timer(newobject)
                pass
            elif sub_ary[1]=="dump":
                dumpTimer()
                pass
            elif sub_ary[1]=="remove":
                removeTimer(sub_ary[2])
                pass    
            runto(ticka)
            pass
    
    return;
    
read_input("timer.in");