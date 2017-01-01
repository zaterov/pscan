#!/usr/bin/env python3

import os
import random
import subprocess
import argparse
import time


def get_vids(base, viddirs):
   found = []
   for vd in viddirs:
       top = os.path.join(base, vd)
       for root, dirs, files in os.walk(top, topdown=False):
           for f in files:
               if f.endswith(('mp4', 'm4v', 'mpg', 'mpeg', 'divx', 'mov','avi', 'wmv', 'flv')):
                   found.append(os.path.join(root, f))

   random.shuffle(found)
   return found
   '''
   for vid in found[0:10]:
       play(vid)
   '''

def get_last_played():
        with open('/tmp/pscan.log', 'r') as t:
            last_vid = t.readline()
            print('replaying {}'.format(last_vid))
            return last_vid

def grep_vids(vids, args):
    matches = []
    s = ".*".join(args)
    print("pattern args: {}".format(s))

    import re
    rx = re.compile(s)
    print('\n')
    for f in vids:
        if re.search(rx, f):
            print('found {}'.format(f))
            matches.append(f)

    print('\n')
    time.sleep(5)
    return matches

def annotate(vid):
    prompt = '''    1)  PE:  perfect ending
    2) COT: cum on tits
    3)  NF:  nice feet
    4)  replay
    XXX : delete file    
    '''

    r = input(prompt)

    if r == str(1):
        pre = "PE_"
    elif r == str(2):
        pre = "COT_"
    elif r == str(3):
        pre = "NF_"
    elif r == str(4):
        play(get_last_played(), 'True')
    elif r == "XXX":
        pre = ''
        print("removing {}".format(vid))
        try:
            #  os.remove(vid)
            pass
        except:
            print("unable to remove {}".format(vid))
    else:
        print("input not recognized")

    path, old = os.path.split(vid)
    new = pre + old
    print("{}  ->  {}".format(old, new))
    try:
        os.rename(vid, os.path.join(path, new))
    except:
        print("problem renaming {}".format(vid))



def play(vid, last = 'False'):
    with open('/tmp/pscan.log', 'w') as t:
        t.write(vid)
    print('selection: {}'.format(vid))

    try:
        args = [ 'cvlc', "-f", vid ]
    #  args = [ 'echo', "-e", "\nwould be playing " + vid ]
        p = subprocess.call(args)
    except:
        print("caught cvlc error")

    if last == 'True':
        print("exiting: single play mode")
        quit()


    pe = input("further action required?(y/[*])")
    if pe.lower() == "y":
        annotate(vid)

    d = input("quit? (q/[*])")
    if d.lower() == "q":
        quit()


if __name__ == "__main__":
    TOPDIR =  '/media/vic/44c6b850-c884-4945-9799-9867dddb0949'
    VIDDIRS = [ os.path.join(TOPDIR, 'Brazzers'), 
            os.path.join(TOPDIR, 'sports/hockey')]

    #  VIDDIR  = '/mnt/T2-1/sports/hockey'

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--search', dest="find", 
                        action='append', help='search term')
    parser.add_argument('-p', '--previous', dest="last", 
                        action='store_true',  help='last played')
    args = parser.parse_args()

    if os.path.ismount(TOPDIR):
        vids_available = get_vids(TOPDIR, VIDDIRS)

    if args.find:
        print("see find pattern as {}".format(args.find))
        vids_to_play = grep_vids(vids_available, args.find)
    elif args.last:
            play(get_last_played(), 'True')
            quit()
    else:
        vids_to_play = vids_available

    for vid in vids_to_play:
        play(vid)



