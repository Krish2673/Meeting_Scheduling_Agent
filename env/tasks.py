from .models import Meeting

def get_easy_task():
    return [
        Meeting(id="M1", start=10, end=11, priority="high", deadline=12),
        Meeting(id="M2", start=10, end=11, priority="low", deadline=13),
    ]


def get_medium_task():
    return [
        Meeting(id="M1", start=9, end=10, priority="high", deadline=11),
        Meeting(id="M2", start=9, end=11, priority="medium", deadline=11),
        Meeting(id="M3", start=10, end=11, priority="low", deadline=12),
        Meeting(id="M4", start=10, end=12, priority="medium", deadline=12),
        Meeting(id="M5", start=11, end=12, priority="low", deadline=13),
    ]


def get_hard_task():
    return [
        # Conflict cluster 1 (slightly relaxed)
        Meeting(id="M1", start=9, end=10, priority="high", deadline=11),
        Meeting(id="M2", start=9, end=11, priority="high", deadline=13),

        # Conflict cluster 2 (manageable overlap)
        Meeting(id="M3", start=10, end=11, priority="medium", deadline=13),
        Meeting(id="M4", start=10, end=12, priority="low", deadline=13),

        # Mild pressure but solvable
        Meeting(id="M5", start=11, end=12, priority="medium", deadline=13),

        # Optional low-priority (can be dropped safely)
        Meeting(id="M6", start=11, end=13, priority="low", deadline=14),
    ]