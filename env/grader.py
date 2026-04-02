from .environment import MeetingEnv
from .models import Action

def compute_score(initial_conflicts: int, final_conflicts: int) -> float:
    if initial_conflicts == 0:
        return 1.0

    score = 1 - (final_conflicts / initial_conflicts)

    # clamp between 0 and 1
    return max(0.0, min(1.0, score))



def run_task(env: MeetingEnv, task_type: str, actions: list):
    obs = env.reset(task_type=task_type)
    initial_conflicts = len(obs.conflicts)

    done = False

    for action in actions:
        result = env.step(action)
        if result.done:
            break

    final_conflicts = len(env.find_conflicts())

    score = compute_score(initial_conflicts, final_conflicts)

    return score

env = MeetingEnv()

actions = [
    Action(action_type="reschedule", meeting_id="M2", new_start=12, new_end=13)
]

score = run_task(env, "easy", actions)
print("\n",score)