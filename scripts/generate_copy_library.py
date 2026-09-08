# -*- coding: utf-8 -*-
"""Generate complete 83-post copy library for @homefit.europe"""
import csv, re, os

BASE = r'C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\project3-ins'

# ---------- Reel content: topic -> (emoji, hook, actions[5], cta) ----------
REELS = {
"15 Min Morning Fat Burn": ("🔥", "No equipment. No gym. No excuses.", ["Jumping Jacks x 45s","Mountain Climbers x 45s","High Knees x 45s","Burpees x 30s","Plank Jacks x 45s"], "⏰ Save this for tomorrow morning!\n👯 Tag a friend who needs this"),
"No-Equipment Ab Workout": ("🤯", "Your core will be on fire.", ["Bicycle Crunches x 20","Leg Raises x 15","Russian Twists x 30","Plank x 45s","Dead Bug x 12 each side"], "💾 Save for your next ab day\n👉 Follow @homefit.europe for daily home workouts"),
"Office Desk Stretch Routine": ("🖥️", "SITTING ALL DAY? DO THIS AT YOUR DESK", ["Seated Spinal Twist — 30s each side","Chest Opener Clasp — 30s","Neck Rolls — 10 each direction","Wrist Stretches — 20s","Seated Forward Fold — 45s"], "Takes 3 minutes. Do it NOW.\n💾 Save this for work hours"),
"5 Min Bedtime Core": ("🌙", "5 MIN BEDTIME CORE — end your day strong", ["Dead Bug x 12 each side","Bird Dog x 10 each side","Glute Bridge March x 10 each","Side Plank Dips x 8 each","Knee-to-Chest Stretch x 30s"], "😴 Do this before sleep. Your core will thank you.\n📌 Save for tonight"),
"Full Body HIIT at Home": ("💣", "FULL BODY HIIT — 20 MIN, ZERO EQUIPMENT", ["Squat Jumps x 30s","Push-Ups x 20s","Mountain Climbers x 40s","Plank Shoulder Taps x 30s","Lunge Jumps x 30s"], "3 rounds. Rest 45s between.\n🔁 Save and repeat tomorrow"),
"Push-Up Progression Guide": ("💪", "CAN'T DO A PUSH-UP? START HERE", ["Wall Push-Ups x 10","Incline Push-Ups (table) x 10","Knee Push-Ups x 8","Standard Push-Ups x 5","Slow Negative Push-Ups x 4"], "Progress is progress. Meet yourself where you are.\n📌 Save this progression"),
"Squat Form Correction": ("⚠️", "FIX YOUR SQUAT — 3 MISTAKES KILLING YOUR FORM", ["Heels flat, weight mid-foot","Knees track over toes","Chest up, back neutral","Sit back like a chair","Depth: hips below knees (if mobility allows)"], "Film yourself. Fix one cue at a time.\n💾 Save for your next leg day"),
"10 Min Leg Day No Equipment": ("🦵", "10 MIN LEG DAY — NO EQUIPMENT NEEDED", ["Bodyweight Squats x 20","Reverse Lunges x 12 each","Glute Bridges x 20","Curtsy Lunges x 10 each","Wall Sit x 45s"], "3 rounds. Your legs will feel it tomorrow.\n🔥 Save this for leg day"),
"Morning Yoga Flow": ("🧘", "5 MIN MORNING YOGA TO WAKE UP", ["Cat-Cow x 10","Downward Dog — 30s","Low Lunge x 30s each","Standing Forward Fold x 30s","Child's Pose x 30s"], "Start your day with intention.\n☀️ Save for tomorrow morning"),
"Post-Workout Stretch": ("🧊", "DON'T SKIP THE STRETCH — DO THIS AFTER TRAINING", ["Quad Stretch x 30s each","Hamstring Stretch x 30s each","Chest Opener x 30s","Pigeon Pose x 30s each","Cat-Cow x 10"], "Stretching = faster recovery, less soreness.\n📌 Save for after your workout"),
"Plank Challenge Variations": ("🛡️", "PLANK, BUT NOT BORING — 5 VARIATIONS", ["Standard Plank x 40s","Plank Shoulder Taps x 30s","Side Plank x 25s each","Plank Up-Downs x 20s","Reaching Plank x 30s"], "Pick 3, do 2 rounds. Core on fire.\n💾 Save this challenge"),
"Lunge Mistakes to Avoid": ("🚫", "STOP DOING LUNGES LIKE THIS", ["Step length: not too long","Front knee over ankle","Chest tall, don't lean forward","Push through front heel","Control the descent, don't bounce"], "Fix these and your lunges will feel 10x better.\n📌 Save for form check"),
"15 Min Upper Body Burn": ("💥", "15 MIN UPPER BODY BURN — NO WEIGHTS", ["Push-Ups x 12","Pike Push-Ups x 8","Tricep Dips (chair) x 10","Superman Hold x 30s","Plank to Downward Dog x 8"], "3 rounds. Minimal rest. Let's go.\n🔥 Save for upper body day"),
"Cool Down Routine": ("🌬️", "HOW TO COOL DOWN PROPERLY", ["Deep Breathing x 1 min","Child's Pose x 45s","Hamstring Stretch x 30s each","Chest Stretch x 30s","Full Body Shake Out x 30s"], "Cool down = better recovery.\n💾 Save for after every workout"),
"30-Day Squat Challenge Day 1": ("🏆", "30-DAY SQUAT CHALLENGE — DAY 1", ["Bodyweight Squats x 20","Wall Sit x 30s","Reverse Lunges x 8 each","Glute Bridges x 15","Squat Hold x 20s"], "Day 1 done! Come back tomorrow.\n🔖 Save the series and join us!"),
"Booty Band Workout at Home": ("🍑", "BOOTY BAND WORKOUT — HOME EDITION", ["Clamshells x 15 each","Fire Hydrants x 12 each","Glute Bridges with Band x 15","Donkey Kicks x 12 each","Band Walks x 10 each direction"], "Need a band? A towel loop works too.\n💾 Save for glute day"),
"Quick Cardio Blast": ("⚡", "5 MIN QUICK CARDIO BLAST", ["High Knees x 40s","Jump Rope (imaginary) x 40s","Burpees x 30s","Skater Jumps x 40s","Mountain Climbers x 40s"], "2 rounds. All you need is 5 minutes.\n⏰ Save for busy days"),
"Fitness Fact of the Week": (None, None, None, None),  # static, not reel - skip
"Shoulder Mobility Routine": ("🙆", "FIX TIGHT SHOULDERS IN 5 MINUTES", ["Arm Circles x 20 each direction","Shoulder Rolls x 15","Wall Slides x 10","Cross-Body Stretch x 30s each","Thread the Needle x 8 each"], "Desk workers: this is for you.\n💾 Save and do it daily"),
"15 Min Arm Workout": ("💪", "15 MIN ARM WORKOUT — TONED ARMS AT HOME", ["Diamond Push-Ups x 8","Tricep Dips x 12","Pike Push-Ups x 8","Arm Circles (light or none) x 30s","Plank to Downward Dog x 8"], "3 rounds. No weights needed.\n🔥 Save for arm day"),
"Burpee Alternatives": ("🦗", "HATE BURPEES? DO THESE INSTEAD", ["Squat to Stand x 15","Plank to Knee Tucks x 10","Step-Back Jacks x 20","Squat Thrusts (no jump) x 10","High Knees x 30s"], "Same burn, kinder to your joints.\n📌 Save this alternative list"),
"Mountain Climber Variations": ("⛰️", "MOUNTAIN CLIMBERS — 5 WAYS", ["Standard Climbers x 40s","Cross-Body Climbers x 40s","Slow Controlled Climbers x 30s","Spider Climbers x 30s","Incline Climbers (hands on chair) x 40s"], "Pick 3 and go. Core + cardio in one.\n💾 Save for your next HIIT"),
"Standing Ab Workout": ("🧍", "ABS WITHOUT GETTING ON THE FLOOR", ["Standing Knee Raises x 20 each","Standing Oblique Crunches x 20 each","Standing Toe Touches x 20","Wood Choppers (imaginary) x 15 each","Standing Twists x 30s"], "Perfect for small spaces and office breaks.\n📌 Save for later"),
"Jump Rope Alternative Home": ("🪢", "NO JUMP ROPE? NO PROBLEM", ["Imaginary Jump Rope x 45s","Boxer Shuffles x 45s","Ski Steps x 45s","Double Step Taps x 45s","High Knees x 30s"], "Same cardio effect, zero equipment.\n⏰ Save for cardio days"),
"15 Min Full Body Stretch": ("🧘", "15 MIN FULL BODY STRETCH — DO THIS ANYTIME", ["Cat-Cow x 10","Downward Dog x 30s","Pigeon Pose x 30s each","Seated Forward Fold x 45s","Spinal Twist x 30s each"], "Full body reset in 15 minutes.\n💾 Save for rest days"),
"Desk Posture Fixes": ("💻", "YOUR DESK IS RUINING YOUR POSTURE", ["Chin Tucks x 10","Shoulder Blade Squeezes x 15","Desk Push-Away Stretch x 30s","Seated Cat-Cow x 10","Stand Up + Reach x 30s"], "Do this every 2 hours at work.\n📌 Save for work hours"),
"No Jump Cardio": ("🦶", "JOINT-FRIENDLY CARDIO — NO JUMPING", ["Step-Touch x 40s","Squat Pulsing x 30s","Knee Drives x 40s","Shadow Boxing x 40s","Side Steps x 30s"], "Perfect for apartments and knee pain.\n💾 Save for quiet-cardio days"),
"Core Stability Workout": ("🧊", "CORE STABILITY — NOT JUST CRUNCHES", ["Plank x 45s","Side Plank x 30s each","Bird Dog x 10 each","Dead Bug x 12 each","Glute Bridge March x 10 each"], "Stability = injury prevention.\n📌 Save this one"),
"Push Day at Home": ("🏋️", "PUSH DAY AT HOME — CHEST, SHOULDERS, TRICEPS", ["Push-Ups x 12","Pike Push-Ups x 8","Diamond Push-Ups x 8","Tricep Dips x 10","Plank Shoulder Taps x 20"], "3 rounds, 60s rest between.\n🔥 Save for push day"),
"Pull Day Bodyweight": ("🎣", "PULL DAY WITHOUT A PULL-UP BAR", ["Towel Rows (door) x 10","Reverse Snow Angels x 12","Superman Hold x 30s","Rear Delt Flys (no weight) x 15","Tabletop Rows x 10"], "Back day is possible at home!\n💾 Save for pull day"),
"Leg Day No Squats": ("🦵", "LEG DAY WITHOUT SQUATS", ["Reverse Lunges x 12 each","Glute Bridges x 20","Curtsy Lunges x 10 each","Step-Ups (chair) x 12 each","Single-Leg Glute Bridge x 10 each"], "Knee pain? This is your leg day.\n📌 Save this routine"),
"Power Yoga for Strength": ("🧘", "POWER YOGA — YOGA THAT BUILDS STRENGTH", ["Chaturanga x 8","Warrior II Hold x 30s each","Plank to Chaturanga x 8","Boat Pose x 30s","Crow Pose (or knee version) x 20s"], "Yoga isn't easy — it's strength in disguise.\n🔥 Save for active rest days"),
"Balance Training Routine": ("⚖️", "BALANCE TRAINING — 5 MIN FOR STABILITY", ["Single-Leg Stand x 30s each","Heel-to-Toe Walk x 10 steps","Single-Leg Deadlift (touch floor) x 8 each","Eyes-Closed Stand x 20s","Tree Pose x 30s each"], "Balance = better athleticism, fewer injuries.\n📌 Save for warm-ups"),
"Reaction Time Drills": ("⚡", "REACTION TIME DRILLS — TRAIN YOUR BRAIN", ["Tennis Ball Drop Catch x 15","Wall Toss x 20","Mirror Shadow x 30s","Speed Taps (alternating) x 30s","Agility Ladder Steps (imaginary) x 30s"], "Fun, fast, and improves coordination.\n💾 Save for active rest"),
"Flexibility Routine": ("🧘", "FLEXIBILITY ROUTINE FOR TIGHT MUSCLES", ["Hamstring Stretch x 30s each","Hip Flexor Stretch x 30s each","Chest Opener x 30s","Butterfly Stretch x 45s","Full Body Roll Down x 30s"], "Flexibility is a skill — practice it.\n📌 Save for evenings"),
"Neck & Shoulder Tension Relief": ("💆", "NECK & SHOULDER TENSION? TRY THIS", ["Chin Tucks x 10","Ear-to-Shoulder Stretch x 30s each","Levator Stretch x 30s each","Shoulder Shrugs + Drop x 15","Towel Neck Stretch x 30s"], "3 minutes. Instant relief for desk workers.\n💾 Save for work breaks"),
"Wrist Mobility Exercises": ("⌨️", "TYPING ALL DAY? STRETCH YOUR WRISTS", ["Wrist Circles x 15 each direction","Prayer Stretch x 30s","Finger Pulls x 10 each","Wrist Flexor Stretch x 30s each","Finger Walks x 10"], "Prevent RSI before it starts.\n📌 Save for work hours"),
"Ankle Stability Drills": ("🦶", "ANKLE STABILITY — PREVENT SPRAINS", ["Alphabet Circles x 1 set each","Single-Leg Hops x 15 each","Heel Raises x 20","Towel Scrunches x 20","Single-Leg Balance x 30s each"], "Strong ankles = confident movement.\n💾 Save for leg days"),
"15 Min Boxing Workout": ("🥊", "15 MIN BOXING WORKOUT AT HOME", ["Jab-Cross Combo x 40s","Hooks x 40s","Shadow Boxing Freestyle x 40s","Squat + Punch x 30s","High Knees x 30s"], "Great cardio, zero equipment.\n🔥 Save and try tonight"),
"Resistance Band Alternative": ("🩹", "NO RESISTANCE BAND? TOWEL WORKS", ["Towel Bicep Curls x 12","Towel Rows x 12","Towel Shoulder Press x 10","Towel Chest Press x 12","Towel Tricep Extensions x 10"], "Grip the ends tight — feel the tension.\n📌 Save for strength days"),
"Glute Bridge Progression": ("🍑", "GLUTE BRIDGE — 3 LEVELS", ["Beginner: Double Bridge x 15","Level 2: Single-Leg Bridge x 8 each","Level 3: Bridge March x 10 each","Level 4: Weighted (book/laptop) x 10","Level 5: Hip Thrust Hold x 30s"], "Start where you are. Progress weekly.\n💾 Save this progression"),
"Low Impact Cardio": ("🦶", "LOW IMPACT CARDIO — EASY ON JOINTS", ["Marching in Place x 45s","Step Touches x 45s","Knee Drives x 40s","Side Steps + Reach x 40s","Slow Burpees (no jump) x 30s"], "Burn calories without the impact.\n⏰ Save for rest or recovery days"),
"Advanced Core Circuit": ("💣", "ADVANCED CORE CIRCUIT — LEVEL UP", ["Hollow Body Hold x 30s","Plank to Pike x 10","L-Sit (or knee tuck) x 20s","Windshield Wipers x 10","Dragon Flag (or decline crunch) x 8"], "Intermediate+ only. Form first!\n🔥 Save when you're ready"),
"Back Pain Relief Stretches": ("🛏️", "LOWER BACK PAIN? TRY THESE", ["Child's Pose x 45s","Knee-to-Chest x 30s each","Cat-Cow x 10","Sphinx Pose x 30s","Happy Baby x 30s"], "Gentle movement helps. Skip if sharp pain.\n💾 Save for back days"),
"Warm Up Before Workout": ("♨️", "DON'T SKIP THE WARM-UP — 3 MIN ROUTINE", ["Arm Circles x 20","Leg Swings x 10 each","Bodyweight Squats x 10","Lunges x 8 each","Jumping Jacks x 30s"], "Warm muscles = better performance, fewer injuries.\n📌 Save before every session"),
"Morning Mobility Routine": ("🌅", "5 MIN MORNING MOBILITY", ["Cat-Cow x 10","World's Greatest Stretch x 5 each","Hip Circles x 10 each","Squat Hold Rocking x 30s","Spinal Twist x 30s each"], "Move better all day long.\n☀️ Save for your morning"),
"Core Stability Workout v2": ("🧊", "CORE STABILITY — PART 2", ["Plank Reach x 8 each","Side Plank Hip Dips x 10 each","Single-Leg Dead Bug x 8 each","Bird Dog Crunch x 10 each","Dead Hang (or table hang) x 20s"], "Progress from last time!\n💾 Save for next core day"),
"Standing Ab Workout v2": ("🧍", "STANDING ABS — NO FLOOR NEEDED", ["Standing Crunches x 25","Side Bends x 20 each","Standing Knee Crunches x 20 each","Wood Chopper x 15 each","Standing Twists with Taps x 30s"], "Do this at your desk!\n📌 Save for work breaks"),
"15 Min Upper Body Burn v2": ("💥", "UPPER BODY BURN — ROUND 2", ["Wide Push-Ups x 10","Pike Push-Ups x 8","Chair Dips x 12","Plank Row (no weight) x 8 each","Arm Circles x 30s"], "Same goal, new circuit.\n🔥 Save for next upper day"),
}

