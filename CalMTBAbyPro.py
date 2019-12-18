import re
import time
import os

#os.system('pause')
logs = []
newlogs = []
outlogs = []

"""
Read LOG file
"""
filename = input('please input the file name(ex.LG07_0520.txt): ' )
pro_id = input('please input the device name(ex.LG06-SN100-D-ASE-325-90-G-01): ')

#with open(filename,'r',encoding='latin1') as f:
with open(filename,'r') as f:
    for line in f:
        #event=re.split(',|\t|\n',line)

        #if len(event) < 5:
            #continue
        #if line.find('PRO') != -1 or line.find('ERRSET') != -1 or line.find('FAS')!= -1 or line.find('FAE')!= -1:
        if line.find('PRO') != -1 or line.find('ERRSET') != -1:
        #log_type = event[1]
        #error_number = event[2]
        #error_comment = event[3] #same as device id, ex:'2019/05/21 23:10:56', 'ERRSET', '39', 'K0039  切痕検査:偏離中心.'
            event = re.split(',|\t|\n', line)
            logs.append(event[0:6])
    #for line in logs:
        #print(line)
newlogs = logs[::-1]

for line in newlogs:
    print(line)
pro_cnt = 0
err40_cnt = 0
for newline in newlogs:
    log_type = newline[1]
    error_number = newline[2]
    error_comment = newline[3] #same as pro_id

    if log_type == 'PRO' and error_comment == pro_id:
        pro_cnt = pro_cnt + 1
        #print(newline)
        outlogs.append(newline)
    elif log_type == 'ERRSET' and error_number == '40': #K0040  切痕検査:太寛
        err40_cnt = err40_cnt + 1
        outlogs.append(newline)
    # if log_type == 'FAS':
    #     err40_cnt = 0
    #     FAS_time = datetime.datetime.strptime(newline[0],'%Y,%m,%d %H:%M')
    # elif log_type == 'ERRSET' and error_number == '40': #K0040  切痕検査:太寛
    #      err40_cnt = err40_cnt + 1
    # elif log_type == 'FAE':
    #     FAE_time = datetime.datetime.strptime(newline[0],'%Y,%m,%d %H:%M')
    # print(FAE_time-FAS_time) #2019-12-10 16:34:00
    # print('MTBA: '+ (FAE_time-FAS_time)/err40_cnt)

print(pro_id + ' Device: ' + ' ' + str(pro_cnt)+ ' wafers are proceeded.')
print('Error code "K0040  切痕検査:太寛" occurred ' + str(err40_cnt) + ' times')

with open('renewLOG.csv', 'w') as fout:
    fout.writelines(pro_id + ' Device: ' + ' ' + str(pro_cnt)+ ' wafers are proceeded.\n')
    fout.writelines('Error code "K0040  切痕検査:太寛" occurred ' + str(err40_cnt) + ' times\n')
    for line in outlogs:
        fout.write(str(line) + '\n')
