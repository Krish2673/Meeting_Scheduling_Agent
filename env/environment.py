from typing import List
from copy import deepcopy
from .models import Meeting, Observation, Action, StepResult
from .tasks import get_easy_task, get_medium_task, get_hard_task

class MeetingEnv:
    def __init__(self, max_steps: int = 5):
        self.max_steps = max_steps
        self.current_step = 0
        self.meetings: List[Meeting] = []

    def find_conflicts(self) -> List[List[str]]:
        conflicts = []

        for i in range(len(self.meetings)):
            for j in range(i + 1, len(self.meetings)):
                m1 = self.meetings[i]
                m2 = self.meetings[j]

                # overlap condition
                if not (m1.end <= m2.start or m2.end <= m1.start):
                    conflicts.append([m1.id, m2.id])

        return conflicts
    
    def reset(self, task_type="easy") -> Observation:
        self.current_step = 0

        if task_type == "easy":
            self.meetings = get_easy_task()
        elif task_type == "medium":
            self.meetings = get_medium_task()
        else:
            self.meetings = get_hard_task()

        conflicts = self.find_conflicts()

        return Observation(
            meetings=self.meetings,
            conflicts=conflicts,
            remaining_steps=self.max_steps
        )
    
    def apply_action(self, action: Action):
        if action.action_type == "reschedule":
            for m in self.meetings:
                if m.id == action.meeting_id:
                    if action.new_start is not None and action.new_end is not None:
                        m.start = action.new_start
                        m.end = action.new_end

        elif action.action_type == "drop":
            self.meetings = [m for m in self.meetings if m.id != action.meeting_id]

        elif action.action_type == "noop":
            pass

    def step(self, action: Action) -> StepResult:
        self.current_step += 1

        # Store previous state (IMPORTANT)
        prev_meetings = deepcopy(self.meetings)
        prev_conflicts = self.find_conflicts()
        prev_conflict_count = len(prev_conflicts)

        # Apply action
        self.apply_action(action)

        # New state
        new_conflicts = self.find_conflicts()
        new_conflict_count = len(new_conflicts)

        # ---------------- REWARD LOGIC ----------------
        reward = 0.0

        # 1. Conflict-based reward
        if new_conflict_count < prev_conflict_count:
            reward += 0.5  # resolved conflict
        elif new_conflict_count > prev_conflict_count:
            reward -= 0.3  # created conflict

        # 2. Priority-aware penalty for dropping meetings
        prev_ids = {m.id for m in prev_meetings}
        current_ids = {m.id for m in self.meetings}

        dropped_ids = prev_ids - current_ids

        for m in prev_meetings:
            if m.id in dropped_ids:
                if m.priority == "high":
                    reward -= 0.6
                elif m.priority == "medium":
                    reward -= 0.3
                else:
                    reward -= 0.1

        # 3. Reward preserving important meetings
        if new_conflict_count < prev_conflict_count:
            for m in self.meetings:
                if m.priority == "high":
                    reward += 0.2
                elif m.priority == "medium":
                    reward += 0.1

        # 4. Penalty for useless action
        if action.action_type == "noop" and prev_conflict_count > 0:
            reward -= 0.1

        # 5. Strong penalty if all meetings are removed
        if len(self.meetings) == 0:
            reward -= 1.0

        # 6. Deadline violation penalty
        for m in self.meetings:
            if m.end > m.deadline:
                reward -= 0.8
            else:
                reward += 0.1  # reward valid scheduling
            if m.end > m.deadline+1:
                reward -= 1.0

        # ---------------- DONE LOGIC ----------------
        done = False

        if new_conflict_count == 0 and len(self.meetings) > 0:
            reward += 1.0
            done = True

        if len(self.meetings) == 0:
            done = True

        if self.current_step >= self.max_steps:
            done = True

        # ---------------- OBSERVATION ----------------
        observation = Observation(
            meetings=deepcopy(self.meetings),
            conflicts=new_conflicts,
            remaining_steps=self.max_steps - self.current_step
        )

        return StepResult(
            observation=observation,
            reward=reward,
            done=done,
            info={}
        )

    def state(self) -> Observation:
        return Observation(
            meetings=self.meetings,
            conflicts=self.find_conflicts(),
            remaining_steps=self.max_steps - self.current_step
        )


env = MeetingEnv()
obs = env.reset()

action = Action(action_type="reschedule", meeting_id="M2", new_start=12, new_end=13)

result = env.step(action)