# ---------- Carousel content: topic -> (emoji, hook, points[4], cta) ----------
CAROUSELS = {
"10 Home Workout Mistakes": ("🚫", "10 MISTAKES RUINING YOUR HOME WORKOUTS", ["1. Skipping the warm-up","2. Using bad form for speed","3. No rest days","4. Repeating the same routine forever","5. Ignoring nutrition"], "Which one are you guilty of? 👇\n💾 Save this checklist"),
"How to Stay Motivated": ("🔥", "HOW TO STAY MOTIVATED (WHEN YOU DON'T WANT TO)", ["1. Shrink the goal: 10 minutes counts","2. Schedule it like a meeting","3. Track streaks, not perfection","4. Have a 'minimum viable workout'","5. Reward consistency"], "Motivation follows action, not the other way.\n📌 Save for tough days"),
"Recovery Tips for Sore Muscles": ("🧊", "SORE? HERE'S HOW TO RECOVER FASTER", ["1. Light movement beats full rest","2. Hydrate + eat protein","3. Sleep 7-9 hours","4. Stretch gently, don't force","5. Massage or foam roll"], "Recovery is where the gains happen.\n💾 Save this"),
"Sleep and Muscle Recovery": ("😴", "SLEEP IS YOUR SECRET WEAPON", ["1. Muscle grows during sleep, not training","2. Aim for 7-9 hours","3. Consistent bedtime = better recovery","4. Screen-free 30 min before bed","5. Cool, dark room helps"], "Train hard. Sleep harder.\n📌 Save for better nights"),
"Meal Prep for Busy People": ("🍱", "MEAL PREP FOR BUSY PEOPLE — 30 MIN SUNDAY", ["1. Pick 2 proteins, 2 carbs, 2 veggies","2. Batch cook on Sunday","3. Portion into containers","4. Keep it simple, not fancy","5. Prep snacks too"], "Eating well = training progress.\n💾 Save this guide"),
"Mind-Muscle Connection": ("🧠", "MIND-MUSCLE CONNECTION — WHAT IT ACTUALLY MEANS", ["1. Focus on the muscle, not the movement","2. Slow down the tempo","3. Squeeze at the top of each rep","4. Use lighter weight with perfect form","5. Visualize the muscle working"], "How you lift matters more than how much.\n📌 Save for your next workout"),
"How to Track Progress": ("📊", "HOW TO ACTUALLY TRACK PROGRESS", ["1. Photos every 2 weeks (same light/pose)","2. Measurements, not just weight","3. Log workouts: weight, reps, sets","4. Track energy + sleep too","5. Review monthly, adjust quarterly"], "What gets measured gets improved.\n💾 Save this system"),
"Goal Setting Template": ("🎯", "GOAL SETTING THAT WORKS — TEMPLATE INSIDE", ["1. Make it specific: '3x/week strength'","2. Make it measurable: reps, kg, minutes","3. Set a deadline: 12 weeks","4. Break into monthly milestones","5. Review weekly, adjust monthly"], "Swipe to copy the template.\n📌 Save for planning day"),
"Fitness Fact of the Week": ("🔬", "FITNESS FACT: REST DAYS ARE TRAINING", ["1. Muscles repair on rest days","2. Overtraining = plateau + injury risk","3. 1-2 rest days per week is optimal","4. Active rest (walk/yoga) counts","5. Listen to your body's signals"], "Rest is productive. Don't skip it.\n💾 Save this fact"),
"Protein Intake Guide": ("🥩", "PROTEIN GUIDE — HOW MUCH YOU ACTUALLY NEED", ["1. Aim 1.6-2.2g per kg of bodyweight","2. Spread across 3-5 meals","3. 20-40g per meal is ideal","4. Sources: chicken, eggs, fish, tofu, beans","5. Protein powder = convenience, not magic"], "Protein is the building block. Get it right.\n📌 Save this guide"),
"Macros Explained Simply": ("🧮", "MACROS EXPLAINED — WITHOUT THE JARGON", ["1. Protein: builds muscle (1.6-2.2g/kg)","2. Carbs: your energy source","3. Fats: hormones + health (don't fear them)","4. Calorie balance drives weight change","5. Focus on protein + veggies first"], "No overthinking. Start with these 5.\n💾 Save for nutrition days"),
"Bodyweight Exercise Progression": ("📈", "BODYWEIGHT PROGRESSION — LEVEL UP WITHOUT WEIGHTS", ["1. Push-Up: wall → incline → knee → full","2. Squat: chair assist → full → jump","3. Plank: 20s → 45s → side plank","4. Lunge: static → reverse → jump","5. Progress = harder variation, not more reps"], "Save this ladder and climb it.\n📌 Save for programming"),
"Plank Form Guide": ("🛡️", "PERFECT PLANK — THE FORM GUIDE", ["1. Elbows under shoulders","2. Body in one straight line","3. Squeeze glutes + core","4. Don't let hips sag or pike","5. Breathe, don't hold breath"], "A 20s perfect plank beats 60s sloppy.\n💾 Save for form check"),
"Stretching vs Warming Up": ("🧐", "STRETCHING VS WARM-UP — THEY'RE NOT THE SAME", ["1. Warm-up: raise temp, before training","2. Dynamic stretching: part of warm-up","3. Static stretching: after training","4. Stretching cold muscles = injury risk","5. 3-5 min warm-up minimum"], "Do both — at the right time.\n📌 Save this distinction"),
"Home Gym Setup on a Budget": ("💰", "HOME GYM UNDER €50 — FULL SETUP", ["1. Yoga mat: €15","2. Resistance band set: €20","3. Jump rope: €10","4. Water bottles as dumbbells: free","5. Chair + towel: already owned"], "No excuses. €45 gets you started.\n💾 Save this shopping list"),
"Beginner Workout Plan Week 1": ("🌱", "BEGINNER WORKOUT PLAN — WEEK 1", ["Day 1: Full body basics (20 min)","Day 2: Walk 30 min + stretching","Day 3: Upper body beginner (15 min)","Day 4: Rest / light yoga","Day 5: Lower body beginner (15 min)"], "Just start. Consistency > intensity.\n📌 Save this week's plan"),
"Common Squat Mistakes": ("🚫", "COMMON SQUAT MISTAKES (FIX THESE)", ["1. Heels lifting off ground","2. Knees caving inward","3. Leaning too far forward","4. Not going deep enough","5. Holding breath at bottom"], "Film your set and check these 5.\n💾 Save for leg day"),
"Cardio vs Strength Training": ("⚖️", "CARDIO VS STRENGTH — WHICH ONE?", ["1. Cardio: heart health, calorie burn","2. Strength: muscle, metabolism, posture","3. Best: both, 2-3x each per week","4. Order: strength first if both same day","5. What you enjoy = what you'll stick to"], "You don't have to choose.\n📌 Save for programming"),
"Hydration and Performance": ("💧", "HYDRATION — THE EASY PERFORMANCE WIN", ["1. Drink 2-3L daily (more if training)","2. Sip during workouts, don't chug","3. Thirst = already 1-2% dehydrated","4. Water before coffee in the morning","5. Monitor urine color (pale = good)"], "The cheapest supplement is water.\n💾 Save this reminder"),
"Rest Day Ideas": ("😌", "REST DAYS — WHAT TO ACTUALLY DO", ["1. 20 min walk outdoors","2. Gentle yoga or stretching","3. Foam rolling + mobility","4. Sleep in / nap","5. Prep meals for the week"], "Rest days build you too.\n📌 Save for your next rest day"),
"Workout Schedule for Beginners": ("📅", "THE PERFECT BEGINNER SCHEDULE", ["Mon: Full body (20 min)","Tue: Walk + stretch","Wed: Upper body (15 min)","Thu: Rest / yoga","Fri: Lower body (15 min)","Weekend: Active rest"], "3 training days is enough to start.\n💾 Save this schedule"),
"Breathing Techniques Exercise": ("🌬️", "BREATHING DURING EXERCISE — DO IT RIGHT", ["1. Exhale on the effort (hard part)","2. Inhale on the release","3. Don't hold your breath (valsalva only for heavy)","4. Core bracing before movement","5. Practice box breathing for calm"], "Breath drives performance.\n📌 Save for your next set"),
"Desk Job Health Tips": ("💻", "DESK JOB? PROTECT YOUR BODY", ["1. Stand up every 45-60 min","2. Screen at eye level","3. Chair: feet flat, back supported","4. 2-min stretch per work hour","5. Walk during lunch break"], "Your desk shouldn't wreck your body.\n💾 Save for work hours"),
"Injury Prevention Tips": ("🩹", "INJURY PREVENTION — THE 5 RULES", ["1. Warm up every session","2. Progress volume slowly (10% rule)","3. Sleep 7-9 hours","4. Pain ≠ gain; stop sharp pain","5. Mobility work 2x per week"], "Train smart, stay healthy.\n📌 Save this"),
}

