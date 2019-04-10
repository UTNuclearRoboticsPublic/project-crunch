#!/usr/bin/env python3

import subprocess
import re

p1 = subprocess.Popen(['xrandr'], stdout=subprocess.PIPE)
opt, err = subprocess.Popen(['grep','2160x1200'], stdin=p1.stdout,stdout=subprocess.PIPE).communicate()
list_of_opt = opt.splitlines()
coords = []
for line in list_of_opt:
    line = line.decode("utf-8", "ignore")
    try:
        res_coords = re.search("\d+x\d+\+\d+\+\d+",line).group()
        _ , x, y = res_coords.split("+")
        coords.append((x,y))
    except:
        pass


print(coords)

# get HDMI/DP port ID using grep to find window position
windows = subprocess.Popen(["wmctrl","-l"],stdout=subprocess.PIPE)
hmd1, err = subprocess.Popen(['grep','HMD1'],
        stdin=windows.stdout,
        stdout=subprocess.PIPE).communicate()

wid1 = hmd1.split()[0]
print(wid1)

subprocess.call(["wmctrl","-ir",wid1,"-e","0,{},{},2160,1200".format(coords[0][0],coords[0][1])])

windows = subprocess.Popen(["wmctrl","-l"],stdout=subprocess.PIPE)
hmd2, err = subprocess.Popen(["grep","HMD2"],
        stdin=windows.stdout,
        stdout=subprocess.PIPE).communicate()

print(hmd2)
wid2 = hmd2.split()[0]

subprocess.call(["wmctrl","-ir",wid2,"-e","0,{},{},2160,1200".format(coords[1][0],coords[1][1])])
