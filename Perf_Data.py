#!/user/bin/python3
#/usr/local/bin
# -*- coding: utf-8 -*-
import os,re,sys
import csv
import time
import datetime
import subprocess
import numpy as np
from subprocess import Popen, PIPE
import logging
import threading
#import OperationA
#import OperationB
#import OperationC
from OperationA import packageA,runA
from OperationB import packageB,runB
from OperationC import *
#from Operation import OperationA,OperationB,OperationC #导入Operation.py文件的Operation类


if os.path.exists(os.getcwd() + "/test_data"):
    pass
else:
    os.makedirs(os.getcwd() + "/test_data")

 
def get_mem(package):
    try:
        cmd = r'adb shell dumpsys meminfo ' + package + ' | grep "TOTAL"'  # % apk_file
        total = str((os.popen(cmd).readlines()))
        return (re.findall(r"\d+\.?\d*", total)[0])
    except Exception as e:
        print(str(e),"get_mem(package)，01请检查包名是否正确……")
        return -1
 
 
 
def dump_layer_stats(str_command):
    L = []
    p = Popen(str_command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for line in p.stdout:
        if line != '\n':
            ldata1 =(line[:-1].split('\t'))
            ldata=[]
            for i in ldata1:
                ldata.append(int(i))
            if len(ldata)== 1:
                pass
            else:
                if (ldata[1]) >= 9223372036854775807:
                    continue
                elif (ldata[1]) == 0:
                    continue
                L.append((ldata[1]))
                #    p.terminate()
    return L
def get_fps(str_command):
        while True:
            try:
                L =dump_layer_stats(str_command)
                size = len(L)
                interval = 0
                if size > 0:
                    interval = L[size - 1] - L[0]
                else:
                    #print("get_fps(str_command)，请使用adb shell dumpsys SurfaceFlinger更新SurfaceView名称")
                    return -1#(获取不到异常)
                if interval == 0:
                    continue
                fps = 1000000000 * (size - 1) / interval
                return round(fps)
            except Exception as e:
                print(str(e),"get_fps(str_command)，01请检查adb是否连通……")
                return '0'
 
 
def get_battery():
    try:
        cmd = 'adb shell dumpsys battery'  # % apk_file
        redcmd = str((os.popen(cmd).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("[",
                                                                                                                 " ")
        battery_dic = {}
        redcmd = (redcmd).split("n', '")[0].split(',')
        for i in redcmd[1:]:
            if ":" in i:
                b_dic = {i.split(":")[0].replace(" ", ""): i.split(":")[1]}
                battery_dic.update(b_dic)
 
        return battery_dic
    except Exception as e:
        print(e,"get_battery()，02请检查包名是否正确……")
        bat_dic={'ACpowered': ' false ',
                 'USBpowered': ' false ',
                 'Wirelesspowered': ' false ',
                 'Maxchargingcurrent': ' 0 ',
                 'Maxchargingvoltage': ' 0 ',
                 'Chargecounter': ' 2172420 ',
                 'status': ' 3 ',
                 'health': ' 2 ',
                 'present': ' true ',
                 'level': ' -1 ',
                 'scale': ' 100 ',
                 'voltage': ' 3843 ',
                 'temperature': ' -1 ',
                 'technology': ' Li-poly  '}
 
        return bat_dic
 
def getUid(package_name):#获取UID
    try:
        p1 = subprocess.Popen('adb shell dumpsys package ' + package_name + ' | grep "userId"',shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 用adb获取信息
        uidLongString = p1.stdout.read()
        uidLongList = uidLongString.split()
        uidMap = uidLongList[0]
        uid = str(uidMap).split("=")[1].replace("'", "")
     
        return uid

    except Exception as e:
        print(e,"getUid()，03请检查包名是否正确……")
 
 
 
def getRev(Uid):
    try:
        rx_bytes = []
        tx_bytes = []
        rx_tcp_bytes = []
        tx_tcp_bytes = []
        cmd = 'adb shell "cat /proc/net/xt_qtaguid/stats | grep %s"' % (Uid)
        redcmd = str((os.popen(cmd).readlines())).replace("['", '').replace("]", '').replace("\\n'", '').replace("'",
                                                                                                                 "").split(
            ",")
        for r in redcmd:
            red = r.split(" ")
            red = [i for i in red if i != '']
            rx_bytes.append(int(red[5]))
            tx_bytes.append(int(red[7]))
            rx_tcp_bytes.append(int(red[9]))
            tx_tcp_bytes.append(int(red[15]))
        # dics={
        #     "rx_bytes":sum(rx_bytes),
        #     "tx_bytes": sum(tx_bytes),
        #     "rx_tcp_bytes":sum(rx_tcp_bytes),
        #     "tx_tcp_bytes":sum(tx_tcp_bytes),
        # }
        listdic = [sum(rx_bytes), sum(tx_bytes), sum(rx_tcp_bytes), sum(tx_tcp_bytes), ]
 
        return listdic
    except Exception as e:
        print(e,"getRev(package_name)，04请检查包名是否正确……")
        return [-1,-1,-1,-1]
 
 
def get_cpu(pid):
    try:
        cmd = 'adb shell "cat /proc/stat | grep ^cpu"'  # % apk_file
        cmd1 = 'adb shell cat /proc/%s/stat' % (pid)
        redcmd = str((os.popen(cmd).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("[",
                                                                                                                 " ")
        redcmd = [i for i in redcmd.split(",")[0].split(" ") if i != '']
        redcmd.remove(redcmd[0])
        del redcmd[-3:]
        total_cpu = sum(list(map(int, redcmd)))
        idle=redcmd[3]
        redcmd1 = str((os.popen(cmd1).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("[",
                                                                                                                 " ").split(
            " ")[14:18]
        pjiff=sum(list(map(int, redcmd1)))
        return [total_cpu,idle,pjiff]
    except Exception as e:
        print(e,"get_s_cpu(),02检查adb是否连通……")
        return [-1,-1,-1,-1,-1,-1,-1]
 
def get_Screen():
    try:
        cmd = 'adb shell "dumpsys window policy|grep isStatusBarKeyguard"'  # % apk_file
        redcmd = str((os.popen(cmd).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("["," ").split("=")[-1]
        return (redcmd)
    except Exception as e:
        print(e,"get_Screen(),03检查adb是否连通……")
def get_iphoneinfo():
    try:
        dics={}
        cmd ='adb shell "getprop | grep product"'
        redcmd= str((os.popen(cmd).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("["," ").replace(" ","").split(",")
        for i in redcmd:
            if ":" in i:
                dic={i.split(":")[0]:i.split(":")[-1]}
                dics.update(dic)
        cmd1 ='adb shell cat /proc/meminfo'
        redcmd1= str((os.popen(cmd1).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("["," ").replace(" ","").split(",")[0]
        pp,cupxh,mmet=(dics["ro.product.manufacturer"].title() +" "+ dics['ro.product.model'], dics['ro.product.board'],
         str(round(int(re.findall(r"\d+\.?\d*", redcmd1)[0]) / 1024 / 1024)) + "G")
        return ("%s;%s;%s"%(pp,cupxh,mmet))
    except Exception as e:
        print(str(e),"get_mem(package)，04请检查adb是否连通……")
        return 'xxxxx'
def get_PID(package):
    if int(str((os.popen("adb shell getprop ro.build.version.release").readlines())).replace("'", "").replace("\\n"," ").replace(
                    "]", " ").replace("[", " ").split('.')[0]) >= 8:
        cmd = "adb shell ps -A"
    else:
        cmd="adb shell ps"
    try:
        pid=[]
        redcmd = str((os.popen(cmd).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("["," ").split(",")
        for n in redcmd:
            if package in n:
                list_n = [i for i in n.split(" ") if i != '']  # 删除空元素
                if package == list_n[-1]:
                    pid.append(list_n[1])
        return pid[0]
    except Exception as e:
        print(str(e), "get_mem(package)，05请检查adb是否连通……")
        return 'xxxxx'
 
def SumDic(versionCode,versionName,package,t):
    csv = logging.getLogger()
    csv.setLevel(logging.DEBUG)
    FileName = os.getcwd() + "/test_data/"+time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + '.csv'
    fh= logging.FileHandler(FileName)
    fh.setLevel(logging.INFO)
    ch= logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter()
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    csv.addHandler(ch)
    csv.addHandler(fh)
    Uid=getUid(package)
    print("进入SumDic函数..."+Uid)
    pid=get_PID(package)
    net1 = np.array(getRev(Uid))#流量
    total_cpu1,idle1,pjiff1= get_cpu(pid)
    str_command = get_cmmand(package)
    iphone_info=get_iphoneinfo()
    bt = "'time','iphone_info', 'package', 'mem', 'cpu', 'systemCpu', 'rxBytes', 'txBytes', 'rxTcpBytes', 'txTcpBytes', 'fps', 'level','batterytem'".replace("'", "").replace(" ", "")
    csv.info(bt)
    m = 0
    while True:
        print(m)
        m = m+1
        timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        mem = round(int(get_mem(package)) / 1024, 3)
        fps = get_fps(str_command)
        level = int(get_battery()['level'])
        batterytem = int(get_battery()['temperature']) / 10
        total_cpu2,idle2,pjiff2= get_cpu(pid)
        net2 = np.array(getRev(Uid))  # 流量
        pcpu = 100.0 * (int(pjiff2) - int(pjiff1)) / (int(total_cpu2) - int(total_cpu1))  # process cpu
        systemCpu =100.0 * ((int(total_cpu2) - int(idle2)) -(int(total_cpu1) - int(idle1))) / (int(total_cpu2) - int(total_cpu1))  # system cpu
        rbytes, tbytes, rtcp, ttcp = (net2 - net1)  # 流量
        total_cpu1,idle1,pjiff1 = total_cpu2,idle2,pjiff2
        net1 = net2
        sumdic = {
            "time": timestr,
            "iphone_info":iphone_info,
            'package': package+"-"+versionName+"-"+versionCode,
            "mem": mem,
            "cpu": round(pcpu,2),
            "systemCpu": round(systemCpu,2),
            'rxBytes': round(rbytes / 1024, 3),
            'txBytes': round(tbytes / 1024, 3),
            'rxTcpBytes': round(rtcp / 1024, 3),
            'txTcpBytes': round(ttcp / 1024, 3),
            "fps": fps,
            "level": level,
            "batterytem": batterytem,
        }
        list_v = str(list(sumdic.values())).replace("[", "").replace("]", "").replace("'", "")
        csv.info(list_v)
        #logger.info(sumdic)
        if t == 1 and thread_daemon(t1) == 1:
            print("结束for循环1！")
            break
        elif t == 2 and thread_daemon(t2) == 1:
            print("结束for循环2！")
            break
        elif t == 3 and thread_daemon(t3) == 1:
            print("结束for循环3！")
            break
    print('结束for循环后执行...')

 
def get_Activity(package):
    try:
        cmd = 'adb shell dumpsys SurfaceFlinger --list'  # % apk_file
        redcmd =str((os.popen(cmd).readlines())).replace("'", "").replace("\\n", " ").replace("]", " ").replace("[", " ").split(" ")
        listpack=[]
        for i in redcmd:
            if package in i:
                listpack.append(i)
        return max_list(listpack).replace(" ","")
    except Exception as e:
        print(str(e),"get_mem(package)，05请检查adb是否连接……")
def max_list(lt):
    temp = 0
    for i in lt:
        if lt.count(i) > temp:
            max_str = i
            temp = lt.count(i)
    return max_str
def get_cmmand(package):
    str_command0 = 'adb shell dumpsys SurfaceFlinger --latency SurfaceView\ -\ %s'%(get_Activity(package))
    str_command1 = 'adb shell dumpsys SurfaceFlinger --latency SurfaceView  %s'%(get_Activity(package))
    str_command2 = 'adb shell dumpsys SurfaceFlinger --latency  %s'%(get_Activity(package))
    list_cmd = [str_command0, str_command1, str_command2]
    for i in list_cmd:
        if int(get_fps(i))!=-1:
            return i
def thread_daemon(thread):
    if not thread.is_alive():
        return 1
def Operation_get(st):
    if st == "A":
        #Op = OperationA()
       runA()
    if st == "B":
        #Op = OperationB()
        runB()
    if st == "C":
        #Op = OperationC()
        runC()
    else:
        print('ERRO!')
                
def DetectThread(Id):
    global timer
    if Id == 0:
        t1 = time.time()
        time_local = time.localtime(t1)
        dt = time.strftime("%Y.%m.%d %H:%M:%S", time_local)
        print('执行线程1，执行时间：', dt)
        Operation_get(package1,"A")
        timer = threading.Timer(2, DetectThread, (1,))
        timer.start()
    if Id == 1:
        t2 = time.time()
        time_local = time.localtime(t2)
        dt = time.strftime("%Y.%m.%d %H:%M:%S", time_local)
        print('执行线程2，执行时间：', dt)
        Operation_get(package1,"B")
        timer = threading.Timer(2, DetectThread, (2,))
        timer.start()
    if Id == 2:
        time_local = time.localtime(time.time())
        dt = time.strftime("%Y.%m.%d %H:%M:%S", time_local)
        print('执行线程3，执行时间：', dt)
        Operation_get(package1,"C")
#timer = threading.Timer(2, DetectThread, (0,))
#timer.start()
def make_data():
    file_old = os.listdir(os.getcwd()+'/test_data')
    file_temp = os.getcwd()+'/test_data/test_temp.csv'
     
    for i in range(0,len(file_old)):
        old_path = os.getcwd()+'/test_data/'+file_old[i]
        print(old_path)
        with open(old_path, 'r', newline='', encoding='utf-8') as f_old, \
            open(file_temp, 'w', newline='', encoding='utf-8') as f_temp:
            f_csv_old = csv.reader(f_old)
            f_csv_temp = csv.writer(f_temp)
            l = 0
            g = 0
            f_csv_bk = []
            for rows in f_csv_old:
                if l != 0 and rows[0] == 'time':
                    print(rows)
                    break
                f_csv_bk.append(rows)
                l = l+1
            for rowss in f_csv_bk:  #删除最后一行
                if g == l-1:
                    print(rowss)
                    break
                f_csv_temp.writerow(rowss)
                g = g+1
        os.remove(old_path)
        os.rename(file_temp, old_path)
def App_Info(package,str):
    apk_file = os.getcwd()+"/test_apk/"+str+".apk"
    os.system("adb install -r %s" %apk_file)
    try:
        versionCode = os.popen("adb shell dumpsys package %s|grep version" %package).readlines()[0].split('versionCode=')[1].split(' ')[0]
        versionName = os.popen("adb shell dumpsys package %s|grep version" %package).readlines()[1].split('versionName=')[1].split("\n")[0]
        return versionCode,versionName
    except Exception as e:
        return 0,0
def del_APP(package):
    os.system("adb uninstall %s" %package)
    
if __name__ == '__main__':
    #os.system('adb connect 192.168.1.98:5555')#连接WiFi连通adb
    os.system("rm -r ./test_data/**")
    package1 = packageA
    package2 = packageB
    package3 = packageC
    #num(package1,package2,package3)
    #t1 = threading.Thread(target=SumDic(),args=package)
    #t1.setdaemon(True)
    #t1.start()
    versionCode,versionName = App_Info(package1,"A")
    t1 = threading.Thread(target=Operation_get,args=("A"))
    t1.start()
    time.sleep(18)  #waiting app to launch
    SumDic(versionCode,versionName,package1,1)
    time.sleep(3)
    del_APP(package1)
    versionCode,versionName = App_Info(package2,"B")
    t2 = threading.Thread(target=Operation_get,args=("B"))
    t2.start()
    time.sleep(18)
    SumDic(versionCode,versionName,package2,2)
    time.sleep(3)
    del_APP(package2)
    versionCode,versionName = App_Info(package3,"C")
    t3 = threading.Thread(target=Operation_get,args=("C"))
    t3.start()
    time.sleep(18)
    SumDic(versionCode,versionName,package3,3)
    time.sleep(3)
    del_APP(package3)
    dir_f = os.getcwd() + "/test_data/" + ".DS_Store"
    os.system("rm -r %s" %dir_f)
    os.system("lsof -n -i:4723 | grep LISTEN | awk '{print $2}' | xargs kill")  #强制杀死appium
    #os.system("ps -A | grep node | grep -v grep | awk 'NR=1 {print $1}' | xargs kill -9")  #杀死node
    make_data()