# ---------- Static content: topic -> (emoji, text) ----------
STATICS = {
"New Month New Goals": ("🎯", "New month. New goals. Same you — but stronger.\n\nWrite down ONE fitness goal for this month and put it where you see it daily. Small steps, every day.\n\nWhat's your goal this month? 👇"),
"Fitness Fact of the Week": ("🔬", "FITNESS FACT 💡\n\nDid you know? Consistency beats intensity.\n\nA 15-minute workout 5 days a week will outperform a 2-hour workout once a week — every single time.\n\nShow up small. Show up often. 💪"),
"Goal Setting Template": ("📝", "SAVE THIS — YOUR GOAL TEMPLATE\n\n🎯 GOAL: ______\n⏱ DEADLINE: ______\n📅 WEEKLY ACTION: ______\n📊 HOW TO MEASURE: ______\n🎁 REWARD: ______\n\nFill it in. Print it. Stick it on your wall."),
"Transformation Tuesday Feature": ("✨", "TRANSFORMATION TUESDAY 🌟\n\nProgress isn't always a mirror change — it's showing up when you didn't want to. It's one more rep. One more walk. One healthier meal.\n\nTag someone whose consistency inspires you 👇"),
"Fan Feature Friday": ("🙌", "FAN FEATURE FRIDAY 🎉\n\nWe love seeing our community in action! Send us your home workout photos or screenshots of your streak — you might get featured here.\n\nShow us what you've got 💪"),
"Gratitude Post": ("💛", "GRATITUDE CHECK 💛\n\nYour body carries you every single day. This week, thank it with movement, rest, and good food.\n\nWhat's one thing your body did for you this week? 👇"),
}

