import subprocess
import os
import glob
import time
import numpy as np


def main(basefolder, tprimesavefolder, runcatGT=True, runsupercat=True, runtprime=True):
    supercatcmd = catgt(basefolder, runcatGT=runcatGT)
    supercat(basefolder, supercatcmd, runsupercat=runsupercat)
    # tprime(basefolder, tprimesavefolder, runtprime=runtprime, runsupercat=runsupercat)


def runprocess(command):
    start = time.time()
    subprocess.Popen(command, shell='False').wait()
    execution_time = time.time() - start
    print('completed: ' + str(np.around(execution_time, 2)) + ' s')


def catgt(basefolder, runcatGT=True):
    recordingfolders = glob.glob(basefolder + '/*_g*')
    print(recordingfolders)
    # catgtcmd = 'C:/CatGT_newversion/CatGT'
    catgtcmd = 'C:/Users/Jake/Documents/CatGT-win/CatGT.exe'
    supercatcmd = '-supercat='
    catgt_output_dir = 'D:/CatGT_output'

    for f, ff in enumerate(recordingfolders):
        rundir = os.path.split(ff)[1]
        rundir = rundir[:-3]
        gvalue = ff[-1]
        command = catgtcmd + ' -dir=' + basefolder + ' -run=' + rundir + ' -g=' + gvalue + ' -t=0 -ap -t_miss_ok -prb_fld -prb=0'
        command = command + ' -apfilter=butter,12,300,9000 -gbldmx -gfix=0.4,0.1,0.02 -xd=2,0,-1,6,0 -dest=D:/CatGT_output'
        print(command)

        #if runcatGT:
        #      runprocess(command)

        supercatpath = '{' + catgt_output_dir + ',' + os.path.split(ff)[1] + '}'
        supercatcmd = supercatcmd + supercatpath

    return supercatcmd


def supercat(supercatcmd, runsupercat=True):
    catgtcmd = 'C:/Users/Jake/Documents/CatGT_win/CatGT'
    supercat_dir = 'D:/supercat'
    supercatcmd = catgtcmd + ' -t=cat -no_run_fld -ap -prb=0 -xd=2,0,-1,6,0 ' + supercatcmd + ' -dest=' + supercat_dir

    if runsupercat:
        runprocess(supercatcmd)

    print(supercatcmd)


if __name__ == "__main__":
    raw_data_path = 'D:/rawData/Rat64-08-11-2023'
    supercatcmd = catgt(raw_data_path, runcatGT=True)
    supercat(supercatcmd, runsupercat=True)
