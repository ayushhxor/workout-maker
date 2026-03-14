"""
Random Workout Generator - Backend API
A Flask-based REST API that generates random workout plans.
Demonstrates core Python concepts: random module, dictionaries,
list comprehensions, functions, and control flow.
"""

import random
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────────────────────────
# Exercise Database — organized by muscle group
# Each exercise has: name, equipment, sets, reps, rest (seconds)
# ──────────────────────────────────────────────────────────────

EXERCISES = {
    "Chest": [
        {"name": "Barbell Bench Press", "equipment": "Barbell", "sets": 4, "reps": "8-10", "rest": 90},
        {"name": "Incline Dumbbell Press", "equipment": "Dumbbells", "sets": 3, "reps": "10-12", "rest": 75},
        {"name": "Cable Flyes", "equipment": "Cable Machine", "sets": 3, "reps": "12-15", "rest": 60},
        {"name": "Push-Ups", "equipment": "Bodyweight", "sets": 3, "reps": "15-20", "rest": 45},
        {"name": "Dumbbell Pullover", "equipment": "Dumbbell", "sets": 3, "reps": "10-12", "rest": 60},
        {"name": "Chest Dips", "equipment": "Dip Station", "sets": 3, "reps": "10-15", "rest": 75},
        {"name": "Pec Deck Machine", "equipment": "Machine", "sets": 3, "reps": "12-15", "rest": 60},
    ],
    "Back": [
        {"name": "Deadlift", "equipment": "Barbell", "sets": 4, "reps": "5-8", "rest": 120},
        {"name": "Pull-Ups", "equipment": "Pull-Up Bar", "sets": 4, "reps": "8-12", "rest": 90},
        {"name": "Barbell Rows", "equipment": "Barbell", "sets": 4, "reps": "8-10", "rest": 90},
        {"name": "Lat Pulldown", "equipment": "Cable Machine", "sets": 3, "reps": "10-12", "rest": 75},
        {"name": "Seated Cable Row", "equipment": "Cable Machine", "sets": 3, "reps": "10-12", "rest": 75},
        {"name": "T-Bar Row", "equipment": "T-Bar", "sets": 3, "reps": "8-10", "rest": 90},
        {"name": "Face Pulls", "equipment": "Cable Machine", "sets": 3, "reps": "15-20", "rest": 45},
    ],
    "Legs": [
        {"name": "Barbell Squat", "equipment": "Barbell", "sets": 4, "reps": "6-8", "rest": 120},
        {"name": "Romanian Deadlift", "equipment": "Barbell", "sets": 4, "reps": "8-10", "rest": 90},
        {"name": "Leg Press", "equipment": "Machine", "sets": 4, "reps": "10-12", "rest": 90},
        {"name": "Walking Lunges", "equipment": "Dumbbells", "sets": 3, "reps": "12 each", "rest": 75},
        {"name": "Leg Curl", "equipment": "Machine", "sets": 3, "reps": "10-12", "rest": 60},
        {"name": "Leg Extension", "equipment": "Machine", "sets": 3, "reps": "12-15", "rest": 60},
        {"name": "Calf Raises", "equipment": "Smith Machine", "sets": 4, "reps": "15-20", "rest": 45},
        {"name": "Bulgarian Split Squat", "equipment": "Dumbbells", "sets": 3, "reps": "10 each", "rest": 75},
    ],
    "Shoulders": [
        {"name": "Overhead Press", "equipment": "Barbell", "sets": 4, "reps": "6-8", "rest": 90},
        {"name": "Lateral Raises", "equipment": "Dumbbells", "sets": 4, "reps": "12-15", "rest": 45},
        {"name": "Front Raises", "equipment": "Dumbbells", "sets": 3, "reps": "12-15", "rest": 45},
        {"name": "Reverse Flyes", "equipment": "Dumbbells", "sets": 3, "reps": "12-15", "rest": 45},
        {"name": "Arnold Press", "equipment": "Dumbbells", "sets": 3, "reps": "10-12", "rest": 75},
        {"name": "Upright Rows", "equipment": "Barbell", "sets": 3, "reps": "10-12", "rest": 60},
    ],
    "Arms": [
        {"name": "Barbell Curl", "equipment": "Barbell", "sets": 3, "reps": "10-12", "rest": 60},
        {"name": "Tricep Dips", "equipment": "Dip Station", "sets": 3, "reps": "10-15", "rest": 75},
        {"name": "Hammer Curls", "equipment": "Dumbbells", "sets": 3, "reps": "10-12", "rest": 60},
        {"name": "Skull Crushers", "equipment": "EZ Bar", "sets": 3, "reps": "10-12", "rest": 60},
        {"name": "Cable Curls", "equipment": "Cable Machine", "sets": 3, "reps": "12-15", "rest": 45},
        {"name": "Tricep Pushdown", "equipment": "Cable Machine", "sets": 3, "reps": "12-15", "rest": 45},
        {"name": "Concentration Curls", "equipment": "Dumbbell", "sets": 3, "reps": "10-12", "rest": 45},
        {"name": "Overhead Tricep Extension", "equipment": "Dumbbell", "sets": 3, "reps": "10-12", "rest": 60},
    ],
    "Core": [
        {"name": "Plank", "equipment": "Bodyweight", "sets": 3, "reps": "45-60 sec", "rest": 30},
        {"name": "Hanging Leg Raises", "equipment": "Pull-Up Bar", "sets": 3, "reps": "12-15", "rest": 45},
        {"name": "Cable Woodchoppers", "equipment": "Cable Machine", "sets": 3, "reps": "12 each", "rest": 45},
        {"name": "Ab Wheel Rollout", "equipment": "Ab Wheel", "sets": 3, "reps": "10-12", "rest": 60},
        {"name": "Russian Twists", "equipment": "Bodyweight", "sets": 3, "reps": "20 total", "rest": 30},
        {"name": "Bicycle Crunches", "equipment": "Bodyweight", "sets": 3, "reps": "20 total", "rest": 30},
        {"name": "Dead Bug", "equipment": "Bodyweight", "sets": 3, "reps": "10 each", "rest": 30},
    ],
    "Full Body": [
        {"name": "Burpees", "equipment": "Bodyweight", "sets": 3, "reps": "10-15", "rest": 60},
        {"name": "Thrusters", "equipment": "Barbell", "sets": 4, "reps": "8-10", "rest": 90},
        {"name": "Kettlebell Swings", "equipment": "Kettlebell", "sets": 4, "reps": "15-20", "rest": 60},
        {"name": "Clean and Press", "equipment": "Barbell", "sets": 4, "reps": "6-8", "rest": 120},
        {"name": "Man Makers", "equipment": "Dumbbells", "sets": 3, "reps": "8-10", "rest": 90},
        {"name": "Mountain Climbers", "equipment": "Bodyweight", "sets": 3, "reps": "30 sec", "rest": 30},
        {"name": "Box Jumps", "equipment": "Plyo Box", "sets": 3, "reps": "10-12", "rest": 60},
    ],
}

