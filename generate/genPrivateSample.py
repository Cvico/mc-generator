import os, sys, enum, argparse, random
from multiprocessing import Pool
import warnings as wr
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)


slurmscaff = 'sbatch {extraS} -p {queue} -J {jobname} {ncores} -e {logpath}/log.%j.%x.err -o {logpath}/log.%j.%x.out --wrap "{command}"'
commscaff  = "cmsRun /nfs/fanae/user/cvico/WorkSpace/ttw-differential/nanogenttw/CMSSW_12_0_2/src/ttw_fxfx.py {args}"
haddcomm   = "hadd {out} {inputs}"


nEvsPerJob  = 1000
nThreshold  = 400
random.seed = 859353    #

def generateNanoGEN(outpath, outnam, nthreads, nevents, queue, verbose, pretend, Eslurm, mode):
    if not os.path.isdir(outpath):
        os.system("mkdir -p " + outpath)
    workpath = outpath + "/workarea"
    if not os.path.isdir(workpath):
        os.system("mkdir -p " + workpath)

    #joboutpath = "../../"
    joboutpath = outpath

    if not queue:
        tmpworkpath = workpath + "/job0"
        if not os.path.isdir(tmpworkpath):
            os.system("mkdir -p " + tmpworkpath)
        comm = "cd " + tmpworkpath + "; " + commscaff.format(args = "outpath={o} outname={nam} nevs={n} ncores={j} seed={s}".format(
            o   = joboutpath,
            nam = outnam,
            n   = nevents,
            j   = nthreads,
            s   = random.randint(0, 65535))) + "; cd -;"

        if verbose:
            print("Command:", comm, "\n")

        if not pretend:
            outstat = os.system(comm)

    else:
        logpath = outpath + "/slurmlogs"
        if not os.path.isdir(logpath):
            os.system("mkdir -p " + logpath)

        #logpath = "../../slurmlogs"

        #if not nthreads:
        if nevents < nThreshold:
            for i in range(nevents):                     #### TODO: paralelizar
                tmpworkpath = workpath + "/job{i}".format(i = i)
                if not os.path.isdir(tmpworkpath):
                    os.system("mkdir -p " + tmpworkpath)

                comm = commscaff.format(args = "outpath={o} outname={nam} nevs={n} ncores={j} seed={s}".format(
                    o   = joboutpath,
                    nam = outnam.replace(".root", "_{i}.root".format(i = i)),
                    n   = 1,
                    j   = nthreads,
                    s   = random.randint(0, 65535)),
                    
                )
                slcomm = "cd " + tmpworkpath + "; " + slurmscaff.format(extraS  = Eslurm,
                                        queue   = queue,
                                        ncores  = "",
                                        jobname = "MCgen_{nam}_{n}_{i}".format(nam = outnam,
                                                                            n   = 1,
                                                                            i = i),
                                        logpath = logpath,
                                        command = comm) + "; cd -;"

                if verbose:
                    print("Command:", slcomm, "\n")

                if not pretend:
                    outstat = os.system(slcomm)
        else:
            nJobs = nevents // nEvsPerJob
            for i in range(nJobs):                     #### TODO: paralelizar
                tmpworkpath = workpath + "/job{i}".format(i = i)
                if not os.path.isdir(tmpworkpath):
                    os.system("mkdir -p " + tmpworkpath)

                comm = commscaff.format(args = "outpath={o} outname={nam} nevs={n} ncores={j} seed={s}".format(
                    o   = joboutpath,
                    nam = outnam.replace(".root", "_{i}.root".format(i = i)),
                    n   = nEvsPerJob if i != nJobs - 1 else nevents - nEvsPerJob * (nJobs - 1),
                    j   = nthreads,
                    s   = random.randint(0, 65535))
                )
                slcomm = "cd " + tmpworkpath + "; " + slurmscaff.format(extraS  = Eslurm,
                                        queue   = queue,
                                        ncores  = "-c " + str(nthreads) if nthreads > 1 else "",
                                        jobname = "MCgen_{nam}_{n}_{i}".format(nam = outnam,
                                                                                n   = nEvsPerJob if i != nJobs - 1 else nevents - nEvsPerJob * (nJobs - 1),
                                                                                i = i),
                                        logpath = logpath,
                                        command = comm) + "; cd -;"

                if verbose:
                    print("Toys GOF command:", slcomm, "\n")

                if not pretend:
                    outstat = os.system(slcomm)
                    if outstat:
                        raise RuntimeError("FATAL: Combine failed to execute for year {y} and region(s) {r} during the nominal GOF test fit execution.".format(y = year, r = region))


        #else:
            #tmpworkpath = workpath + "/job{i}".format(i = 0)
            #if not os.path.isdir(tmpworkpath):
                #os.system("mkdir -p " + tmpworkpath)
            #comm = commscaff.format(args = "outpath={o} outname={N} nevs={n} ncores={j}".format(o = joboutpath,
                                                                                    #nam = outnam,
                                                                                    #n = nevents,
                                                                                    #j = nthreads))
            #slcomm = "cd " + tmpworkpath + "; " + slurmscaff.format(extraS  = Eslurm,
                                       #queue   = queue,
                                       #ncores  = "-c " + str(nthreads),
                                       #jobname = "MCgen_{nam}_{n}".format(nam = outnam,
                                                                          #n   = nevents),
                                       #logpath = logpath,
                                       #command = comm) + "; cd -;"
            #if verbose:
                #print "Command:", slcomm, "\n"

            #if not pretend:
                #outstat = os.system(slcomm)
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = "python nanoAOD_checker.py [options]", description = "Checker tool for the outputs of nanoAOD production (NOT postprocessing)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--extraSlurm','-eS',metavar = 'extraslurm', dest = "extraslurm", required = False, default = "")
    parser.add_argument('--nthreads',  '-j', metavar = 'nthreads',   dest = "nthreads",   required = False, default = 0,    type = int)
    parser.add_argument('--nevents',   '-n', metavar = 'nevents',    dest = "nevents",    required = False, default = 1000, type = int)
    parser.add_argument('--pretend',   '-p', action  = "store_true", dest = "pretend",    required = False, default = False)
    parser.add_argument('--outpath',   '-o', metavar = 'outpath ',   dest = "outpath",    required = False, default = "output")
    parser.add_argument('--outname',   '-N', metavar = 'outname',    dest = "outname",    required = False, default = "TTWJetsToLNu_fxfxEWK.root")
    parser.add_argument('--queue',     '-q', metavar = 'queue',      dest = "queue",      required = False, default = None)
    parser.add_argument('--verbose',   '-V', action  = "store_true", dest = "verbose",    required = False, default = False)
    parser.add_argument('--mode',   '-m', dest = "mode", required = False, default = "new")

    args       = parser.parse_args()
    extraslurm = args.extraslurm
    nthreads   = args.nthreads
    nevents    = args.nevents
    pretend    = args.pretend
    outpath    = os.getcwd() + "/%s"%args.outpath
    queue      = args.queue
    verbose    = args.verbose
    outname    = args.outname
    mode       = args.mode

    generateNanoGEN(outpath, outname, nthreads, nevents, queue, verbose, pretend, extraslurm, mode)

