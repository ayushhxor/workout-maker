"""
Random Workout Generator - Backend API
A Flask-based REST API that generates random workout plans.
Demonstrates core Python concepts: random module, dictionaries,
list comprehensions, functions, and control flow.
"""

import random
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────────────────────────
# Exercise Image CDN
# Images sourced from yuhonas/free-exercise-db (public domain)
# Each exercise folder contains 0.jpg (start) and 1.jpg (end)
# ──────────────────────────────────────────────────────────────

IMAGE_BASE_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises"

# ──────────────────────────────────────────────────────────────
# Exercise Database — organized by muscle group
# Each exercise has: name, equipment, sets, reps, rest, image_id
# image_id maps to the free-exercise-db folder name
# ──────────────────────────────────────────────────────────────

EXERCISES = {
    "Chest": [
        {"name": "Barbell Bench Press", "equipment": "Barbell", "sets": 4, "reps": "8-10", "rest": 90, "image_id": "Barbell_Bench_Press_-_Medium_Grip"},
        {"name": "Incline Dumbbell Press", "equipment": "Dumbbells", "sets": 3, "reps": "10-12", "rest": 75, "image_id": "Incline_Dumbbell_Press"},
        {"name": "Cable Flyes", "equipment": "Cable Machine", "sets": 3, "reps": "12-15", "rest": 60, "image_id": "Flat_Bench_Cable_Flyes"},
        {"name": "Push-Ups", "equipment": "Bodyweight", "sets": 3, "reps": "15-20", "rest": 45, "image_id": "Push-Ups"},
        {"name": "Dumbbell Pullover", "equipment": "Dumbbell", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "Bent-Arm_Dumbbell_Pullover"},
        {"name": "Chest Dips", "equipment": "Dip Station", "sets": 3, "reps": "10-15", "rest": 75, "image_id": "Dips_-_Chest_Version"},
        {"name": "Pec Deck Machine", "equipment": "Machine", "sets": 3, "reps": "12-15", "rest": 60, "image_id": "Butterfly"},
    ],
    "Back": [
        {"name": "Deadlift", "equipment": "Barbell", "sets": 4, "reps": "5-8", "rest": 120, "image_id": "Barbell_Deadlift"},
        {"name": "Pull-Ups", "equipment": "Pull-Up Bar", "sets": 4, "reps": "8-12", "rest": 90, "image_id": "Pullups"},
        {"name": "Barbell Rows", "equipment": "Barbell", "sets": 4, "reps": "8-10", "rest": 90, "image_id": "Bent_Over_Barbell_Row"},
        {"name": "Lat Pulldown", "equipment": "Cable Machine", "sets": 3, "reps": "10-12", "rest": 75, "image_id": "Wide-Grip_Lat_Pulldown"},
        {"name": "Seated Cable Row", "equipment": "Cable Machine", "sets": 3, "reps": "10-12", "rest": 75, "image_id": "Seated_Cable_Rows"},
        {"name": "T-Bar Row", "equipment": "T-Bar", "sets": 3, "reps": "8-10", "rest": 90, "image_id": "Bent_Over_Two-Arm_Long_Bar_Row"},
        {"name": "Face Pulls", "equipment": "Cable Machine", "sets": 3, "reps": "15-20", "rest": 45, "image_id": "Face_Pull"},
    ],
    "Legs": [
        {"name": "Barbell Squat", "equipment": "Barbell", "sets": 4, "reps": "6-8", "rest": 120, "image_id": "Barbell_Squat"},
        {"name": "Romanian Deadlift", "equipment": "Barbell", "sets": 4, "reps": "8-10", "rest": 90, "image_id": "Romanian_Deadlift_With_Dumbbells"},
        {"name": "Leg Press", "equipment": "Machine", "sets": 4, "reps": "10-12", "rest": 90, "image_id": "Leg_Press"},
        {"name": "Walking Lunges", "equipment": "Dumbbells", "sets": 3, "reps": "12 each", "rest": 75, "image_id": "Barbell_Walking_Lunge"},
        {"name": "Leg Curl", "equipment": "Machine", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "Seated_Leg_Curl"},
        {"name": "Leg Extension", "equipment": "Machine", "sets": 3, "reps": "12-15", "rest": 60, "image_id": "Leg_Extensions"},
        {"name": "Calf Raises", "equipment": "Smith Machine", "sets": 4, "reps": "15-20", "rest": 45, "image_id": "Smith_Machine_Calf_Raise"},
        {"name": "Bulgarian Split Squat", "equipment": "Dumbbells", "sets": 3, "reps": "10 each", "rest": 75, "image_id": "Single_Leg_Push-Off"},
    ],
    "Shoulders": [
        {"name": "Overhead Press", "equipment": "Barbell", "sets": 4, "reps": "6-8", "rest": 90, "image_id": "Barbell_Shoulder_Press"},
        {"name": "Lateral Raises", "equipment": "Dumbbells", "sets": 4, "reps": "12-15", "rest": 45, "image_id": "Side_Lateral_Raise"},
        {"name": "Front Raises", "equipment": "Dumbbells", "sets": 3, "reps": "12-15", "rest": 45, "image_id": "Front_Dumbbell_Raise"},
        {"name": "Reverse Flyes", "equipment": "Dumbbells", "sets": 3, "reps": "12-15", "rest": 45, "image_id": "Bent_Over_Dumbbell_Rear_Delt_Raise_With_Head_On_Bench"},
        {"name": "Arnold Press", "equipment": "Dumbbells", "sets": 3, "reps": "10-12", "rest": 75, "image_id": "Arnold_Dumbbell_Press"},
        {"name": "Upright Rows", "equipment": "Barbell", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "Upright_Barbell_Row"},
    ],
    "Arms": [
        {"name": "Barbell Curl", "equipment": "Barbell", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "Barbell_Curl"},
        {"name": "Tricep Dips", "equipment": "Dip Station", "sets": 3, "reps": "10-15", "rest": 75, "image_id": "Bench_Dips"},
        {"name": "Hammer Curls", "equipment": "Dumbbells", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "Alternate_Hammer_Curl"},
        {"name": "Skull Crushers", "equipment": "EZ Bar", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "EZ-Bar_Skullcrusher"},
        {"name": "Cable Curls", "equipment": "Cable Machine", "sets": 3, "reps": "12-15", "rest": 45, "image_id": "Cable_Hammer_Curls_-_Rope_Attachment"},
        {"name": "Tricep Pushdown", "equipment": "Cable Machine", "sets": 3, "reps": "12-15", "rest": 45, "image_id": "Triceps_Pushdown"},
        {"name": "Concentration Curls", "equipment": "Dumbbell", "sets": 3, "reps": "10-12", "rest": 45, "image_id": "Concentration_Curls"},
        {"name": "Overhead Tricep Extension", "equipment": "Dumbbell", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "Standing_Dumbbell_Triceps_Extension"},
    ],
    "Core": [
        {"name": "Plank", "equipment": "Bodyweight", "sets": 3, "reps": "45-60 sec", "rest": 30, "image_id": "Plank"},
        {"name": "Hanging Leg Raises", "equipment": "Pull-Up Bar", "sets": 3, "reps": "12-15", "rest": 45, "image_id": "Hanging_Leg_Raise"},
        {"name": "Cable Woodchoppers", "equipment": "Cable Machine", "sets": 3, "reps": "12 each", "rest": 45, "image_id": "Cross-Body_Crunch"},
        {"name": "Ab Wheel Rollout", "equipment": "Ab Wheel", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "Ab_Roller"},
        {"name": "Russian Twists", "equipment": "Bodyweight", "sets": 3, "reps": "20 total", "rest": 30, "image_id": "Russian_Twist"},
        {"name": "Bicycle Crunches", "equipment": "Bodyweight", "sets": 3, "reps": "20 total", "rest": 30, "image_id": "Air_Bike"},
        {"name": "Dead Bug", "equipment": "Bodyweight", "sets": 3, "reps": "10 each", "rest": 30, "image_id": "Flat_Bench_Lying_Leg_Raise"},
    ],
    "Full Body": [
        {"name": "Burpees", "equipment": "Bodyweight", "sets": 3, "reps": "10-15", "rest": 60, "image_id": "Burpee"},
        {"name": "Thrusters", "equipment": "Barbell", "sets": 4, "reps": "8-10", "rest": 90, "image_id": "Barbell_Squat"},
        {"name": "Kettlebell Swings", "equipment": "Kettlebell", "sets": 4, "reps": "15-20", "rest": 60, "image_id": "One-Arm_Kettlebell_Swings"},
        {"name": "Clean and Press", "equipment": "Barbell", "sets": 4, "reps": "6-8", "rest": 120, "image_id": "Clean_and_Press"},
        {"name": "Man Makers", "equipment": "Dumbbells", "sets": 3, "reps": "8-10", "rest": 90, "image_id": "Alternating_Renegade_Row"},
        {"name": "Mountain Climbers", "equipment": "Bodyweight", "sets": 3, "reps": "30 sec", "rest": 30, "image_id": "Mountain_Climbers"},
        {"name": "Box Jumps", "equipment": "Plyo Box", "sets": 3, "reps": "10-12", "rest": 60, "image_id": "Bench_Jump"},
    ],
}

# Difficulty multipliers affect volume (number of exercises)
DIFFICULTY_CONFIG = {
    "Beginner": {"exercise_count": 3, "set_modifier": -1, "label": "Beginner"},
    "Intermediate": {"exercise_count": 5, "set_modifier": 0, "label": "Intermediate"},
    "Advanced": {"exercise_count": 7, "set_modifier": 1, "label": "Advanced"},
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
    "The only bad workout is the one that didn't happen.",
    "Push yourself, because no one else is going to do it for you.",
    "Your body can stand almost anything. It's your mind you have to convince.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "Don't wish for it. Work for it.",
    "Sweat is just fat crying.",
    "Be stronger than your excuses.",
    "The hard days are what make you stronger.",
    "Success starts with self-discipline.",
    "Train insane or remain the same.",
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
                "images": [
                    f"{IMAGE_BASE_URL}/{ex['image_id']}/0.jpg",
                    f"{IMAGE_BASE_URL}/{ex['image_id']}/1.jpg",
                ],
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
            "icon": "",
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
    print("   Press Ctrl+C to stop\n")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)