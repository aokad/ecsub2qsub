# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 19:31:13 2022

@author: aokada
"""

import sys
import os
import shutil
import string
import random
import time
import subprocess
import ecsub2qsub.tools

def read_tasksfile(tasks_file, cluster_name):
    
    tasks = []
    header = []

    for line in open(tasks_file).readlines():
        text = line.rstrip("\r\n")
        if len(text.rstrip()) == 0:
            continue
        if header == []:
            if text.startswith("#"):
                continue
            for item in text.split("\t"):
                v = item.strip(" ").split(" ")
                if v[0] == "":
                    header.append({"type": "", "recursive": False, "name": ""})
                
                elif v[0].lower() == "--env":
                    header.append({"type": "env", "recursive": False, "name": v[-1]})
                elif v[0].lower() == "--secret-env":
                    header.append({"type": "secret-env", "recursive": False, "name": v[-1]})
                elif v[0].lower() == "--input-recursive":
                    header.append({"type": "input", "recursive": True, "name": v[-1]})
                elif v[0].lower() == "--input":
                    header.append({"type": "input", "recursive": False, "name": v[-1]})
                elif v[0].lower() == "--output-recursive":
                    header.append({"type": "output", "recursive": True, "name": v[-1]})
                elif v[0].lower() == "--output":
                    header.append({"type": "output", "recursive": False, "name": v[-1]})
                else:
                    print (ecsub2qsub.tools.error_message (cluster_name, None, "type %s is not support." % (v[0])))
                    return None
            continue
        
        items = text.split("\t")
        for i in range(len(items)):
            if header[i]["type"] in ["input", "output"]:
                if items[i] == "":
                    continue
                if not items[i].startswith("s3://"):
                    print (ecsub2qsub.tools.error_message(cluster_name, None, "'%s' is invalid S3 path." % (items[i])))
                    return None
            
        tasks.append(items)

    return {"tasks": tasks, "header": header}

def write_scripts(task_params, wdir, script, singularity_path, singularity_option, image):
    run_template = """#!/bin/bash
#
# Set SGE
#
#$ -S /bin/bash         # set shell in UGE
#$ -cwd                 # execute at the submitted dir
#$ -e {log_path}
#$ -o {log_path}

set -x

{env_text}
{singularity_path} exec {singularity_option} {image} bash {script_run_path}
"""
    script_pathes = []
    for no in range(len(task_params["tasks"])):
        env_text = ""
        for i in range(len(task_params["tasks"][no])):
            env_text += 'export %s="%s"\n' % (task_params["header"][i]["name"], task_params["tasks"][no][i])

        runsh = wdir + "/script/run.%d.sh" % (no)
        open(runsh, "w").write(run_template.format(
            env_text = env_text,
            script_run_path = script,
            log_path = wdir + "/log/",
            singularity_path = singularity_path,
            singularity_option = singularity_option,
            image = image,
        ))
        script_pathes.append(runsh)
    return script_pathes

def subprocess_call (cmd, cluster_name):
    subprocess.run(cmd, shell=True, check=True)

def main(params):

    # set cluster_name
    params["cluster_name"] = params["task_name"]
    if params["cluster_name"] == "":
        params["cluster_name"] = os.path.splitext(os.path.basename(params["tasks"]))[0].replace(".", "_") \
            + '-' \
            + ''.join([random.choice(string.ascii_letters + string.digits) for i in range(5)])
            

    # read tasks file
    task_params = read_tasksfile(params["tasks"], params["cluster_name"])
    if task_params == None:
        return 1
    
    if task_params["tasks"] == []:
        print (ecsub2qsub.tools.info_message (params["cluster_name"], None, "task file is empty."))
        return 0
    
    subdir = params["cluster_name"]
    
    params["wdir"] = params["wdir"].rstrip("/") + "/" + subdir
    
    if os.path.exists (params["wdir"]):
        shutil.rmtree(params["wdir"])
        print (ecsub2qsub.tools.info_message (params["cluster_name"], None, "'%s' existing directory was deleted." % (params["wdir"])))
        
    os.makedirs(params["wdir"])
    os.makedirs(params["wdir"] + "/log")
    os.makedirs(params["wdir"] + "/script")

    # write task-scripts, and upload to S3
    script_pathes = write_scripts(
        task_params, 
        params["wdir"], 
        params["script"],
        params["singularity_path"],
        params["singularity_option"],
        params["image"],
     )

    # run purocesses
    try:
        for script in script_pathes:
            cmd = "set -x; qsub %s %s" % (params["qsub_option"], script)
            subprocess_call (cmd, params["cluster_name"])

        print ("ecsub2qsub completed successfully!")
        return 0
        
    except Exception as e:
        print (e)
        
    except KeyboardInterrupt:
        print ("KeyboardInterrupt")
    
    print ("ecsub2qsub failed.")
    return 1

def set_param(args, env_options = None):
    
    default = Argments()
    
    params = {}
    for key in default.__dict__.keys():
        params[key] = default.__dict__[key]
    
    for key in args.__dict__.keys():
        params[key] = args.__dict__[key]
    
    return params

def entry_point(args):
    
    params = set_param(args)
    return main(params)

class Argments:
    def __init__(self):
        self.wdir = "./"
        self.image = ""
        self.script = ""
        self.tasks = ""
        self.task_name = ""
        self.singularity_path = "singularity"
        self.singularity_option = ""
        self.qsub_option = ""
        
if __name__ == "__main__":
    pass

