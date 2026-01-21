def decide_policy(mastery):
    if mastery < 0.3:
        return "beginner", 5
    elif mastery < 0.7:
        return "intermediate", 4
    return "advanced", 3