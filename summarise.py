#!/usr/bin/env python
'''
  summarise slurm job details
  Usage: summarise.py --files slurm-*.log > summary.tsv
  Time is in hours.
  Memory is in GB.
'''

#(venv_somatic_2) spartan-login1 18:48:20 msi-evaluation$ sacct -j 18860471  --format="JobName,CPUTime,MaxRSS,Elapsed,MaxVMSize,Timelimit"
#   JobName    CPUTime     MaxRSS    Elapsed  MaxVMSize  Timelimit
#---------- ---------- ---------- ---------- ---------- ----------
#    mantis   17:37:48              02:56:18              08:00:00
#     batch   17:37:48    733264K   02:56:18  47907692K
#    extern   17:37:48      1212K   02:56:18    144788K

import argparse
import logging
import subprocess
import sys

def to_hours(v):
  # d-hh:mm:ss or hh:mm:ss
  if '-' in v:
    d = float(v.split('-')[0])
    return 24 * d + to_hours(v.split('-')[1])
  else:
    h, m, s = [int(x) for x in v.split(':')]
    return h + m / 60 + s / 3600

def main(files):
  logging.info('starting...')

  sys.stdout.write('ID,Name,TimeRequested,TimeUsed,MemoryRequested,MemoryUsed\n')
  for f in files:
    logging.info('%s...', f)
    i = f.split('/')[-1].split('.')[0].split('-')[-1]
    output = subprocess.check_output("sacct -j {} -p --format JobName,Elapsed,MaxRSS,MaxVMSize,TimeLimit".format(i), shell=True).decode()
    lines = output.split('\n')
    jobname = lines[1].split('|')[0]
    time_requested = to_hours(lines[1].split('|')[4])
    time_used = to_hours(lines[2].split('|')[1])
    memory_used = float(lines[2].split('|')[2][:-1]) / 1024 / 1024
    memory_requested = float(lines[2].split('|')[3][:-1]) / 1024 / 1024

    sys.stdout.write('{},{},{:.1f},{:.1f},{:.1f},{:.1f}\n'.format(i, jobname, time_requested, time_used, memory_requested, memory_used))

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Slurm summariser')
  parser.add_argument('--files', required=True, nargs='+', help='files containing slurm ids')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  main(args.files)

