import subprocess
import os
import glob
import time
import numpy as np


def main(basefolder, tprimesavefolder, runcatGT=True, runsupercat=True, runtprime=True):
    supercatcmd = catgt(basefolder, runcatGT=runcatGT)
    supercat(basefolder, supercatcmd, runsupercat=runsupercat)
    tprime(basefolder, tprimesavefolder, runtprime=runtprime, runsupercat=runsupercat)


def runprocess(command):
    start = time.time()
    subprocess.Popen(command, shell='False').wait()
    execution_time = time.time() - start
    print('completed: ' + str(np.around(execution_time, 2)) + ' s')


def catgt(basefolder, runcatGT=True):
    recordingfolders = glob.glob(basefolder + '/*_g*')
    catgtcmd = 'C:/CatGT_newversion/CatGT'
    supercatcmd = '-supercat='

    for f, ff in enumerate(recordingfolders):
        rundir = os.path.split(ff)[1]
        rundir = rundir[:-3]
        gvalue = ff[-1]
        command = catgtcmd + ' -dir=' + basefolder + ' -run=' + rundir + ' -g=' + gvalue + ' -t=0 -ap -ni -prb_fld -prb=0'
        command = command + ' -apfilter=butter,12,300,9000 -loccar_um=200,400 -gfix=0.4,0.1,0.02 -xid=0,0,0,1,0'
        print(command)

        if runcatGT:
            runprocess(command)

        supercatpath = '{' + basefolder + ',' + os.path.split(ff)[1] + '}'
        supercatcmd = supercatcmd + supercatpath

    return supercatcmd


def supercat(basefolder, supercatcmd, runsupercat=True):
    catgtcmd = 'C:/CatGT_newversion/CatGT'
    supercatcmd = catgtcmd + ' -t=cat -prb_fld -ap -prb=0 -no_auto_sync ' + supercatcmd + ' -dest=' + basefolder

    if runsupercat:
        runprocess(supercatcmd)

    print(supercatcmd)


def tprime(basefolder, savefolder, runtprime=True, runsupercat=True):
    tprimecmd = 'C:/TPrime/TPrime'
    recordingfolders = glob.glob(basefolder + '/*_g*')

    if runsupercat:
        recordingfolders = recordingfolders[:-1]

    for f, ff in enumerate(recordingfolders):
        foldername = os.path.split(ff)[1]
        foldername = foldername+'_imec0'
        spikeglxsync = glob.glob(ff+'/'+foldername+'/*500.txt')[0]
        nisync = glob.glob(ff+'/*500.txt')[0]
        nicamsync = glob.glob(ff+'/*xid*txt')[0]
        savefile = savefolder+foldername[:-6]+'_spikeglx.txt'
        command = tprimecmd + ' -syncperiod=1.0 -tostream=' + spikeglxsync + ' -fromstream=1,' + nisync + ' -events=1,' + nicamsync + ',' + savefile
        print(command)

        if runtprime:
            runprocess(command)
