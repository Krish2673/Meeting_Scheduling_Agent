import os
from openai import OpenAI
from env.environment import MeetingEnv
from env.models import Action
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")

# client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def choose_action(observation):
    """
    Simple rule-based fallback (for stability)
    """
    if observation.conflicts:
        m1, m2 = observation.conflicts[0]

        # always reschedule second meeting
        return Action(
            action_type="reschedule",
            meeting_id=m2,
            new_start=12,
            new_end=13
        )

    return Action(action_type="noop")


def run_task(task_type):
    env = MeetingEnv()
    obs = env.reset(task_type=task_type)

    total_reward = 0

    while True:
        action = choose_action(obs)

        result = env.step(action)
        obs = result.observation

        total_reward += result.reward

        if result.done:
            break

    final_conflicts = len(obs.conflicts)
    initial_conflicts = len(env.reset(task_type=task_type).conflicts)

    score = 1 - (final_conflicts / max(1, initial_conflicts))

    return score


def main():
    for task in ["easy", "medium", "hard"]:
        score = run_task(task)
        print(f"{task} score: {score:.2f}")


if __name__ == "__main__":
    main()