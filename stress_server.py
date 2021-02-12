from typing import Optional

from fastapi import FastAPI
from fastapi import BackgroundTasks

import subprocess
import time
import random


app = FastAPI()


@app.get("/")
def root():
    return {"ZSM": "PoC"}





def _stress(cpus: int, duration: int):
    print("START")
#    time.sleep(20)
    stress_cmd = subprocess.run(["stress-ng", "--cpu", str(cpus), "--timeout",str(duration)])
    print("END")

#@app.post("/send-notification/{email}")
#@app.post("/stress")
@app.get("/test")
async def test(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
    else:
        message = "NO DATA:"
    background_tasks.add_task(_stress, 1,10,message)
    return  {"Stress_ENDPOINT": "Cpus"}




@app.get("/browser_stress/",summary="Stress CPU", description="Stress cpu. Parameters are cpu for number of cpus (1-12 cpus) to be stressed and time for duration(1-100 seconds).")
def bstress(background_tasks: BackgroundTasks, cpu: Optional[int]=1, duration: Optional[int] = 10):
    if cpu<1:
        cpu=1
    if cpu>12:
        cpu=1
    if duration<1:
        duration=10
    if duration>100:
        duration=10
    background_tasks.add_task(_stress, cpu,duration)

    #print("The exit code was: %d" % list_files.returncode)
    return {"cpu": cpu, "duration": duration}


@app.post("/stress/",summary="Stress CPU", description="Stress cpu. Parameters are cpu for number of cpus (1-12 cpus) to be stressed and time for duration(1-100 seconds).")
def stress(background_tasks: BackgroundTasks, cpu: Optional[int]=1, duration: Optional[int] = 10):
    if cpu<1:
        cpu=1
    if cpu>12:
        cpu=1
    if duration<1:
        duration=10
    if duration>100:
        duration=10
 #   stress_cmd = subprocess.run(["stress-ng", "--cpu", str(cpu), "--timeout",str(time)])
    background_tasks.add_task(_stress, cpu,duration)
    #print("The exit code was: %d" % list_files.returncode)
    return {"cpu": cpu, "duration": duration}    


@app.get("/browser_stress_random/",summary="Stress CPU", description="Stress cpu. Random number of cpus will be hogged (2-8) for random time (10-30 secs).")
def stress(background_tasks: BackgroundTasks, cpu: Optional[int]=1, duration: Optional[int] = 10):
    cpu=random.randint(2,8)
    duration=random.randint(10,30)
 #   stress_cmd = subprocess.run(["stress-ng", "--cpu", str(cpu), "--timeout",str(time)])
    background_tasks.add_task(_stress, cpu,duration)
    #print("The exit code was: %d" % list_files.returncode)
    return {"cpu": cpu, "duration": duration}    

@app.post("/stress_random/",summary="Stress CPU", description="Stress cpu. Random number of cpus will be hogged (2-8) for random time (10-30 secs).")
def stress(background_tasks: BackgroundTasks, cpu: Optional[int]=1, duration: Optional[int] = 10):
    cpu=random.randint(2,8)
    duration=random.randint(10,30)
 #   stress_cmd = subprocess.run(["stress-ng", "--cpu", str(cpu), "--timeout",str(time)])
    background_tasks.add_task(_stress, cpu,duration)
    #print("The exit code was: %d" % list_files.returncode)
    return {"cpu": cpu, "duration": duration}    