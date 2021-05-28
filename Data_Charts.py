#!/user/bin/python
# -*- coding: utf-8 -*-
import os,time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import humanize
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
 
def csv2images(files):
    num = len(files)
    target_dir=os.getcwd()
    iphone_info=tets_iphone_info(files[0])
 
    """
            Args:
                src: csv file, default to perf record csv path
                target_dir: images store dir
            """
 
    plt.figure(figsize=(19.20, 10.80))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if num == 1:
        package_name=tets_pack_info(files[0])
        data = pd.read_csv(files[0])
        data['time'] = data['time'].apply(
            lambda x: datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))  # time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())  %Y-%m-%d %H:
    #    #     #timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
          
        timestr = time.strftime("%Y-%m-%d %H:%M")
        # network
     
        plt.subplot(7, 1, 1)
        plt.plot(data['time'], data['rxBytes'], '-')
     
        plt.title(
            '\n'.join(
                ["Summary",iphone_info,package_name, timestr,
                 'package_name:%s,|| Recv %s KB,|| Send %s KB,|| mem_avg %s,|| cpu_avg %s,|| fps_avg %s,|| level %s,|| battery_avg %s' % (package_name,round(data['rxBytes'].sum(), 2), round(data['txBytes'].sum(), 2), round(data['mem'].mean(), 2),  round(data['cpu'].mean(), 2), round(data['fps'].mean(), 2), round(data['level'].mean(), 2), round(data['batterytem'].mean(), 2))]),
            loc='left')
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.ylabel('Recv(KB)')
        plt.ylim(ymin=0)
     
        plt.subplot(7, 1, 2)
        plt.plot(data['time'], data['txBytes'])
        # plt.xlabel('Time')
        plt.ylabel('Send(KB)')
        plt.ylim(ymin=0)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
        # .clf()
     
        plt.subplot(7, 1, 3)
     
        plt.plot(data['time'], data['mem'])
        plt.ylabel('mem(MB)')
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 4)
        plt.plot(data['time'], data['cpu'])  # systemCpu
        plt.ylim(0, max(100, data['systemCpu'].max()))
        plt.ylabel('CPU')
        plt.ylim(ymin=0)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 5)
        plt.plot(data['time'], data['fps'], '-')
        plt.ylabel('FPS')
        plt.ylim(-1, 100)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 6)
        plt.plot(data['time'], data['level'], '-')
        plt.ylabel('level')
        plt.ylim(0, 110)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 7)
        plt.plot(data['time'], data['batterytem'], '-')
        plt.ylim(0, 100)
        plt.ylabel('BatteryTem')
        plt.xlabel('Time')
        
    elif num == 2:
        package_name_0=tets_pack_info(files[0])
        package_name_1=tets_pack_info(files[1])
        data0 = pd.read_csv(files[0])
        data1 = pd.read_csv(files[1])
        data0['time'] = data0['time'].apply(
            lambda x: datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))  # time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())  %Y-%m-%d %H:
    #    #     #timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        data1['time'] = data1['time'].apply(
            lambda x: datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
        nums = [len(data0),len(data1)]    #每个表格行数存放列表
        Max = max(nums)  #求最大数值
        if Max == len(data0):
            data1['time']=data0['time']
        elif Max == len(data1):
            data0['time']=data1['time']
        else:
            data1['time']=data0['time']
     
        timestr = time.strftime("%Y-%m-%d %H:%M")
        # network
     
        plt.subplot(7, 1, 1)
        plt.plot(data0['time'], data0['rxBytes'], '-', label=package_name_0)
        plt.plot(data1['time'], data1['rxBytes'], 'r-', label=package_name_1)
        plt.legend()
     
        plt.title(
            '\n'.join(
                ["Summary",iphone_info, timestr,
                 'package_name:%s,|| Recv %s KB,|| Send %s KB,|| mem_avg %s,|| cpu_avg %s,|| fps_avg %s,|| level %s,|| battery_avg %s' % (package_name_0,round(data0['rxBytes'].sum(), 2), round(data0['txBytes'].sum(), 2), round(data0['mem'].mean(), 2),  round(data0['cpu'].mean(), 2), round(data0['fps'].mean(), 2), round(data0['level'].mean(), 2), round(data0['batterytem'].mean(), 2)), 'package_name:%s,|| Recv %s KB,|| Send %s KB,|| mem_avg %s,|| cpu_avg %s,|| fps_avg %s,|| level %s,|| battery_avg %s' % (package_name_1,round(data1['rxBytes'].sum(), 2), round(data1['txBytes'].sum(), 2), round(data1['mem'].mean(), 2),  round(data1['cpu'].mean(), 2), round(data1['fps'].mean(), 2), round(data1['level'].mean(), 2), round(data1['batterytem'].mean(), 2))]),
            loc='left')
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.ylabel('Recv(KB)')
        plt.ylim(ymin=0)
     
        plt.subplot(7, 1, 2)
        plt.plot(data0['time'], data0['txBytes'], '-', label=package_name_0)
        plt.plot(data1['time'], data1['txBytes'], 'r-', label=package_name_1)
        plt.legend()
        # plt.xlabel('Time')
        plt.ylabel('Send(KB)')
        plt.ylim(ymin=0)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
        # .clf()
     
        plt.subplot(7, 1, 3)
     
        plt.plot(data0['time'], data0['mem'], '-', label=package_name_0)
        plt.plot(data1['time'], data1['mem'], 'r-', label=package_name_1)
        plt.legend()
        plt.ylabel('mem(MB)')
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 4)
        plt.plot(data0['time'], data0['cpu'], '-', label=package_name_0)  # Cpu
        plt.plot(data1['time'], data1['cpu'], 'r-', label=package_name_1)
        plt.legend()
        plt.ylim(0, max(100, data0['systemCpu'].max()))
        plt.ylim(0, max(100, data1['systemCpu'].max()))
        plt.ylabel('CPU')
        plt.ylim(ymin=0)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 5)
        plt.plot(data0['time'], data0['fps'], '-', label=package_name_0)
        plt.plot(data1['time'], data1['fps'], 'r-', label=package_name_1)
        plt.legend()
        plt.ylabel('FPS')
        plt.ylim(-1, 100)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 6)
        plt.plot(data0['time'], data0['level'], '-', label=package_name_0)
        plt.plot(data1['time'], data1['level'], 'r-', label=package_name_1)
        plt.legend()
        plt.ylabel('level')
        plt.ylim(0, 110)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 7)
        plt.plot(data0['time'], data0['batterytem'], '-', label=package_name_0)
        plt.plot(data1['time'], data1['batterytem'], 'r-', label=package_name_1)
        plt.legend()
        plt.ylim(0, 100)
        plt.ylabel('BatteryTem')
        plt.xlabel('Time')
        
    elif num == 3:
        package_name_0=tets_pack_info(files[0])
        package_name_1=tets_pack_info(files[1])
        package_name_2=tets_pack_info(files[2])
        data = pd.read_csv(files[0])
        data0 = pd.read_csv(files[1])
        data1 = pd.read_csv(files[2])

        data['time'] = data['time'].apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))  # time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())  %Y-%m-%d %H:
    #    #     #timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        data0['time'] = data0['time'].apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
        data1['time'] = data1['time'].apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f"))
        nums = [len(data),len(data0),len(data1)]    #每个表格行数存放列表
        Max = max(nums)  #求最大数值
        if Max == len(data):
            data0['time']=data['time']
            data1['time']=data['time']
        elif Max == len(data0):
            data['time']=data0['time']
            data1['time']=data0['time']
        elif Max == len(data1):
            data['time']=data1['time']
            data0['time']=data1['time']
        else:
            data['time']=data1['time']=data0['time']
        timestr = time.strftime("%Y-%m-%d %H:%M")
        # network
     
        plt.subplot(7, 1, 1)
        plt.plot(data['time'], data['rxBytes'], '-', label=package_name_0)
        plt.plot(data0['time'], data0['rxBytes'], 'r-', label=package_name_1)
        plt.plot(data1['time'], data1['rxBytes'], 'g-', label=package_name_2)
        plt.legend()
     
        plt.title(
            '\n'.join(
                ["Summary",iphone_info, timestr,
                    'package_name:%s,|| Recv %s KB,|| Send %s KB,|| mem_avg %s,|| cpu_avg %s,|| fps_avg %s,|| level %s,|| battery_avg %s' % (package_name_0,round(data['rxBytes'].sum(), 2), round(data['txBytes'].sum(), 2), round(data['mem'].mean(), 2),  round(data['cpu'].mean(), 2), round(data['fps'].mean(), 2), round(data['level'].mean(), 2), round(data['batterytem'].mean(), 2)), 'package_name:%s,|| Recv %s KB,|| Send %s KB,|| mem_avg %s,|| cpu_avg %s,|| fps_avg %s,|| level %s,|| battery_avg %s' % (package_name_1,round(data0['rxBytes'].sum(), 2), round(data0['txBytes'].sum(), 2), round(data0['mem'].mean(), 2),  round(data0['cpu'].mean(), 2), round(data0['fps'].mean(), 2), round(data0['level'].mean(), 2), round(data0['batterytem'].mean(), 2)), 'package_name:%s,|| Recv %s KB,|| Send %s KB,|| mem_avg %s,|| cpu_avg %s,|| fps_avg %s,|| level %s,|| battery_avg %s' % (package_name_2,round(data1['rxBytes'].sum(), 2), round(data1['txBytes'].sum(), 2), round(data1['mem'].mean(), 2),  round(data1['cpu'].mean(), 2), round(data1['fps'].mean(), 2), round(data1['level'].mean(), 2), round(data1['batterytem'].mean(), 2))]),
            loc='left')
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.ylabel('Recv(KB)')
        plt.ylim(ymin=0)
     
        plt.subplot(7, 1, 2)
        plt.plot(data['time'], data['txBytes'], '-', label=package_name_0)
        plt.plot(data0['time'], data0['txBytes'], 'r-', label=package_name_1)
        plt.plot(data1['time'], data1['txBytes'], 'g-', label=package_name_2)
        plt.legend()
        # plt.xlabel('Time')
        plt.ylabel('Send(KB)')
        plt.ylim(ymin=0)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
        # .clf()
     
        plt.subplot(7, 1, 3)
     
        plt.plot(data['time'], data['mem'], '-', label=package_name_0)
        plt.plot(data0['time'], data0['mem'], 'r-', label=package_name_1)
        plt.plot(data1['time'], data1['mem'], 'g-', label=package_name_2)
        plt.legend()
        plt.ylabel('mem(MB)')
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 4)
        plt.plot(data['time'], data['cpu'], '-', label=package_name_0)  #Cpu
        plt.plot(data0['time'], data0['cpu'], 'r-', label=package_name_1)
        plt.plot(data1['time'], data1['cpu'], 'g-', label=package_name_2)
        plt.legend()
        plt.ylim(0, max(100, data['systemCpu'].max()))
        plt.ylim(0, max(100, data0['systemCpu'].max()))
        plt.ylim(0, max(100, data1['systemCpu'].max()))
        plt.ylabel('CPU')
        plt.ylim(ymin=0)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 5)
        plt.plot(data['time'], data['fps'], '-', label=package_name_0)
        plt.plot(data0['time'], data0['fps'], 'r-', label=package_name_1)
        plt.plot(data1['time'], data1['fps'], 'g-', label=package_name_2)
        plt.legend()
        plt.ylabel('FPS')
        plt.ylim(-1, 100)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 6)
        plt.plot(data['time'], data['level'], '-', label=package_name_0)
        plt.plot(data0['time'], data0['level'], 'r-', label=package_name_1)
        plt.plot(data1['time'], data1['level'], 'g-', label=package_name_2)
        plt.legend()
        plt.ylabel('level')
        plt.ylim(0, 110)
        plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
     
        plt.subplot(7, 1, 7)
        plt.plot(data['time'], data['batterytem'], '-', label=package_name_0)
        plt.plot(data0['time'], data0['batterytem'], 'r-', label=package_name_1)
        plt.plot(data1['time'], data1['batterytem'], 'g-', label=package_name_2)
        plt.legend()
        plt.ylim(0, 100)
        plt.ylabel('BatteryTem')
        plt.xlabel('Time')
    else:
        print("not found file or limit 3 files!")
    #plt.savefig(os.path.join(target_dir, files[0].split("/")[-1].split('.')[0]+".png"))
    plt.savefig(os.path.join(target_dir, "app_info.png"))
def tets_iphone_info(src):
    data = pd.read_csv(src)
    iphone=(data['iphone_info'][0])
    return iphone
def tets_pack_info(src):
    data = pd.read_csv(src)
    pack=(data['package'][0]).replace(" ",'')
    return pack

    
if __name__ == '__main__':
#    src = input('请将csv文件拖入窗口，并点击回车！！！！！\n\n')
#    src = '20210517201749.csv'
#    src =(os.getcwd() + "/test_data/"+os.listdir((os.getcwd() + "/test_data"))[-1])
    dir_f = os.getcwd() + "/test_data/" + ".DS_Store"
    os.system("rm -r %s" %dir_f)
    files = os.listdir(os.getcwd() + "/test_data")
    files_list = []
    for i in range(0,len(files)):
        file = os.getcwd() + "/test_data/" + files[i]
        files_list.append(file)
    print(files_list)
    csv2images(files_list)
    #input(".............................")
