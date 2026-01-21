from memory.memory_manager import update_memory

def simulate(student_id):
    mastery, stability = update_memory(
        student_id=student_id,
        concept="Newton First Law",
        correct=False,
        days_passed=3
    )

    print("Updated mastery:", mastery)
    print("Updated stability:", stability)