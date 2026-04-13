#  Meeting Scheduling Agent Environment (OpenEnv)

A real-world environment for training and evaluating AI agents on **calendar scheduling under constraints**.

This environment simulates a common human task: resolving meeting conflicts while balancing **priorities, deadlines, and limited time slots**.

---
## Motivation

Modern AI assistants are expected to handle productivity tasks like:

- Managing calendars  
- Resolving scheduling conflicts  
- Prioritizing important meetings  
- Respecting deadlines and constraints  

However, most benchmarks do not capture this **multi-objective decision-making**.

This environment fills that gap by providing a **deterministic, reproducible evaluation setting** for agentic AI systems.

---

## Environment Overview

The agent interacts with the environment using standard OpenEnv APIs:

- `reset()` → initializes the task  
- `step(action)` → applies an action  
- `state()` → returns current state  

---

## Observation Space

Each observation contains:

```json
{
  "meetings": [
    {
      "id": "M1",
      "start": 10,
      "end": 11,
      "priority": "high",
      "deadline": 12
    }
  ],
  "conflicts": [["M1", "M2"]],
  "remaining_steps": 5
}
```

## Fields

- **meetings** → current schedule  
- **conflicts** → overlapping meetings  
- **remaining_steps** → steps left in episode  

---

## Action Space

The agent can take the following actions:

```json
{
  "action_type": "reschedule | drop | noop",
  "meeting_id": "M2",
  "new_start": 12,
  "new_end": 13
}
```

### Actions

- **reschedule** → move meeting  
- **drop** → remove meeting  
- **noop** → do nothing  

---

## Reward Function

The reward function provides dense, meaningful feedback:

### ➕ Positive Signals

- Resolving conflicts → **+0.5**  
- Keeping high-priority meetings → **+0.2**  
- Valid scheduling within deadline  **+0.1**  
- Fully conflict-free schedule → **+1.0**  

### ➖ Penalties

- Creating conflicts → **-0.3**  
- Dropping high-priority meetings → **-0.6**  
- Deadline violations → **up to -0.8**  
- Empty schedule → **-1.0**  
- Useless actions → **-0.1**  

#### This encourages intelligent trade-offs, not greedy behavior.

## Tasks

The environment includes 3 deterministic tasks:

### 🟢 Easy

- Single conflict  
- Easily solvable  
- Expected score: **~1.0**

### 🟡 Medium

- Multiple overlaps  
- Requires reasoning  
- Expected score: **~0.9–1.0**

### 🔴 Hard

- Multiple conflict clusters  
- Priority trade-offs  
- Deadline constraints  
- Not fully solvable  

Expected score: **~0.6-0.85**

---

## Baseline Agent

A hybrid agent is provided:

- LLM-based reasoning   
- Fallback rule-based logic 

### The agent:

- resolves conflicts  
- preserves high-priority meetings  
- respects deadlines  

---

## Baseline Results

- **easy** → 1.00  
- **medium** → 1.00  
- **hard** → 0.86  

## Setup & Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set environment variables

```bash
API_BASE_URL=https://openrouter.ai/api/v1
OPENAI_API_KEY=your_api_key
MODEL_NAME=openai/gpt-4o-mini
```

### 3. Run inference

```bash
python inference.py
```

### Docker

Build and run:

```bash
docker build -t meeting-env .
docker run meeting-env
```

## API Endpoints (HF Space)

- `/reset` → initialize environment  
- `/step` → apply action  
- `/state` → get current state  
- `/run_inference` → run baseline evaluation  

---

## Key Features

-  Real-world task simulation  
-  Multi-objective optimization  
-  Deterministic evaluation  
-  Meaningful reward shaping  
-  LLM + rule-based hybrid agent  
-  Fully deployable (Docker + HF Spaces)  

## Why this matters

This environment enables evaluation of agents on:

- Planning under constraints  
- Trade-off reasoning  
- Decision-making with incomplete satisfaction  

---

## Future Improvements

- Dynamic task generation  
- Time-slot constraints (working hours)  
- Multi-agent scheduling  
- Real calendar dataset integration  

## Conclusion

This project demonstrates a realistic, scalable benchmark for agentic AI systems performing scheduling tasks.

It bridges the gap between:

- simple RL environments 
- real-world decision-making systems