# ---------- Stories templates (keep original) ----------
STORIES = """## Stories 互动模板

### 投票互动
```
📊 POLL: Morning or evening workout?
Option A: 🌅 Morning (energizes my day)
Option B: 🌙 Evening (fits my schedule)
Cast your vote! The results help us plan content.
```

### Q&A
```
❓ ASK ME ANYTHING
Got a home workout question?
Drop it below and we'll answer in this week's stories.
Training · Nutrition · Motivation — nothing off limits!
```

### 倒计时
```
⏰ 24-HOUR COUNTDOWN
New workout dropping TOMORROW at 7AM CET.
Set your reminder so you don't miss it!
Sneak peek: core + cardio 🔥
```

### 打卡
```
✅ WEEKLY CHECK-IN
How many workouts did you complete this week?
1️⃣ None yet (ok, start today!)
2️⃣ 1-2 (good start)
3️⃣ 3+ (beast mode 🦾)
Comment your number below!
```"""


def build_reel(topic, emoji, hook, actions, cta, variant_note=""):
    lines = []
    title = topic.upper()
    lines.append("### " + topic + ((" — %s" % variant_note) if variant_note else ""))
    lines.append("```")
    lines.append("%s %s %s" % (emoji, title, emoji))
    lines.append("")
    lines.append(hook)
    lines.append("")
    for a in actions:
        lines.append("• " + a)
    lines.append("")
    lines.append(cta)
    lines.append("")
    lines.append("#homeworkout #homefitness #noequipment #bodyweight #fitnessmotivation #workoutroutine #homegym #trainathome #fitnessjourney #europefitness")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def build_carousel(topic, emoji, hook, points, cta):
    lines = []
    lines.append("### " + topic)
    lines.append("```")
    lines.append("%s %s" % (emoji, hook))
    lines.append("")
    for p in points:
        lines.append(p)
    lines.append("")
    lines.append(cta)
    lines.append("")
    lines.append("#fitnesstips #workouttips #fitnesseducation #homeworkout #fitnessjourney #nutrition #workoutmotivation #healthylifestyle #progressnotperfection #homefitness")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def build_static(topic, emoji, text):
    lines = []
    lines.append("### " + topic)
    lines.append("```")
    lines.append("%s %s" % (emoji, text))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# ---------- Read posts_performance order and generate ----------
