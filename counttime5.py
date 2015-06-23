#coding=utf-8
import time
import string
command_second = list() #0
command_IDlist = list() #1
id_list =list()  #2
new_id_list= list()
process_list =list() #3
now_process_list =list()
#=============================================================
def read_input(txt_name):
    "讀檔案進來"
    file = open(txt_name)
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        line_count=0
        for line in lines:
            sub_ary = line.split()  
            #0:執行指令時間  1:指令   2:程式ID   3:執行程式時間
            sub_ary[0] = int(sub_ary[0])  
            sub_ary[3] = int(sub_ary[3])
            command_second.insert(line_count,sub_ary[0])
            command_IDlist.insert(line_count,sub_ary[1])
            id_list.insert(line_count,sub_ary[2])
            process_list.insert(line_count,sub_ary[3])
            line_count+=1
            pass    
    return;
#=============================================================
def  insert( id_name , now_second):
    
    if( len(now_process_list)==0):
        new_id_list.insert(0,id_name)
        now_process_list.insert(0,process_list[0])
        pass
    else:
        locate=i_locatation(now_process_list,process_list[0])
        new_id_list.insert(locate,id_name)
    id_list.pop(0)
    process_list.pop(0)
    #print "insert=====",id_name,now_second,now_process_list,new_id_list
    print "第",now_second,'秒--insert檔案',id_name
    return;
#=============================================================
def  remove( string , now_second ):
    idix=id_list.index(string)
    new_id_list.pop(idix)
    now_process_list.pop(idix)
    if len(new_id_list)>0:
        now_process_list[0]-=now_second-1
    #print string+'程式已強制中斷',now_second,now_process_list
    print string+'程式已強制中斷--在第',now_second,'秒'
    print "================================================="
    return;
#=============================================================    
def  countdown(now_second):
    now_process_list[0]-=1
    if(now_process_list[0]==0):
        print new_id_list[0],'程式自動結束'
        now_process_list.pop(0)
        new_id_list.pop(0)
        if len(now_process_list)>=1 and now_process_list[0]-now_second>0:
            now_process_list[0]-=now_second  
        elif len(now_process_list)>=1:
            now_process_list.pop(0)
            now_process_list[0]-=now_second
            pass 
    #print "countdown:",now_process_list,now_second
    #print "================================================="
    return;
#=============================================================
def i_locatation( now_process_list, second ):
    "定義位置在哪兒"
    now_process_list.insert(len(now_process_list)+1, second)
    now_process_list.sort()    
    return now_process_list.index( second);
#=============================================================
def command_pr(now_second):
    "執行指令程式"
    if command_IDlist[0]=="insert":
        insert( id_list[0] , now_second )
    else:    
        remove( id_list[0] , now_second )
        id_list.pop(0)
    command_second.pop(0)
    command_IDlist.pop(0)
    if(len(command_second)>=1 and command_second[0]==now_second):
        command_pr(now_second)
    pass       
    return;
#=============================================================     
read_input("input_time.txt")
now_second=0
while 1:
    if len(command_second)>=1 and command_second[0]==now_second:
        command_pr(now_second)
    time.sleep(1)
    countdown(now_second)
    now_second+=1  
    if len(now_process_list)==0:
        print "所有程式結束"
        break