# Difficulty multipliers affect volume (number of exercises)
DIFFICULTY_CONFIG = {
    "Beginner": {"exercise_count": 3, "set_modifier": -1, "label": "🟢 Beginner"},
    "Intermediate": {"exercise_count": 5, "set_modifier": 0, "label": "🟡 Intermediate"},
    "Advanced": {"exercise_count": 7, "set_modifier": 1, "label": "🔴 Advanced"},
}

# Warm-up suggestions by muscle group
WARMUPS = {
    "Chest": ["Arm circles", "Band pull-aparts", "Light push-ups"],
    "Back": ["Cat-cow stretch", "Band pull-aparts", "Light lat pulldown"],
    "Legs": ["Bodyweight squats", "Leg swings", "Hip circles"],
    "Shoulders": ["Arm circles", "Band dislocations", "Light lateral raises"],
    "Arms": ["Wrist circles", "Light curls", "Tricep stretches"],
    "Core": ["Cat-cow stretch", "Dead bugs", "Glute bridges"],
    "Full Body": ["Jumping jacks", "Arm circles", "Bodyweight squats"],
}

# Motivational quotes to include in the workout
QUOTES = [
    "The only bad workout is the one that didn't happen. 💪",
    "Push yourself, because no one else is going to do it for you. 🔥",
    "Your body can stand almost anything. It's your mind you have to convince. 🧠",
    "The pain you feel today will be the strength you feel tomorrow. ⚡",
    "Don't wish for it. Work for it. 🏋️",
    "Sweat is just fat crying. 😤",
    "Be stronger than your excuses. 💯",
    "The hard days are what make you stronger. 🦾",
    "Success starts with self-discipline. 🎯",
    "Train insane or remain the same. 🏆",
]