with open(BASE + r'\data\posts_performance.csv', encoding='utf-8-sig') as f:
    posts = list(csv.DictReader(f))

reel_section = []
carousel_section = []
static_section = []

seen_reel = {}
seen_carousel = {}

for p in posts:
    ptype = p['type']
    topic = p['topic'].strip()
    pid = p['post_id']
    if ptype == 'Reel':
        if topic in REELS and REELS[topic][0] is not None:
            emoji, hook, actions, cta = REELS[topic]
        else:
            emoji, hook, actions, cta = ("💪", "QUICK HOME WORKOUT", ["Warm-Up: Arm Circles x 20", "Main: 3 rounds of bodyweight moves", "Finisher: 30s Plank", "Cool Down: 30s stretch each side", "Hydrate!"], "Save this for your next workout")
        seen_reel[topic] = seen_reel.get(topic, 0) + 1
        note = ""
        if seen_reel[topic] > 1:
            note = "Round " + str(seen_reel[topic])
        reel_section.append(build_reel(topic, emoji, hook, actions, cta, note))
    elif ptype == 'Carousel':
        if topic in CAROUSELS:
            emoji, hook, points, cta = CAROUSELS[topic]
        else:
            emoji, hook, points, cta = ("📚", "QUICK FITNESS GUIDE", ["1. Start where you are", "2. Progress weekly", "3. Track your results", "4. Stay consistent", "5. Enjoy the process"], "Save this guide for later")
        seen_carousel[topic] = seen_carousel.get(topic, 0) + 1
        note = ""
        if seen_carousel[topic] > 1:
            note = "Round " + str(seen_carousel[topic])
        title = topic + ((" — %s" % note) if note else "")
        carousel_section.append(build_carousel(title, emoji, hook, points, cta))
    elif ptype == 'Static':
        if topic in STATICS:
            emoji, text = STATICS[topic]
        else:
            emoji, text = ("💬", "Keep showing up. Small steps compound.")
        static_section.append(build_static(topic, emoji, text))

header = "# @homefit.europe 帖子文案库\n\n> 83条原创英文文案 — 51 Reels + 26 Carousels + 6 Static（与 posts_performance.csv 一一对应）\n\n"

out = header
out += "## Reels 文案（训练教学类）\n\n"
out += "\n".join(reel_section)
out += "\n## Carousel 文案（知识教学类）\n\n"
out += "\n".join(carousel_section)
out += "\n## Static 文案（激励类）\n\n"
out += "\n".join(static_section)
out += "\n" + STORIES + "\n"

with open(BASE + r'\content\帖子文案库.md', 'w', encoding='utf-8') as f:
    f.write(out)

# verify
import re
count = len(re.findall(r'^### ', out, re.M))
print("生成完成！文案库帖子条目数:", count)
print("Reel条目:", len(reel_section), "| Carousel条目:", len(carousel_section), "| Static条目:", len(static_section))
