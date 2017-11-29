import datetime
import os
import glob


## Parser Lib
import json
import csv
import re
# from konlpy.tag import Mecab
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from matplotlib import animation
from collections import deque
import random
from datetime import datetime, timedelta

## Data Structure
from collections import defaultdict
import random
import math
import numpy as np
import time
## Output
import pprint
id_dict={}

def print_timestamp(prev,idx,timestamp,type):

    if (prev['start']['idx'] +1 == idx) and (prev['start']['type'] == type):
        prev['start']['idx'] = prev['start']['idx'] + 1
        prev['end']['timestamp'] = timestamp

    else:
        #print("%.6f","%.6f","%s",prev['start']['timestamp'],prev['end']['timestamp'],prev['start']['type'])
        #print('{0:.6f},'.format(prev['start']['timestamp']),'{0:.6f},'.format(prev['end']['timestamp']),prev['start']['type'])
        #plot graph here
        print(datetime.fromtimestamp(int(prev['start']['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')," 부터 ",datetime.fromtimestamp(int(prev['end']['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')," 까지 ", prev['start']['type'], " 공격 발생 " )

        prev['start']['idx'] = idx
        prev['start']['timestamp'] = timestamp
        prev['start']['type'] = type
        prev['end']['idx'] = idx
        prev['end']['timestamp'] = timestamp
        prev['end']['type'] = type



def calculate_freq_mean(id,freq):

    id_dict[id]['freq']['cnt'] = id_dict[id]['freq']['cnt'] + 1
    id_dict[id]['freq']['freq'] = freq
    cnt = id_dict[id]['freq']['cnt']
    id_dict[id]['freq']['mean'] = (id_dict[id]['freq']['freq']+(id_dict[id]['freq']['mean']*(cnt-1)))/cnt

def main():
    global prev
    prev = {}
    prev['start']={}
    prev['end']={}

    prev['start']['idx']=0
    prev['start']['timestamp'] = 0
    prev['start']['type'] = 'UNKOWN'
    prev['end']['idx']=0
    prev['end']['timestamp'] = 0
    prev['end']['type'] = 'UNKOWN'

    with open("CAN_Dataset.txt", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=" ", quoting=csv.QUOTE_NONE)
        for idx, row in enumerate(csv_reader):
            #if idx%100000 == 0:
            #    print(idx)
            time.sleep(0.0001)
            #print(row[1],row[10],row[14],row[19])
            timestamp=float(row[1])
            id = row[10]
            rtr = row[14]
            dlc = row[19]
            data = str(row[23:30])


            if(id == '0000'):
                #print(idx,freq, freq_mean, "DoS", row)
                print_timestamp(prev, idx, timestamp, "DoS")
                continue

            if id not in id_dict:
                id_dict[id] = {}
                id_dict[id]['freq'] = {}
                id_dict[id]['freq']['freq'] = 0
                id_dict[id]['freq']['mean'] = 0
                id_dict[id]['freq']['cnt'] = 0

            #freq = timestamp - id_dict.get(id,0)['last']

            if 'last' in id_dict[id]:
                freq = timestamp - id_dict[id]['last']

                freq_mean = id_dict[id]['freq']['mean']
                #freq_sigma = np.std(id_dict[id]['freq'])

                #if idx > 100000:
                if id_dict[id]['freq']['cnt'] > 5:

                    if freq < freq_mean*(0.5):
                        #print(freq,freq_mean,"fuzzy attack: ",timestamp,id,rtr,dlc,row)
                        if data == "['00', '00', '00', '00', '00', '00', '00']":
                            #print(idx,freq,freq_mean,"DoS",row)
                            print_timestamp(prev, idx, timestamp, "DoS")
                        else:
                            #print(idx,freq,freq_mean,"Fuzzy",row)
                            print_timestamp(prev, idx, timestamp, "Fuzzy")

                            #continue
                    else:
                        calculate_freq_mean(id, freq)

                else:
                    calculate_freq_mean(id, freq)

            id_dict[id]['last'] = timestamp

            #if idx %10000 == 0:
            #print(timestamp,id,rtr,dlc)


if __name__ == '__main__':
    main()