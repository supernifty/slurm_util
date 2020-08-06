# slurm_util
Scripts for analysing slurm jobs

## usage
```
python summarise.py --files log/slurm* > summary.csv
```

## suggested post processing
* sort on name to see which jobs have inappropriate walltime and/or memory requested

## suggested plot command

Using the following libraries
* https://github.com/supernifty/csvtools/
* https://github.com/supernifty/plotme/

```
csvfilter.py --filter 'TimeUsed>1' 'MemoryUsed>1' < summary.csv | python plotme/scatter.py --verbose --delimiter ',' --x TimeUsed --y MemoryUsed --z Name --z_color
```
