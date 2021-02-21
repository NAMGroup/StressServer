from typing import Optional

from fastapi import FastAPI, Request
from fastapi import BackgroundTasks
from starlette.responses import RedirectResponse

import subprocess
import time
import random

import os


import requests

app = FastAPI()

REDIRECT_TO=None

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))




@app.on_event("startup")
async def startup_event():
    print("Do something on startup")
    _getTargets()


@app.get("/")
def root( request: Request):
    return {"ZSM": "PoC"}


def _getTargets():
    targets=list()
    print(os.path.abspath(os.getcwd()))
    try:
        targets_file = open('./targets.txt', 'r')
        targets = targets_file.read().splitlines()

    except OSError:
        print ("Could not open/read targets file:")
    print(len(targets))
    print(targets)
    return targets

def _redir( params: str):
    print("START REDIR")
    targets=list()
    print(os.path.abspath(os.getcwd()))
    # Using readlines()
    try:
        targets_file = open('./targets.txt', 'r')
        #targets = targets_file.readlines()
        targets = targets_file.read().splitlines()

    except OSError:
        print ("Could not open/read targets file:")
    print(len(targets))
    print(targets)

    for target in targets:
        x = requests.get(target)
        print(x.status_code)
        print("-->",x,"<--")
  

    print("END REDIR")


def _stress(cpus: int, duration: int):
    print("START")
    stress_cmd = subprocess.run(["stress-ng", "--cpu", str(cpus), "--timeout",str(duration)])
    print("END")


@app.get("/stress",summary="Stress CPU", description="Stress cpu. Parameters are cpu for number of cpus (1-12 cpus) to be stressed and time for duration(1-100 seconds).")
def bstress(request: Request,background_tasks: BackgroundTasks, cpu: Optional[int]=1, duration: Optional[int] = 10, redir: Optional[int] = 0,):
    global REDIRECT_TO
    if cpu<1:
        cpu=1
    if cpu>12:
        cpu=1
    if duration<1:
        duration=10
    if duration>100:
        duration=10
    background_tasks.add_task(_stress, cpu,duration)
    if redir!=0:
        background_tasks.add_task(_redir, "some params")
    return {"cpu": cpu, "duration": duration}



@app.get("/stress_random",summary="Stress CPU", description="Stress cpu. Random number of cpus will be hogged (2-8) for random time (10-30 secs).")
def brstress(request: Request,background_tasks: BackgroundTasks, cpu: Optional[int]=1, duration: Optional[int] = 10):
    global REDIRECT_TO
    cpu=random.randint(2,8)
    duration=random.randint(10,30)
    print("-->",REDIRECT_TO,"<--")
 #   stress_cmd = subprocess.run(["stress-ng", "--cpu", str(cpu), "--timeout",str(time)])
    background_tasks.add_task(_stress, cpu,duration)
    if REDIRECT_TO != None:
        params = str(request.query_params)
        print("HERE")
        url = f'{REDIRECT_TO}/browser_stress_random/?{params}'
        response = RedirectResponse(url=url)
        return response
        
    return {"cpu": cpu, "duration": duration}    


@app.get("/redir",summary="Redirection", description="Test redirection")
def redir(request: Request,background_tasks: BackgroundTasks):
    print("REDIT TEST")
    background_tasks.add_task(_redir, "some params")
    return ("REDIR TEST")