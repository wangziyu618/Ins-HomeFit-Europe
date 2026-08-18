"""
项目3：生成90天Ins模拟运营数据
- 每日粉丝增长/互动数据
- 帖子明细数据（Reels/Carousel/Static）
- 受众画像数据
- Stories数据
"""
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

np.random.seed(42)
base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\project3-ins"
data_dir = os.path.join(base_dir, "data")

start_date = datetime(2026, 1, 1)
days = 90
dates = [start_date + timedelta(days=i) for i in range(days)]

# ========== 1. 每日粉丝增长 ==========
daily_data = []
followers = 0
for i, d in enumerate(dates):
    # 粉丝增长：冷启动慢，中期加速，后期稳定
    if i < 30:
        new_followers = max(3, int(np.random.normal(18, 8) + i * 0.5))
    elif i < 60:
        new_followers = max(10, int(np.random.normal(45, 18) + (i-30) * 0.8))
    else:
        new_followers = max(20, int(np.random.normal(60, 22)))
    
    # 偶尔有爆款带来粉丝激增
    if np.random.random() < 0.06:
        new_followers += int(np.random.uniform(80, 250))
    
    unfollowed = int(new_followers * np.random.uniform(0.05, 0.15))
    followers += new_followers - unfollowed
    
    # 当日帖子数
    is_reel_day = d.weekday() in [0, 2, 4, 6]  # 周一三五日
    is_carousel_day = d.weekday() in [1, 3]     # 周二四
    posts_today = (1 if is_reel_day else 0) + (1 if is_carousel_day else 0)
    if np.random.random() < 0.1:
        posts_today += 1  # 偶尔加发static
    
    # Stories
    stories_count = np.random.choice([2, 3, 3, 4], p=[0.2, 0.4, 0.2, 0.2])
    story_views = int(followers * np.random.uniform(0.15, 0.35))
    
    # 当日互动
    base_engagement = int(followers * np.random.uniform(0.03, 0.06))
    
    daily_data.append({
        'date': d.strftime('%Y-%m-%d'),
        'day_of_week': d.strftime('%A'),
        'new_followers': new_followers,
        'unfollowed': unfollowed,
        'net_followers': new_followers - unfollowed,
        'total_followers': followers,
        'posts_count': posts_today,
        'stories_count': stories_count,
        'story_views': story_views,
        'daily_likes': base_engagement,
        'daily_comments': int(base_engagement * np.random.uniform(0.08, 0.15)),
        'daily_saves': int(base_engagement * np.random.uniform(0.1, 0.2)),
        'daily_shares': int(base_engagement * np.random.uniform(0.05, 0.12)),
        'profile_visits': int(followers * np.random.uniform(0.08, 0.18)),
        'website_clicks': int(followers * np.random.uniform(0.01, 0.04))
    })

df_daily = pd.DataFrame(daily_data)
df_daily.to_csv(os.path.join(data_dir, 'daily_metrics.csv'), index=False, encoding='utf-8-sig')

# ========== 2. 帖子明细数据 ==========
reel_topics = [
    '15 Min Morning Fat Burn', 'No-Equipment Ab Workout', 'Office Desk Stretch Routine',
    '5 Min Bedtime Core', 'Full Body HIIT at Home', 'Push-Up Progression Guide',
    'Squat Form Correction', '10 Min Leg Day No Equipment', 'Morning Yoga Flow',
    'Post-Workout Stretch', 'Plank Challenge Variations', 'Lunge Mistakes to Avoid',
    '15 Min Upper Body Burn', 'Resistance Band Alternative', 'Cool Down Routine',
    '30-Day Squat Challenge Day 1', 'Booty Band Workout at Home', 'Quick Cardio Blast',
    'Beginner Full Body Workout', 'Advanced Core Circuit', 'Shoulder Mobility Routine',
    'Back Pain Relief Stretches', 'Warm Up Before Workout', '15 Min Arm Workout',
    'Burpee Alternatives', 'Mountain Climber Variations', 'Glute Bridge Progression',
    'Standing Ab Workout', 'Low Impact Cardio', 'Jump Rope Alternative Home',
    '15 Min Full Body Stretch', 'Desk Posture Fixes', 'Morning Mobility Routine',
    'No Jump Cardio', 'Core Stability Workout', 'Push Day at Home',
    'Pull Day Bodyweight', 'Leg Day No Squats', 'Endurance Circuit',
    'Power Yoga for Strength', 'Pilates Core Workout', 'Balance Training Routine',
    'Reaction Time Drills', 'Flexibility Routine', 'Posture Correction Exercises',
    'Neck & Shoulder Tension Relief', 'Hip Opener Stretches', 'Wrist Mobility Exercises',
    'Ankle Stability Drills', '15 Min Boxing Workout', 'Dance Cardio Fun',
    'Kettlebell Alternative Home', 'TRX Alternative Exercises'
]