# Available duration presets (in minutes)
# "any" means no time constraint
DURATION_OPTIONS = [
    {"value": "any",  "label": "⏳ No Limit",  "minutes": None},
    {"value": "15",   "label": "⚡ 15 min",    "minutes": 15},
    {"value": "30",   "label": "🕐 30 min",    "minutes": 30},
    {"value": "45",   "label": "🕑 45 min",    "minutes": 45},
    {"value": "60",   "label": "🕒 60 min",    "minutes": 60},
    {"value": "90",   "label": "🕓 90 min",    "minutes": 90},
]


def calculate_exercise_duration(exercise):
    """
    Calculate the duration of a single exercise in seconds.
    Formula: (sets * ~45 seconds per set) + (sets * rest between sets)
    """
    return (exercise["sets"] * 45) + (exercise["sets"] * exercise["rest"])


def calculate_estimated_duration(exercises):
    """
    Calculate the estimated workout duration in minutes.
    Uses: sum(), list comprehension, dictionary access.
    """
    total_seconds = sum(
        calculate_exercise_duration(ex)
        for ex in exercises
    )
    return round(total_seconds / 60)


def adjust_sets(exercise, modifier):
    """
    Adjust the number of sets based on difficulty.
    Returns a new dictionary (doesn't mutate the original).
    Uses: dictionary unpacking, max() function.
    """
    return {**exercise, "sets": max(1, exercise["sets"] + modifier)}


def generate_workout(muscle_group="Full Body", difficulty="Intermediate", max_duration=None):
    """
    Generate a random workout plan.
    
    Core Python concepts demonstrated:
    - random.sample() for selecting exercises without repetition
    - Dictionary operations for organizing data
    - List comprehensions for transforming data
    - String formatting for output
    - Conditional logic for difficulty scaling
    - Function composition
    - Greedy algorithm for time-constrained selection

    Parameters:
      muscle_group (str): Target muscle group
      difficulty   (str): Beginner / Intermediate / Advanced
      max_duration (int | None): Maximum workout time in minutes.
                                 When None, the normal count-based logic is used.
    """
    # Validate inputs with fallback defaults
    if muscle_group not in EXERCISES:
        muscle_group = "Full Body"
    if difficulty not in DIFFICULTY_CONFIG:
        difficulty = "Intermediate"

    config = DIFFICULTY_CONFIG[difficulty]
    available_exercises = EXERCISES[muscle_group]

    if max_duration is not None:
        # ── Time-constrained mode ──────────────────────────
        # Shuffle to randomize, then greedily pick exercises
        # that fit within the remaining time budget.
        # Warm-up & cool-down overhead: ~12 min
        overhead_minutes = 12
        budget_seconds = max(0, (max_duration - overhead_minutes)) * 60

        candidates = [
            adjust_sets(ex, config["set_modifier"])
            for ex in available_exercises
        ]
        random.shuffle(candidates)

        adjusted_exercises = []
        used_seconds = 0
        for ex in candidates:
            ex_time = calculate_exercise_duration(ex)
            if used_seconds + ex_time <= budget_seconds:
                adjusted_exercises.append(ex)
                used_seconds += ex_time

        # Guarantee at least 1 exercise even for very short durations
        if not adjusted_exercises and candidates:
            adjusted_exercises.append(candidates[0])
    else:
        # ── Normal count-based mode ────────────────────────
        count = min(config["exercise_count"], len(available_exercises))
        selected = random.sample(available_exercises, count)
        adjusted_exercises = [
            adjust_sets(ex, config["set_modifier"]) for ex in selected
        ]

    # Shuffle the order for variety
    random.shuffle(adjusted_exercises)

    # Calculate estimated duration
    duration = calculate_estimated_duration(adjusted_exercises)

    # Pick a random warm-up routine
    warmup = WARMUPS.get(muscle_group, WARMUPS["Full Body"])

    # Pick a random motivational quote
    quote = random.choice(QUOTES)

    # Build the workout response
    workout = {
        "muscle_group": muscle_group,
        "difficulty": config["label"],
        "exercise_count": len(adjusted_exercises),
        "estimated_duration": f"{duration} minutes",
        "max_duration": f"{max_duration} minutes" if max_duration else None,
        "warmup": warmup,
        "exercises": [
            {
                "order": i + 1,
                "name": ex["name"],
                "equipment": ex["equipment"],
                "sets": ex["sets"],
                "reps": ex["reps"],
                "rest": f"{ex['rest']} sec",
            }
            for i, ex in enumerate(adjusted_exercises)
        ],
        "cooldown": [
            "Static stretching — 5 minutes",
            "Deep breathing — 2 minutes",
            "Foam rolling (optional) — 5 minutes",
        ],
        "quote": quote,
    }

    return workout


