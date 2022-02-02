![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue.svg)

# ecsub2qsub

## 1. Dependency

 - qsub (submit a batch job command to Univa Grid Engine)

## 2. Install

```
git clone https://github.com/aokad/ecsub2qsub.git
cd ecsub2qsub
python3 setup.py install
```

## 3. Usage

```
ecsub2qsub submit \
 --script ./examples/un-wordcount.sh \
 --tasks ./examples/tasks-wordcount.tsv \
 --wdir ./output \
 --image /path/to/images/python3.sif \
 --qsub-option "-l s_vmem=2G"
 ```
 