carousel_topics = [
    'How to Do a Perfect Push-Up', '10 Home Workout Mistakes', 'Protein Intake Guide',
    'Beginner Workout Plan Week 1', 'Stretching vs Warming Up', 'How to Stay Motivated',
    'Home Gym Setup on a Budget', 'Recovery Tips for Sore Muscles', 'Macros Explained Simply',
    '30-Day Challenge Calendar', 'Common Squat Mistakes', 'Sleep and Muscle Recovery',
    'Bodyweight Exercise Progression', 'Meal Prep for Busy People', 'Plank Form Guide',
    'How to Start Working Out', 'Cardio vs Strength Training', 'Hydration and Performance',
    'Mind-Muscle Connection', 'Rest Day Ideas', 'Workout Schedule for Beginners',
    'How to Track Progress', 'Injury Prevention Tips', 'Breathing Techniques Exercise',
    'Cold Weather Workout Motivation', 'Desk Job Health Tips'
]

static_topics = [
    'Motivation Monday Quote', 'Transformation Tuesday Feature', 'Weekend Workout Reminder',
    'New Month New Goals', 'Community Shoutout', 'Progress Not Perfection',
    'Rest Day Reminder', 'Fitness Fact of the Week', 'Fan Feature Friday',
    'Weekly Recap', 'Goal Setting Template', 'Gratitude Post'
]

posts = []
post_id = 1
for i, d in enumerate(dates):
    is_reel_day = d.weekday() in [0, 2, 4, 6]
    is_carousel_day = d.weekday() in [1, 3]
    
    if is_reel_day:
        topic = reel_topics[post_id % len(reel_topics)]
        post_type = 'Reel'
        # Reels数据：播放量远大于粉丝数（算法推荐）
        base_views = int(df_daily.iloc[i]['total_followers'] * np.random.uniform(2, 8))
        if np.random.random() < 0.12:  # 12%概率爆款
            base_views = int(base_views * np.random.uniform(3, 8))
        likes = int(base_views * np.random.uniform(0.025, 0.06))
        comments = int(likes * np.random.uniform(0.05, 0.12))
        saves = int(likes * np.random.uniform(0.10, 0.25))
        shares = int(likes * np.random.uniform(0.05, 0.15))
        reach = int(base_views * np.random.uniform(0.85, 1.0))
        posts.append({
            'post_id': f'P{post_id:03d}', 'date': d.strftime('%Y-%m-%d'),
            'type': post_type, 'topic': topic,
            'views': base_views, 'likes': likes, 'comments': comments,
            'saves': saves, 'shares': shares, 'reach': reach,
            'engagement_rate': round((likes+comments+saves+shares)/max(base_views,1)*100, 2),
            'time_posted': '07:00' if d.weekday() != 6 else '10:00',
            'hashtags_count': np.random.randint(10, 16)
        })
        post_id += 1
    
    if is_carousel_day:
        topic = carousel_topics[post_id % len(carousel_topics)]
        post_type = 'Carousel'
        base_likes = int(df_daily.iloc[i]['total_followers'] * np.random.uniform(0.025, 0.06))
        comments = int(base_likes * np.random.uniform(0.04, 0.10))
        saves = int(base_likes * np.random.uniform(0.15, 0.35))
        shares = int(base_likes * np.random.uniform(0.04, 0.12))
        reach = int(df_daily.iloc[i]['total_followers'] * np.random.uniform(0.5, 0.8))
        posts.append({
            'post_id': f'P{post_id:03d}', 'date': d.strftime('%Y-%m-%d'),
            'type': post_type, 'topic': topic,
            'views': 0, 'likes': base_likes, 'comments': comments,
            'saves': saves, 'shares': shares, 'reach': reach,
            'engagement_rate': round((base_likes+comments+saves+shares)/max(reach,1)*100, 2),
            'time_posted': '12:30',
            'hashtags_count': np.random.randint(8, 13)
        })
        post_id += 1
    
    # 偶尔static
    if np.random.random() < 0.1:
        topic = static_topics[post_id % len(static_topics)]
        post_type = 'Static'
        base_likes = int(df_daily.iloc[i]['total_followers'] * np.random.uniform(0.02, 0.05))
        comments = int(base_likes * np.random.uniform(0.03, 0.08))
        saves = int(base_likes * np.random.uniform(0.03, 0.10))
        shares = int(base_likes * np.random.uniform(0.01, 0.06))
        reach = int(df_daily.iloc[i]['total_followers'] * np.random.uniform(0.5, 0.8))
        posts.append({
            'post_id': f'P{post_id:03d}', 'date': d.strftime('%Y-%m-%d'),
            'type': post_type, 'topic': topic,
            'views': 0, 'likes': base_likes, 'comments': comments,
            'saves': saves, 'shares': shares, 'reach': reach,
            'engagement_rate': round((base_likes+comments+saves+shares)/max(reach,1)*100, 2),
            'time_posted': np.random.choice(['09:00','18:00','20:00']),
            'hashtags_count': np.random.randint(5, 10)
        })
        post_id += 1

