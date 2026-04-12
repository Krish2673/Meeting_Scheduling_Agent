from fastapi import FastAPI
from env.environment import MeetingEnv
from env.models import Action
from inference import run_task
import uvicorn

app = FastAPI()

env = MeetingEnv()

@app.get("/")
def root():
    return {"Message" : "Meeting Scheduling Environment is running"}

@app.get("/reset")
@app.post("/reset")
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

@app.get("/run_inference")
def run():
    try:
        easy_score = run_task("easy")
        medium_score = run_task("medium")
        hard_score = run_task("hard")

        return {
            "status": "success",
            "scores": {
                "easy": easy_score,
                "medium": medium_score,
                "hard": hard_score
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/state")
def state():
    obs = env.state()
    return obs.model_dump()

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()