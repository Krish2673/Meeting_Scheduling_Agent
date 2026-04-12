import os
from openai import OpenAI
from env.environment import MeetingEnv
from env.models import Action
from dotenv import load_dotenv
import json
import re

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

# Safe client initialization
try:
    client = OpenAI(base_url=API_BASE_URL, api_key=os.getenv("HF_TOKEN"))
except:
    client = None


def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("No valid JSON found")


def fallback_action(observation):
    if observation.conflicts:
        m1, m2 = observation.conflicts[0]
        return Action(
            action_type="reschedule",
            meeting_id=m2,
            new_start=12,
            new_end=13
        )
    return Action(action_type="noop")


def choose_action_llm(observation):
    if client is None:
        return fallback_action(observation)

    prompt = f"""
        You are an intelligent scheduling assistant.

        Meetings:
        {observation.meetings}

        Conflicts:
        {observation.conflicts}

        Return ONLY valid JSON:
        {{
        "action_type": "reschedule",
        "meeting_id": "M2",
        "new_start": 12,
        "new_end": 13
        }}
        """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a scheduling agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content
        action_dict = extract_json(content)

        return Action(**action_dict)

    except Exception as e:
        print("LLM error:", e)
        return fallback_action(observation)


def run_task(task_type):
    try:
        env = MeetingEnv()
        obs = env.reset(task_type=task_type)

        initial_conflicts = len(obs.conflicts)

        total_reward = 0

        while True:
            try:
                action = choose_action_llm(obs)
                result = env.step(action)
            except Exception as e:
                print(f"Step error ({task_type}):", e)
                break

            obs = result.observation
            total_reward += result.reward

            if result.done:
                break

        final_conflicts = len(obs.conflicts)

        score = 1 - (final_conflicts / max(1, initial_conflicts))
        return round(score, 2)

    except Exception as e:
        print(f"Task {task_type} failed:", e)
        return 0.0


def main():
    try:
        print("\nFinal Results:")
        for task in ["easy", "medium", "hard"]:
            score = run_task(task)
            print(f"{task} score: {score:.2f}")
    except Exception as e:
        print("Fatal error:", e)


if __name__ == "__main__":
    main()