df_posts = pd.DataFrame(posts)
df_posts.to_csv(os.path.join(data_dir, 'posts_performance.csv'), index=False, encoding='utf-8-sig')

# ========== 3. 受众画像 ==========
audience = {
    'countries': [
        {'country': 'Germany', 'percentage': 28},
        {'country': 'UK', 'percentage': 24},
        {'country': 'France', 'percentage': 16},
        {'country': 'Netherlands', 'percentage': 12},
        {'country': 'Spain', 'percentage': 7},
        {'country': 'Italy', 'percentage': 6},
        {'country': 'Sweden', 'percentage': 4},
        {'country': 'Other', 'percentage': 3}
    ],
    'age_groups': [
        {'group': '18-24', 'percentage': 18},
        {'group': '25-34', 'percentage': 42},
        {'group': '35-44', 'percentage': 28},
        {'group': '45-54', 'percentage': 9},
        {'group': '55+', 'percentage': 3}
    ],
    'gender': [
        {'gender': 'Female', 'percentage': 58},
        {'gender': 'Male', 'percentage': 39},
        {'gender': 'Other', 'percentage': 3}
    ],
    'active_hours': [
        {'hour': '06:00', 'activity': 45}, {'hour': '07:00', 'activity': 78},
        {'hour': '08:00', 'activity': 62}, {'hour': '09:00', 'activity': 35},
        {'hour': '10:00', 'activity': 28}, {'hour': '11:00', 'activity': 30},
        {'hour': '12:00', 'activity': 72}, {'hour': '13:00', 'activity': 55},
        {'hour': '14:00', 'activity': 32}, {'hour': '15:00', 'activity': 28},
        {'hour': '16:00', 'activity': 35}, {'hour': '17:00', 'activity': 48},
        {'hour': '18:00', 'activity': 75}, {'hour': '19:00', 'activity': 88},
        {'hour': '20:00', 'activity': 95}, {'hour': '21:00', 'activity': 82},
        {'hour': '22:00', 'activity': 55}, {'hour': '23:00', 'activity': 25}
    ],
    'follower_growth_by_phase': [
        {'phase': 'Day 1-30 (冷启动)', 'start': 0, 'end': int(df_daily.iloc[29]['total_followers']), 'avg_daily': int(df_daily.iloc[:30]['new_followers'].mean())},
        {'phase': 'Day 31-60 (增长期)', 'start': int(df_daily.iloc[29]['total_followers']), 'end': int(df_daily.iloc[59]['total_followers']), 'avg_daily': int(df_daily.iloc[30:60]['new_followers'].mean())},
        {'phase': 'Day 61-90 (加速期)', 'start': int(df_daily.iloc[59]['total_followers']), 'end': int(df_daily.iloc[89]['total_followers']), 'avg_daily': int(df_daily.iloc[60:90]['new_followers'].mean())}
    ]
}

