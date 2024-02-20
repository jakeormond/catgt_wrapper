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

    # order the folders by the g value
    g_vals = {}
    for f, ff in enumerate(recordingfolders):
        idx2 = ff.rfind('g')
        gvalue = ff[idx2+1:]
        g_vals[ff] = int(gvalue)
    
    recordingfolders = [k for k, v in sorted(g_vals.items(), key=lambda item: item[1])]
    for r in recordingfolders:
        print(r)
    
    for f, ff in enumerate(recordingfolders):
        rundir = os.path.split(ff)[1]
        # find the final underscore in the folder name
        idx1 = rundir.rfind('_')        
        rundir = rundir[:idx1]

        # find the final g in the folder name
        idx2 = ff.rfind('g')
        gvalue = ff[idx2+1:]
        
        command = catgtcmd + ' -dir=' + basefolder + ' -run=' + rundir + ' -g=' + gvalue + ' -t=0 -ap -t_miss_ok -prb_fld -prb=0'
        command = command + ' -apfilter=butter,12,300,9000 -gbldmx -gfix=0.4,0.1,0.02 -xd=2,0,-1,6,0 -dest=D:/CatGT_output'
        print(command)

        # check if the output folder exists
        output_folder = catgt_output_dir + '/' + 'catgt_' + os.path.split(ff)[1]
        if not os.path.exists(output_folder):
            if runcatGT:
                runprocess(command)

        supercatpath = '{' + catgt_output_dir + ',' + 'catgt_' + os.path.split(ff)[1] + '}'
        supercatcmd = supercatcmd + supercatpath

    return supercatcmd


def supercat(supercatcmd, runsupercat=True):
    catgtcmd = 'C:/Users/Jake/Documents/CatGT-win/CatGT.exe'
    supercat_dir = 'D:/supercat'
    supercatcmd = catgtcmd + ' -t=cat -no_run_fld -ap -prb=0 -xd=2,0,-1,6,0 ' + supercatcmd + ' -dest=' + supercat_dir

    if runsupercat:
        runprocess(supercatcmd)

    print(supercatcmd)


if __name__ == "__main__":
    
    raw_data_path = 'D:/rawData/Rat46/19-02-2024'
    supercatcmd = catgt(raw_data_path, runcatGT=True)
    supercat(supercatcmd, runsupercat=True)

    raw_data_path = 'D:/rawData/Rat46/17-02-2024'
    supercatcmd = catgt(raw_data_path, runcatGT=False)
    supercat(supercatcmd, runsupercat=True)
