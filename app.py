from fastapi import FastAPI
from env.environment import MeetingEnv
from env.models import Action

app = FastAPI()

env = MeetingEnv()

@app.get("/")
def root():
    return {"Message" : "Meeting Scheduling Environment is running"}

@app.get("/reset")
def reset(task: str = "easy"):
    obs = env.reset(task_type=task)
    return obs.model_dump()


@app.post("/step")
def step(action: dict):
    action_obj = Action(**action)
    result = env.step(action_obj)

    return {
        "observation": result.observation.model_dump(),
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }


@app.get("/state")
def state():
    obs = env.state()
    return obs.model_dump()