with open(os.path.join(data_dir, 'audience_insights.json'), 'w', encoding='utf-8') as f:
    json.dump(audience, f, ensure_ascii=False, indent=2)

# ========== 4. 内容类型表现汇总 ==========
type_summary = []
for ptype in ['Reel', 'Carousel', 'Static']:
    tdf = df_posts[df_posts['type'] == ptype]
    type_summary.append({
        'type': ptype,
        'count': len(tdf),
        'avg_likes': int(tdf['likes'].mean()),
        'avg_comments': int(tdf['comments'].mean()),
        'avg_saves': int(tdf['saves'].mean()),
        'avg_shares': int(tdf['shares'].mean()),
        'avg_engagement_rate': round(tdf['engagement_rate'].mean(), 2),
        'total_reach': int(tdf['reach'].sum()),
        'avg_views': int(tdf['views'].mean()) if ptype == 'Reel' else 0
    })

with open(os.path.join(data_dir, 'content_type_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(type_summary, f, ensure_ascii=False, indent=2)

# ========== 5. Top 10帖子 ==========
df_posts['total_engagement'] = df_posts['likes'] + df_posts['comments'] + df_posts['saves'] + df_posts['shares']
top_posts = df_posts.nlargest(10, 'total_engagement')[['post_id','date','type','topic','views','likes','comments','saves','shares','engagement_rate','total_engagement']].to_dict('records')
with open(os.path.join(data_dir, 'top_posts.json'), 'w', encoding='utf-8') as f:
    json.dump(top_posts, f, ensure_ascii=False, indent=2)

# ========== 6. 关键洞察 ==========
final_followers = int(df_daily.iloc[-1]['total_followers'])
avg_er = round(df_posts['engagement_rate'].mean(), 2)
reel_er = round(df_posts[df_posts['type']=='Reel']['engagement_rate'].mean(), 2)
carousel_er = round(df_posts[df_posts['type']=='Carousel']['engagement_rate'].mean(), 2)
best_post = df_posts.loc[df_posts['total_engagement'].idxmax()]

insights = [
    {'type':'success','title':'90天粉丝增长达标','desc':f'最终粉丝{final_followers}，超过5000目标，日均增长{int(df_daily["new_followers"].mean())}人'},
    {'type':'success','title':'互动率高于行业均值','desc':f'整体互动率{avg_er}%，Reels互动率{reel_er}%，高于健身微型博主3-6%基准'},
    {'type':'info','title':'Carousel收藏率最高','desc':f'Carousel互动率{carousel_er}%，收藏占比高，教学类内容长尾价值强'},
    {'type':'warning','title':'Static帖子表现弱','desc':'静态图互动率仅2-3%，建议减少频率，将资源集中在Reels和Carousel'},
    {'type':'success','title':'爆款内容验证','desc':f'最佳帖子"{best_post["topic"]}"({best_post["type"]})获得{int(best_post["total_engagement"])}次互动，验证训练教学方向'},
    {'type':'info','title':'德国英国为核心受众','desc':'德国(28%)+英国(24%)占受众52%，内容可增加欧洲本地化元素'},
    {'type':'warning','title':'晚间8点为流量高峰','desc':'20:00活跃度最高(95%)，建议Reels发布时间从7AM调整部分至6-8PM测试'}
]

with open(os.path.join(data_dir, 'insights.json'), 'w', encoding='utf-8') as f:
    json.dump(insights, f, ensure_ascii=False, indent=2)

print(f"=== 项目3数据生成完成 ===")
print(f"每日数据: {len(df_daily)}天")
print(f"帖子数据: {len(df_posts)}条 (Reels:{len(df_posts[df_posts['type']=='Reel'])}, Carousels:{len(df_posts[df_posts['type']=='Carousel'])}, Static:{len(df_posts[df_posts['type']=='Static'])})")
print(f"最终粉丝: {final_followers}")
print(f"平均互动率: {avg_er}%")
print(f"最佳帖子: {best_post['topic']} ({best_post['type']}) - {int(best_post['total_engagement'])} engagements")
