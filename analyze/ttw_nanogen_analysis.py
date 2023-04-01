# -- Import libraries -- #
import ROOT as r
import numpy as np
from framework.ttw_analysis import ttw_analysis
from framework.canvas import canvas
import json
from copy import deepcopy
import os
from optparse import OptionParser
import multiprocessing as mp

# -- Define functions -- #
def add_parsing_opts():
  """ Function with base parsing arguments used by any script """
  parser = OptionParser(usage = "python nanogen_analysis.py [options]", 
                        description = "Main options for running nanogen analysis") 
  parser.add_option("--inputFolder", dest = "inputFolder", default = "files_sergio",
              help = "Input folder to run the analysis.")
  parser.add_option("--nEvents", dest = "nEvents", type=int, default = 290000,
              help = "Number of events to process.")
  parser.add_option("--outpath", dest = "outpath", default = "outfiles",
              help = "Number of events to process.")
  parser.add_option("--verbosity", "-v", dest = "verbosity", type=int, default = 0,
              help = "Verbosity control.")
  return parser

def multiproc(submitter, args, njobs):
  """ For submitting parallel jobs """
  with mp.Pool(processes = njobs) as pool:
    pool.map(submitter, args)
  return

def submit(args):
  analysis = ttw_analysis(*args)
  analysis.loop()
  analysis.save_in_tree()
  return

if __name__ == "__main__":
  # -- Read json with sample configurations -- #
  parser = add_parsing_opts()
  
  (opts, args) = parser.parse_args()
  
  # Create the output path if it does not exist
  if not os.path.exists(opts.outpath):
    os.system("mkdir -p %s"%opts.outpath)
    
  files_ = os.listdir(opts.inputFolder)
  njobs = len(files_)
  
  multiproc( submit, ((opts, f) for f in files_), njobs )
        
  



