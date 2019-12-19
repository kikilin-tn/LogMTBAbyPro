import re
import datetime

logs = []
newlogs = []
outlogs = []
fullcut_time = None
MTBA = None
errtime = None

"""
Read LOG file
"""
filename = input('please input the file name(ex.LG07_0520.txt): ' )
#pro_id = input('please input the device name(ex.LG06-SN100-D-ASE-325-90-G-01):
#with open(filename,'r',encoding='latin1') as f:
with open(filename,'r') as f:
    for line in f:
        if line.find('PRO') != -1 or line.find('ERRSET') != -1 or line.find('FAS')!= -1 or line.find('FAE')!= -1:
        #if line.find('PRO') != -1 or line.find('ERRSET') != -1:
        #log_type = event[1]
        #error_number = event[2]
        #error_comment = event[3] #same as device id, ex:'2019/05/21 23:10:56', 'ERRSET', '39', 'K0039  切痕検査:偏離中心.'
            event = re.split(',|\t|\n', line)
            logs.append(event[0:6])
#    for line in logs:
#        print(line)
newlogs = logs[::-1]
with open('checkLOG.csv', 'w') as fcheck:
    for line in newlogs:
        fcheck.write(str(line) + '\n')
#for line in newlogs:
#    print(line)

fae_time = None
fas_time = None
for newline in newlogs:
    #log_type = newline[1]
    #error_number = newline[2]
    #error_comment = newline[3] #same as pro_id
    if newline[1] == 'FAS':
        print('fullcut start at ' + newline[0])
        pro_cnt = 0
        err40_cnt = 0
        fas_time = datetime.datetime.strptime(newline[0],'%Y/%m/%d %H:%M:%S')

    elif newline[1] == 'ERRSET' and newline[2] == '40': #K0040  切痕検査:太寛
        err40_cnt = err40_cnt + 1
        errtime = newline[0]
        print('"K0040  切痕検査:太寛" occurred at ' + str(errtime) + ' '+ str(err40_cnt) + ' times')
        #outlogs.append(newline)

    elif newline[1] == 'FAE':
        fae_time = datetime.datetime.strptime(newline[0],'%Y/%m/%d %H:%M:%S')
        #fullcut_time = fae_time - fas_time
        print('fullcut end at ' + newline[0])
        #print('自動加工所花費的時間為: ' + str(fullcut_time) + '\n')
