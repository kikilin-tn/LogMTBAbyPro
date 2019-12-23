import re
from datetime import datetime
import time

logs = []
newlogs = []
outlogs = []
fullcutReco = []
fullcut_time = None
MTBA = None
errtime = None
fae_time = None
fas_time = None
all_err_cnt = None
err_cnt = None

"""
Read LOG file
"""
filename = input('please input the file name(ex.LG07_0520.txt): ' )
#input_err_number = input('please input the error number you want to check or enter to check all.(ex: 40, for K0040  切痕検査:太寛): ')
#pro_id = input('please input the device name(ex.LG06-SN100-D-ASE-325-90-G-01):
#with open(filename,'r',encoding='latin1') as f:
with open(filename,'r', encoding='latin1') as f:
    # for line in f:
    #     if line.find('PRO') != -1 or line.find('ERRSET') != -1 or line.find('FAS')!= -1 or line.find('FAE')!= -1:
    #     #if line.find('PRO') != -1 or line.find('ERRSET') != -1:
    #         event = re.split(',|\t|\n', line)
    #         logs.append(event[0:6])
    # for line in logs:
    #     print(line)
#----------------------------
    for line in f:
        event=re.split(',|\t|\n',line)

        #if len(event) <3:
        #    continue
        #event[1] = event[1]
        if event[1] == 'PRO' or event[1] == 'ERRSET'or event[1] == 'FAS' or event[1] == 'FAE':
            logs.append(event[0:6])
#---------------------------
newlogs = logs[::-1]
#with open('checkLOG.csv', 'w',encoding = 'utf-8') as fcheck:
with open('checkLOG.csv', 'w', encoding='latin1') as fcheck:
    for line in newlogs:
        fcheck.write(str(line) + '\n')
#for line in newlogs:
#    print(line)

for newline in newlogs:
    #log_type = newline[1]
    #error_number = newline[2]
    #error_comment = newline[3] #same as pro_id ex:'2019/05/21 23:10:56', 'ERRSET', '39', 'K0039  切痕検査:偏離中心.'
    if newline[1] == 'FAS':
        #print('\n' + 'fullcut start at ' + newline[0])
        fullcutReco.append('\n' + 'fullcut start time: ' + newline[0])
        pro_cnt = 0
        all_err_cnt = 0
        err_cnt = 0
        fas_date = str(newline[0])
        fas_time = datetime.strptime(fas_date,'%Y/%m/%d %H:%M:%S')
        #print('fas:' + str(fas_time))

     # elif newline[1] == 'ERRSET' and newline[2] == '40': #K0040  切痕検査:太寛
     #     err_cnt = err_cnt + 1
     #     errtime = newline[0]
     #     print('"K0040  切痕検査:太寛" occurred at ' + str(errtime) + ' '+ str(err_cnt) + ' times')
    # elif newline[1] == 'ERRSET' and input_err_number == '': #對應所有error code
    #     all_err_cnt = all_err_cnt + 1
    #     errtime = newline[0]
    #     print(newline[3] + ' occurred at ' + str(errtime) + ' '+ str(all_err_cnt) + ' times')
    #     fullcutReco.append(newline[3] + ' occurred at ' + str(errtime) + ' '+ str(all_err_cnt) + ' times')

    elif newline[1] == 'ERRSET': #對應所有error code
        all_err_cnt = all_err_cnt + 1
        errtime = newline[0]
        #print(newline[3] + ' occurred at ' + str(errtime) + ' '+ str(all_err_cnt) + ' times')
        fullcutReco.append(newline[3] + ' occurred at ' + str(errtime) + ' '+ str(all_err_cnt) + ' times')
    # elif newline[1] == 'ERRSET' and newline[2] == input_err_number:
    #     err_cnt = err_cnt + 1
    #     errtime = newline[0]
    #     print(newline[3] + ' occurred at ' + str(errtime) + ' '+ str(err_cnt) + ' times')
    #     fullcutReco.append(newline[3] + ' occurred at ' + str(errtime) + ' '+ str(err_cnt) + ' times')
    elif newline[1] == 'FAE':
        fae_date = str(newline[0])
        fae_time = datetime.strptime(fae_date,'%Y/%m/%d %H:%M:%S')
        #print('fae:' + str(fae_time))
        if fas_time == None:
            continue
        else:
            fullcut_time = fae_time - fas_time
            #print(fullcut_time)
        #print('fullcut end time: ' + newline[0])
        fullcutReco.append('fullcut end at ' + newline[0])
        #print('自動加工所花費的時間為: ' + str(fullcut_time) + '即為 '+ str(fullcut_time.seconds) + '秒')
        fullcutReco.append('total full cut time: ' + str(fullcut_time) + ', '+ str((fullcut_time.seconds)/3600) + ' hrs')
        #print('MTBA: ' + str(all_err_cnt/(fullcut_time.seconds)))
        if all_err_cnt == 0:
            continue
        else:
            fullcutReco.append('MTBA: ' + str(((fullcut_time.seconds)/3600)/all_err_cnt) + ' (hrs)')

        # if input_err_number == newline[2]:
        #     print('MTBA: ' + str(err_cnt/(fullcut_time.seconds)))
        # else:
        #     print('MTBA: ' + str(all_err_cnt/(fullcut_time.seconds)))
#with open('outputLOG.csv', 'w', encoding = 'utf-8') as fout:
with open('outputLOG.csv', 'w', encoding='latin1') as fout:
    for line in fullcutReco:
        fout.write(line + '\n')
print('\nThe file is output. Please check "outputLOG.csv" file to get MTBA result.')
time.sleep(3)
