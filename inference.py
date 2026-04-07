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

client = OpenAI(base_url=API_BASE_URL, api_key=os.getenv("OPENAI_API_KEY"))

def extract_json(text):
            try:
                return json.loads(text)
            except:
                match = re.search(r"\{.*\}", text, re.DOTALL)       # Extract JSON block
                if match:
                    return json.loads(match.group())
                raise ValueError("No valid JSON found")

def choose_action_llm(observation):
    prompt = f"""
        You are an intelligent scheduling assistant.

        Your goal:
        - Resolve meeting conflicts
        - Preserve high-priority meetings
        - Respect deadlines

        Meetings:
        {observation.meetings}

        Conflicts:
        {observation.conflicts}

        IMPORTANT:
        - Return ONLY valid JSON
        - Do NOT include any explanation or text
        - Output must be strictly in this format:

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
                {"role": "system", "content": "You are a smart scheduling agent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content

        action_dict = extract_json(content)

        return Action(**action_dict)

    except Exception as e:
        print("LLM error:", e)

        return Action(action_type="noop")


def run_task(task_type):
    env = MeetingEnv()
    obs = env.reset(task_type=task_type)

    total_reward = 0

    while True:
        action = choose_action_llm(obs)

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
    print("\nFinal Results:")
    for task in ["easy", "medium", "hard"]:
        score = run_task(task)
        print(f"{task} score: {score:.2f}")


if __name__ == "__main__":
    main()