# ──────────────────────────────────────────────────────────────
# Flask API Routes
# ──────────────────────────────────────────────────────────────

@app.route("/api/workout", methods=["GET"])
def get_workout():
    """
    Generate a random workout.
    Query Parameters:
        - muscle_group (str): Target muscle group
        - difficulty (str): Beginner, Intermediate, or Advanced
        - max_duration (str): Maximum workout time in minutes, or 'any'
    """
    muscle_group = request.args.get("muscle_group", "Full Body")
    difficulty = request.args.get("difficulty", "Intermediate")
    max_duration_raw = request.args.get("max_duration", "any")

    # Parse max_duration — 'any' or missing means no time constraint
    max_duration = None
    if max_duration_raw and max_duration_raw != "any":
        try:
            max_duration = int(max_duration_raw)
        except ValueError:
            pass

    workout = generate_workout(muscle_group, difficulty, max_duration)
    return jsonify(workout)


@app.route("/api/muscle-groups", methods=["GET"])
def get_muscle_groups():
    """Return all available muscle groups with exercise counts."""
    groups = [
        {
            "name": group,
            "exercise_count": len(exercises),
            "icon": {
                "Chest": "🏋️",
                "Back": "🔙",
                "Legs": "🦵",
                "Shoulders": "💪",
                "Arms": "💪",
                "Core": "🎯",
                "Full Body": "🔥",
            }.get(group, "💪"),
        }
        for group, exercises in EXERCISES.items()
    ]
    return jsonify(groups)


@app.route("/api/difficulties", methods=["GET"])
def get_difficulties():
    """Return all available difficulty levels."""
    difficulties = [
        {"name": key, "label": val["label"], "exercise_count": val["exercise_count"]}
        for key, val in DIFFICULTY_CONFIG.items()
    ]
    return jsonify(difficulties)


@app.route("/api/durations", methods=["GET"])
def get_durations():
    """Return all available duration presets."""
    return jsonify(DURATION_OPTIONS)


@app.route("/", methods=["GET"])
def index():
    """API health check / info endpoint."""
    return jsonify({
        "app": "Random Workout Generator API",
        "version": "1.1.0",
        "endpoints": [
            "GET /api/workout?muscle_group=...&difficulty=...&max_duration=...",
            "GET /api/muscle-groups",
            "GET /api/difficulties",
            "GET /api/durations",
        ],
    })


if __name__ == "__main__":
    print("\n🏋️  Random Workout Generator API")
    print("   Running on http://127.0.0.1:5000")
    print("   Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)
