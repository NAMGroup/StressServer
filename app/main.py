from typing import Optional

from fastapi import FastAPI, Request
from fastapi import BackgroundTasks
from starlette.responses import RedirectResponse

import subprocess
import time
import random

import os

from random import randrange
import requests

app = FastAPI()

REDIRECT_TO=None

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))




@app.on_event("startup")
async def startup_event():
    print("Do something on startup")

    val,target1,target2= _checkTargets()
    if val is None:
        print("Target.txt NOT valid")
    else:
        print("Target.txt looks valid")
        print("FORWARD POSS-->", val)
        print("TARGET1-->", target1)
        print("TARGET2-->", target2)





@app.get("/")
def root( request: Request):
    return {"ZSM": "PoC"}



def _checkTargets():
    targets=_getTargets()
    list_size=len(targets)
    if list_size==0:
        print("NO TARGET!")
        return None, None, None
    elif list_size==1:
        if targets[0].isdigit():
            print("Just a  number with no target.")
            print("No idea what to do!")
            return None, None, None
        else:
            print("First/third layer of WEBSERVER.")
            print("Will forward to next (single) target ")
            print("Poss:-->",100)
            print("Target:-->",targets[0])
            return 100, targets[0], None
    elif list_size==2:
        if targets[0].isdigit():
            print("First/third layer of WEBSERVER.")
            print("Will forward to next (single) target ")
            print("Poss:-->",int(targets[0]))
            print("Target:-->",targets[1])
            return int(targets[0]), targets[1], None
        else:
            print("Second layer.")
            print("Will default poss to 90%")
            print("Target1:-->",targets[0])
            print("Target2:-->",targets[1])
            return 90, targets[0], targets[1]
    elif list_size==3:
        if targets[0].isdigit():
            print("Seconf layer of WEBSERVER.")
            print("Will forward to next (single) target ")
            print("Poss:-->",int(targets[0]))
            print("Target1:-->",targets[1])
            print("Target2:-->",targets[2])
            return int(targets[0]), targets[1], targets[2]
        else:
            print("Not valid.")
            return None, None, None
    else:
        print("Ooops")
        return None, None, None

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

def _redir( target:str, get_req: str,action:str):
    print("START REDIR")
 
    
    ft=target+action+"?"+str(get_req.query_params)
    print("----->",ft,"<------")
    x = requests.get(ft)
    print(x.status_code)
    print("-->",x,"<--")

    print("END REDIR")


def _stress(cpus: int, duration: int):
    print("START")
    stress_cmd = subprocess.run(["stress-ng", "--cpu", str(cpus), "--timeout",str(duration)])
    print("END")


def _decide_forward(val:int, tar1:str,tar2:str, redir:int):
    forward = True 
    final_destination=tar1
    random_num=randrange(100)
    if tar2 is None: #this μeans we can have one target (so either 1 or 3 layer)
        if redir==0: #check val for possibility to forward
            print(random_num, val)    
            if random_num<=val:
                print("WILL  FORWARD")
                final_destination=tar1
            else:
                print("WILL NOT FORWARD")
                forward=False
    else: #use the val to select target
        print(random_num, val)    
        if random_num<=val:
            print("WILL GO TO TARGET 1")
        else:
            print("WILL GO TO TARGET 2")
            final_destination=tar2
    return forward, final_destination



'''
if override ==-1 do not forward at all
if override ==0  forward depending on value
otherwise forward at all times
'''
@app.get("/stress",summary="Stress CPU", description="Stress cpu. Parameters are cpu for number of cpus (1-12 cpus) to be stressed and time for duration(1-100 seconds).")
def bstress(request: Request,background_tasks: BackgroundTasks, cpu: Optional[int]=1, duration: Optional[int] = 10, override: Optional[int] = 0):
    if cpu<1:
        cpu=1
    if cpu>12:
        cpu=1
    if duration<1:
        duration=10
    if duration>100:
        duration=10
    val,target1,target2= _checkTargets()
  
    print(request.url)

   
    if val is None:
        print("Target.txt NOT valid")
        print("NO FORWARD")
    else:
        if override==-1:
            print("Do not forward")
        else:
            print("WILL (propably) FORWARD")
            forw,targ=_decide_forward( val,target1,target2,override)
            if forw is True:
                get_req=request
                background_tasks.add_task(_redir, targ,get_req, "stress")
    background_tasks.add_task(_stress, cpu,duration)
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