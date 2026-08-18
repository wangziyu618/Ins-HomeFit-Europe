"""生成90天内容日历CSV"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(123)
base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\project3-ins"

reel_topics = [
    '15 Min Morning Fat Burn', 'No-Equipment Ab Workout', 'Office Desk Stretch Routine',
    '5 Min Bedtime Core', 'Full Body HIIT at Home', 'Push-Up Progression Guide',
    'Squat Form Correction', '10 Min Leg Day No Equipment', 'Morning Yoga Flow',
    'Post-Workout Stretch', 'Plank Challenge Variations', 'Lunge Mistakes to Avoid',
    '15 Min Upper Body Burn', 'Cool Down Routine', '30-Day Squat Challenge',
    'Quick Cardio Blast', 'Beginner Full Body Workout', 'Advanced Core Circuit',
    'Shoulder Mobility Routine', 'Back Pain Relief Stretches', 'Warm Up Before Workout',
    '15 Min Arm Workout', 'Burpee Alternatives', 'Mountain Climber Variations',
    'Glute Bridge Progression', 'Standing Ab Workout', 'Low Impact Cardio',
    '15 Min Full Body Stretch', 'Desk Posture Fixes', 'Morning Mobility Routine',
    'No Jump Cardio', 'Core Stability Workout', 'Push Day at Home',
    'Pull Day Bodyweight', 'Leg Day No Squats', 'Endurance Circuit',
    'Power Yoga for Strength', 'Pilates Core Workout', 'Balance Training Routine',
    'Posture Correction Exercises', 'Neck & Shoulder Tension Relief',
    'Hip Opener Stretches', 'Wrist Mobility Exercises', 'Ankle Stability Drills',
    '15 Min Boxing Workout', 'Dance Cardio Fun', 'Kettlebell Alternative Home',
    'TRX Alternative Exercises', 'Resistance Band Full Body', 'Friday Finisher Circuit'
]

carousel_topics = [
    'How to Do a Perfect Push-Up', '10 Home Workout Mistakes', 'Protein Intake Guide',
    'Beginner Workout Plan Week 1', 'Stretching vs Warming Up', 'How to Stay Motivated',
    'Recovery Tips for Sore Muscles', 'Macros Explained Simply', '30-Day Challenge Calendar',
    'Common Squat Mistakes', 'Sleep and Muscle Recovery', 'Bodyweight Exercise Progression',
    'Meal Prep for Busy People', 'Plank Form Guide', 'How to Start Working Out',
    'Cardio vs Strength Training', 'Hydration and Performance', 'Mind-Muscle Connection',
    'Rest Day Ideas', 'Workout Schedule for Beginners', 'How to Track Progress',
    'Injury Prevention Tips', 'Breathing Techniques Exercise', 'Desk Job Health Tips',
    'Foam Rolling Guide', 'Cold Weather Workout Motivation'
]

static_topics = [
    'Motivation Monday Quote', 'Transformation Tuesday Feature', 'Weekend Workout Reminder',
    'New Month New Goals', 'Community Shoutout', 'Progress Not Perfection'
]

calendar = []
start = datetime(2026, 1, 1)
ri, ci, si = 0, 0, 0

for day in range(90):
    d = start + timedelta(days=day)
    wd = d.weekday()
    
    # Reels: Mon(0), Wed(2), Fri(4), Sun(6)
    if wd in [0, 2, 4, 6]:
        topic = reel_topics[ri % len(reel_topics)]
        ri += 1
        time_posted = '10:00' if wd == 6 else '07:00'
        calendar.append({
            'date': d.strftime('%Y-%m-%d'), 'day': d.strftime('%A'),
            'content_type': 'Reel', 'topic': topic, 'pillar': '训练教学',
            'time_posted': time_posted, 'status': '已发布',
            'hashtags': '#homeworkout #fitness #workout #15minuteworkout #nogymneeded #bodyweightworkout #fitnessmotivation #homefitness'
        })
    
    # Carousel: Tue(1), Thu(3)
    if wd in [1, 3]:
        topic = carousel_topics[ci % len(carousel_topics)]
        ci += 1
        calendar.append({
            'date': d.strftime('%Y-%m-%d'), 'day': d.strftime('%A'),
            'content_type': 'Carousel', 'topic': topic, 'pillar': '健身知识',
            'time_posted': '12:30', 'status': '已发布',
            'hashtags': '#fitnesstips #workouttips #fitnesseducation #homeworkout #fitnessjourney #nutrition #workoutmotivation'
        })
    
    # Static: 偶尔周六
    if wd == 5 and np.random.random() < 0.15:
        topic = static_topics[si % len(static_topics)]
        si += 1
        calendar.append({
            'date': d.strftime('%Y-%m-%d'), 'day': d.strftime('%A'),
            'content_type': 'Static', 'topic': topic, 'pillar': '动力激励',
            'time_posted': '09:00', 'status': '已发布',
            'hashtags': '#motivation #fitnessmotivation #mindset #fitnessjourney'
        })
    
    # Stories every day
    calendar.append({
        'date': d.strftime('%Y-%m-%d'), 'day': d.strftime('%A'),
        'content_type': 'Story', 'topic': 'Daily stories (poll/Q&A/check-in)',
        'pillar': '互动日常', 'time_posted': '07:00/12:30/20:00',
        'status': '已发布', 'hashtags': ''
    })

df_cal = pd.DataFrame(calendar)
df_cal.to_csv(os.path.join(base_dir, 'content', 'content_calendar.csv'), index=False, encoding='utf-8-sig')
print(f"内容日历生成完成: {len(df_cal)}条记录")
print(f"Reels: {len(df_cal[df_cal['content_type']=='Reel'])}")
print(f"Carousels: {len(df_cal[df_cal['content_type']=='Carousel'])}")
print(f"Static: {len(df_cal[df_cal['content_type']=='Static'])}")
print(f"Stories: {len(df_cal[df_cal['content_type']=='Story'])}")
