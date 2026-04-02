from .models import Meeting

def get_easy_task():
    return [
        Meeting(id="M1", start=10, end=11, priority="high"),
        Meeting(id="M2", start=10, end=11, priority="low"),
    ]


def get_medium_task():
    return [
        Meeting(id="M1", start=9, end=10, priority="high"),
        Meeting(id="M2", start=9, end=11, priority="medium"),
        Meeting(id="M3", start=10, end=11, priority="low"),
        Meeting(id="M4", start=11, end=12, priority="medium"),
    ]


def get_hard_task():
    return [
        Meeting(id="M1", start=9, end=10, priority="high"),
        Meeting(id="M2", start=9, end=11, priority="high"),
        Meeting(id="M3", start=10, end=11, priority="medium"),
        Meeting(id="M4", start=10, end=12, priority="low"),
        Meeting(id="M5", start=11, end=12, priority="medium"),
        Meeting(id="M6", start=11, end=13, priority="low"),
    ]