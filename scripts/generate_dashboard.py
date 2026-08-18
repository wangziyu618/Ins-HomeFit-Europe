"""
生成项目3交互式运营看板HTML
"""
import pandas as pd
import json
import os

base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\project3-ins"
data_dir = os.path.join(base_dir, "data")

# 读取数据
df_daily = pd.read_csv(os.path.join(data_dir, 'daily_metrics.csv'))
df_posts = pd.read_csv(os.path.join(data_dir, 'posts_performance.csv'))

with open(os.path.join(data_dir, 'audience_insights.json'), 'r', encoding='utf-8') as f:
    audience = json.load(f)
with open(os.path.join(data_dir, 'content_type_summary.json'), 'r', encoding='utf-8') as f:
    type_summary = json.load(f)
with open(os.path.join(data_dir, 'top_posts.json'), 'r', encoding='utf-8') as f:
    top_posts = json.load(f)
with open(os.path.join(data_dir, 'insights.json'), 'r', encoding='utf-8') as f:
    insights = json.load(f)

# 聚合数据
dashboard_data = {
    'metrics': {
        'final_followers': int(df_daily.iloc[-1]['total_followers']),
        'total_posts': int(len(df_posts)),
        'total_reels': int(len(df_posts[df_posts['type']=='Reel'])),
        'total_carousels': int(len(df_posts[df_posts['type']=='Carousel'])),
        'avg_engagement_rate': round(float(df_posts['engagement_rate'].mean()), 2),
        'total_likes': int(df_posts['likes'].sum()),
        'total_comments': int(df_posts['comments'].sum()),
        'total_saves': int(df_posts['saves'].sum()),
        'total_shares': int(df_posts['shares'].sum()),
        'total_reach': int(df_posts['reach'].sum()),
        'total_views': int(df_posts['views'].sum()),
        'avg_story_views': int(df_daily['story_views'].mean()),
        'avg_daily_new_followers': int(df_daily['new_followers'].mean()),
        'best_er': round(float(df_posts['engagement_rate'].max()), 2),
        'days': 90
    },
    'follower_growth': [
        {'date': r['date'], 'followers': int(r['total_followers']), 'new': int(r['new_followers']), 'unfollowed': int(r['unfollowed'])}
        for _, r in df_daily.iterrows()
    ],
    'daily_engagement': [
        {'date': r['date'], 'likes': int(r['daily_likes']), 'comments': int(r['daily_comments']),
         'saves': int(r['daily_saves']), 'shares': int(r['daily_shares']),
         'profile_visits': int(r['profile_visits']), 'website_clicks': int(r['website_clicks'])}
        for _, r in df_daily.iterrows()
    ],
    'content_types': type_summary,
    'audience': audience,
    'top_posts': top_posts,
    'insights': insights,
    'posts_scatter': [
        {'date': r['date'], 'type': r['type'], 'likes': int(r['likes']),
         'er': float(r['engagement_rate']), 'topic': r['topic'], 'views': int(r['views'])}
        for _, r in df_posts.iterrows()
    ]
}

json_path = os.path.join(base_dir, 'dashboard', 'dashboard_data.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=2)

data_json = json.dumps(dashboard_data, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@homefit.europe 运营数据看板</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
:root{--bg:#f0f2f5;--card:#fff;--text:#1a1a2e;--sec:#6b7280;--primary:#e1306c;--p2:#c13584;--p3:#833ab4;--border:#e5e7eb;--success:#38a169;--warning:#dd6b20;--danger:#e53e3e;--info:#3182ce;--shadow:0 2px 12px rgba(0,0,0,.08);--shadow-h:0 8px 24px rgba(0,0,0,.12)}
[data-theme="dark"]{--bg:#0f172a;--card:#1e293b;--text:#f1f5f9;--sec:#94a3b8;--primary:#f472b6;--p2:#e879f9;--p3:#a78bfa;--border:#334155;--shadow:0 2px 12px rgba(0,0,0,.3);--shadow-h:0 8px 24px rgba(0,0,0,.4)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Microsoft YaHei',sans-serif;background:var(--bg);color:var(--text);padding:16px;transition:background .3s,color .3s}
.navbar{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;background:linear-gradient(135deg,#833ab4 0%,#c13584 50%,#e1306c 100%);color:#fff;border-radius:12px;margin-bottom:16px;box-shadow:var(--shadow);flex-wrap:wrap;gap:12px}
.navbar h1{font-size:22px}.navbar .sub{font-size:13px;opacity:.85;margin-top:2px}
.nav-right{display:flex;gap:10px}
.nav-btn{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);color:#fff;padding:8px 14px;border-radius:8px;cursor:pointer;font-size:13px;transition:all .2s}
.nav-btn:hover{background:rgba(255,255,255,.25)}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px}
.kpi{background:var(--card);padding:16px;border-radius:10px;box-shadow:var(--shadow);border-top:3px solid var(--primary);transition:all .3s}
.kpi:hover{transform:translateY(-3px);box-shadow:var(--shadow-h)}
.kpi .l{font-size:12px;color:var(--sec);margin-bottom:6px}
.kpi .v{font-size:24px;font-weight:700;color:var(--text)}
.kpi .u{font-size:12px;color:var(--sec);font-weight:400;margin-left:3px}
.kpi:nth-child(2){border-top-color:var(--success)}.kpi:nth-child(3){border-top-color:var(--warning)}
.kpi:nth-child(4){border-top-color:var(--p3)}.kpi:nth-child(5){border-top-color:var(--info)}
.kpi:nth-child(6){border-top-color:var(--success)}
.insights{background:var(--card);border-radius:10px;padding:16px 20px;margin-bottom:16px;box-shadow:var(--shadow)}
.insights h3{font-size:15px;margin-bottom:12px}
.insights-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px}
.ins{padding:10px 14px;border-radius:8px;border-left:3px solid;font-size:13px;line-height:1.5}
.ins .t{font-weight:600;margin-bottom:3px;font-size:13px}
.ins .d{color:var(--sec);font-size:12px}
.ins.success{border-color:var(--success);background:rgba(56,161,105,.08)}
.ins.warning{border-color:var(--warning);background:rgba(221,107,32,.08)}
.ins.danger{border-color:var(--danger);background:rgba(229,62,62,.08)}
.ins.info{border-color:var(--info);background:rgba(49,130,206,.08)}
.charts{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-bottom:16px}
.cc{background:var(--card);padding:16px;border-radius:10px;box-shadow:var(--shadow)}
.cc.full{grid-column:1/-1}
.cc h3{font-size:14px;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.box{width:100%;height:300px}
.table-card{background:var(--card);border-radius:10px;padding:16px 20px;margin-bottom:16px;box-shadow:var(--shadow);overflow-x:auto}
.table-card h3{font-size:15px;margin-bottom:12px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{background:var(--bg);padding:10px 12px;text-align:left;font-weight:600;color:var(--sec);border-bottom:2px solid var(--border);white-space:nowrap}
td{padding:9px 12px;border-bottom:1px solid var(--border)}
tr:hover td{background:rgba(225,48,108,.05)}
.num{text-align:right;font-variant-numeric:tabular-nums}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:500}
.badge.reel{background:rgba(225,48,108,.15);color:var(--primary)}
.badge.carousel{background:rgba(131,58,180,.15);color:var(--p3)}
.badge.static{background:rgba(49,130,206,.15);color:var(--info)}
.footer{text-align:center;padding:16px;color:var(--sec);font-size:12px}
@media(max-width:900px){.charts{grid-template-columns:1fr}.navbar h1{font-size:18px}.kpi .v{font-size:20px}}
</style>
</head>
<body>
<div class="navbar">
  <div><h1>📱 @homefit.europe 运营数据看板</h1><div class="sub">90天Instagram模拟运营 | 2026.01.01 - 2026.03.31 | 欧洲居家健身</div></div>
  <div class="nav-right"><button class="nav-btn" onclick="toggleTheme()">🌙 深色模式</button><button class="nav-btn" onclick="toggleFS()">⛶ 全屏</button></div>
</div>
<div class="kpi-grid" id="kpiGrid"></div>
<div class="insights"><h3>💡 运营洞察</h3><div class="insights-grid" id="insightsGrid"></div></div>
<div class="charts">
  <div class="cc full"><h3>📈 粉丝增长趋势（90天）</h3><div id="growthChart" class="box"></div></div>
  <div class="cc"><h3>📊 内容类型表现对比</h3><div id="typeChart" class="box"></div></div>
  <div class="cc"><h3>🌍 受众国家分布</h3><div id="countryChart" class="box"></div></div>
  <div class="cc"><h3>👥 受众年龄分布</h3><div id="ageChart" class="box"></div></div>
  <div class="cc"><h3>⏰ 受众活跃时间（CET）</h3><div id="hourChart" class="box"></div></div>
  <div class="cc full"><h3>🔥 每日互动趋势</h3><div id="engagementChart" class="box"></div></div>
  <div class="cc full"><h3>⭐ 帖子互动率分布（按类型）</h3><div id="scatterChart" class="box"></div></div>
</div>
<div class="table-card"><h3>🏆 Top 10 最佳帖子</h3>
  <table><thead><tr><th>ID</th><th>日期</th><th>类型</th><th>主题</th><th class="num">播放/触达</th><th class="num">点赞</th><th class="num">评论</th><th class="num">收藏</th><th class="num">分享</th><th class="num">互动率</th></tr></thead><tbody id="topTable"></tbody></table>
</div>
<div class="footer">@homefit.europe 模拟运营项目 | 数据基于Instagram健身行业基准生成 | Python + ECharts</div>
<script>
const D=''' + data_json + ''';
let charts={};
function toggleTheme(){const h=document.documentElement,d=h.getAttribute('data-theme')==='dark';h.setAttribute('data-theme',d?'light':'dark');document.querySelector('.nav-btn').textContent=d?'🌙 深色模式':'☀️ 浅色模式';setTimeout(()=>Object.values(charts).forEach(c=>c&&c.resize()),100)}
function toggleFS(){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}
function C(){const t=document.documentElement.getAttribute('data-theme')==='dark';return{text:t?'#f1f5f9':'#333',sec:t?'#94a3b8':'#666',grid:t?'#334155':'#eee',p:'#e1306c',p2:'#c13584',p3:'#833ab4',s:'#38a169',w:'#dd6b20',i:'#3182ce'}}
function renderKPI(){const m=D.metrics;const k=[
{l:'最终粉丝',v:m.final_followers.toLocaleString(),u:'人'},
{l:'发布帖子',v:m.total_posts,u:'条'},
{l:'平均互动率',v:m.avg_engagement_rate,u:'%'},
{l:'总点赞',v:(m.total_likes/1000).toFixed(1),u:'K'},
{l:'总收藏',v:(m.total_saves/1000).toFixed(1),u:'K'},
{l:'总分享',v:(m.total_shares/1000).toFixed(1),u:'K'}
];document.getElementById('kpiGrid').innerHTML=k.map(x=>'<div class="kpi"><div class="l">'+x.l+'</div><div class="v">'+x.v+'<span class="u">'+x.u+'</span></div></div>').join('')}
function renderInsights(){const ic={success:'✅',warning:'⚠️',danger:'🚨',info:'ℹ️'};document.getElementById('insightsGrid').innerHTML=D.insights.map(i=>'<div class="ins '+i.type+'"><div class="t">'+ic[i.type]+' '+i.title+'</div><div class="d">'+i.desc+'</div></div>').join('')}
function renderTable(){document.getElementById('topTable').innerHTML=D.top_posts.map(p=>'<tr><td>'+p.post_id+'</td><td>'+p.date+'</td><td><span class="badge '+p.type.toLowerCase()+'">'+p.type+'</span></td><td>'+p.topic+'</td><td class="num">'+(p.views>0?p.views.toLocaleString():p.reach.toLocaleString())+'</td><td class="num">'+p.likes.toLocaleString()+'</td><td class="num">'+p.comments+'</td><td class="num">'+p.saves+'</td><td class="num">'+p.shares+'</td><td class="num" style="font-weight:600;color:var(--primary)">'+p.engagement_rate+'%</td></tr>').join('')}
function init(){['growthChart','typeChart','countryChart','ageChart','hourChart','engagementChart','scatterChart'].forEach(id=>charts[id]=echarts.init(document.getElementById(id)))}
function update(){
  const c=C(),tt={triggerOn:'click',renderMode:'richText',confine:true,textStyle:{fontSize:11}};
  // 粉丝增长
  charts.growthChart.setOption({backgroundColor:'transparent',tooltip:{...tt,trigger:'axis'},legend:{data:['总粉丝','新增粉丝'],top:0,textStyle:{fontSize:11,color:c.sec}},
    grid:{left:60,right:60,top:30,bottom:40,containLabel:true},
    xAxis:{type:'category',data:D.follower_growth.map(x=>x.date),axisLabel:{fontSize:10,color:c.sec,rotate:45},axisLine:{lineStyle:{color:c.grid}}},
    yAxis:[{type:'value',name:'粉丝数',axisLabel:{fontSize:11,color:c.sec},splitLine:{lineStyle:{color:c.grid}}},{type:'value',name:'新增',axisLabel:{fontSize:11,color:c.sec},splitLine:{show:false}}],
    series:[
      {name:'总粉丝',type:'line',data:D.follower_growth.map(x=>x.followers),smooth:true,symbol:'none',lineStyle:{color:c.p,width:2.5},areaStyle:{color:{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(225,48,108,0.25)'},{offset:1,color:'rgba(225,48,108,0.02)'}]}}},
      {name:'新增粉丝',type:'bar',yAxisIndex:1,data:D.follower_growth.map(x=>x.new),itemStyle:{color:c.p3,opacity:0.5},barWidth:4}
    ]});
  // 内容类型对比
  charts.typeChart.setOption({backgroundColor:'transparent',tooltip:{...tt,trigger:'axis'},legend:{bottom:0,textStyle:{fontSize:10,color:c.sec}},
    grid:{left:50,right:20,top:20,bottom:40,containLabel:true},
    xAxis:{type:'category',data:D.content_types.map(x=>x.type),axisLabel:{color:c.sec}},
    yAxis:{type:'value',axisLabel:{fontSize:11,color:c.sec},splitLine:{lineStyle:{color:c.grid}}},
    series:[
      {name:'平均点赞',type:'bar',data:D.content_types.map(x=>x.avg_likes),itemStyle:{color:c.p},barWidth:'18%'},
      {name:'平均收藏',type:'bar',data:D.content_types.map(x=>x.avg_saves),itemStyle:{color:c.s},barWidth:'18%'},
      {name:'平均分享',type:'bar',data:D.content_types.map(x=>x.avg_shares),itemStyle:{color:c.w},barWidth:'18%'}
    ]});
  // 国家分布
  charts.countryChart.setOption({backgroundColor:'transparent',tooltip:{...tt,trigger:'item',formatter:'{b}: {c}%'},
    series:[{type:'pie',radius:['40%','70%'],center:['50%','45%'],data:D.audience.countries.map(x=>({value:x.percentage,name:x.country})),
      itemStyle:{borderRadius:6,borderColor:'var(--card)',borderWidth:2},label:{fontSize:11,formatter:'{b}\\n{c}%',color:c.sec},
      color:['#e1306c','#c13584','#833ab4','#5856d6','#3182ce','#38a169','#dd6b20','#718096']}]});
  // 年龄分布
  charts.ageChart.setOption({backgroundColor:'transparent',tooltip:{...tt,trigger:'axis',axisPointer:{type:'shadow'}},
    grid:{left:50,right:20,top:20,bottom:30,containLabel:true},
    xAxis:{type:'category',data:D.audience.age_groups.map(x=>x.group),axisLabel:{color:c.sec}},
    yAxis:{type:'value',name:'%',axisLabel:{fontSize:11,color:c.sec},splitLine:{lineStyle:{color:c.grid}}},
    series:[{type:'bar',data:D.audience.age_groups.map(x=>x.percentage),itemStyle:{color:{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:c.p2},{offset:1,color:c.p3}]},borderRadius:[6,6,0,0]},label:{show:true,position:'top',fontSize:11,color:c.sec,formatter:'{c}%'},barWidth:'50%'}]});
  // 活跃时间
  charts.hourChart.setOption({backgroundColor:'transparent',tooltip:{...tt,trigger:'axis'},
    grid:{left:50,right:20,top:20,bottom:30,containLabel:true},
    xAxis:{type:'category',data:D.audience.active_hours.map(x=>x.hour.replace(':00','')),axisLabel:{fontSize:10,color:c.sec,rotate:45}},
    yAxis:{type:'value',name:'活跃度',axisLabel:{fontSize:11,color:c.sec},splitLine:{lineStyle:{color:c.grid}}},
    series:[{type:'line',data:D.audience.active_hours.map(x=>x.activity),smooth:true,symbol:'none',lineStyle:{color:c.p,width:2},areaStyle:{color:'rgba(225,48,108,0.12)'},
      markPoint:{data:[{type:'max',name:'峰值'}],label:{fontSize:10}}}]});
  // 每日互动
  charts.engagementChart.setOption({backgroundColor:'transparent',tooltip:{...tt,trigger:'axis'},legend:{data:['点赞','评论','收藏','分享'],top:0,textStyle:{fontSize:11,color:c.sec}},
    grid:{left:60,right:20,top:30,bottom:40,containLabel:true},
    xAxis:{type:'category',data:D.daily_engagement.map(x=>x.date),axisLabel:{fontSize:10,color:c.sec,rotate:45},axisLine:{lineStyle:{color:c.grid}}},
    yAxis:{type:'value',axisLabel:{fontSize:11,color:c.sec},splitLine:{lineStyle:{color:c.grid}}},
    series:[
      {name:'点赞',type:'line',data:D.daily_engagement.map(x=>x.likes),smooth:true,symbol:'none',lineStyle:{color:c.p,width:1.5},stack:'a',areaStyle:{color:'rgba(225,48,108,0.3)'}},
      {name:'评论',type:'line',data:D.daily_engagement.map(x=>x.comments),smooth:true,symbol:'none',lineStyle:{color:c.i,width:1.5},stack:'a',areaStyle:{color:'rgba(49,130,206,0.3)'}},
      {name:'收藏',type:'line',data:D.daily_engagement.map(x=>x.saves),smooth:true,symbol:'none',lineStyle:{color:c.s,width:1.5},stack:'a',areaStyle:{color:'rgba(56,161,105,0.3)'}},
      {name:'分享',type:'line',data:D.daily_engagement.map(x=>x.shares),smooth:true,symbol:'none',lineStyle:{color:c.w,width:1.5},stack:'a',areaStyle:{color:'rgba(221,107,32,0.3)'}}
    ]});
  // 散点图
  const reelData=D.posts_scatter.filter(x=>x.type==='Reel'),carData=D.posts_scatter.filter(x=>x.type==='Carousel'),statData=D.posts_scatter.filter(x=>x.type==='Static');
  charts.scatterChart.setOption({backgroundColor:'transparent',tooltip:{...tt,trigger:'item',formatter:function(p){return p.data[3]+'<br/>'+p.data[2]+'<br/>互动率: '+p.data[1]+'%<br/>点赞: '+p.data[0]}},
    legend:{data:['Reel','Carousel','Static'],top:0,textStyle:{fontSize:11,color:c.sec}},
    grid:{left:60,right:20,top:30,bottom:40,containLabel:true},
    xAxis:{type:'value',name:'点赞数',axisLabel:{fontSize:11,color:c.sec},splitLine:{lineStyle:{color:c.grid}}},
    yAxis:{type:'value',name:'互动率(%)',axisLabel:{fontSize:11,color:c.sec},splitLine:{lineStyle:{color:c.grid}}},
    series:[
      {name:'Reel',type:'scatter',data:reelData.map(x=>[x.likes,x.er,x.type,x.topic]),itemStyle:{color:c.p},symbolSize:function(d){return Math.sqrt(d[0])/3+6}},
      {name:'Carousel',type:'scatter',data:carData.map(x=>[x.likes,x.er,x.type,x.topic]),itemStyle:{color:c.p3},symbolSize:function(d){return Math.sqrt(d[0])/3+6}},
      {name:'Static',type:'scatter',data:statData.map(x=>[x.likes,x.er,x.type,x.topic]),itemStyle:{color:c.i},symbolSize:function(d){return Math.sqrt(d[0])/3+6}}
    ]});
}
if(typeof echarts==='undefined'){document.body.innerHTML='<div style="padding:60px;text-align:center;color:#666">⚠️ 图表库加载失败，请检查网络后刷新。</div>'}
else{init();renderKPI();renderInsights();renderTable();update();window.addEventListener('resize',()=>Object.values(charts).forEach(c=>c&&c.resize()))}
</script>
</body></html>'''

html_path = os.path.join(base_dir, 'dashboard', 'index.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"看板已生成: {html_path}")
print(f"文件大小: {os.path.getsize(html_path)/1024:.1f} KB")
print(f"数据点数: 粉丝增长{len(dashboard_data['follower_growth'])}天, 帖子{len(dashboard_data['posts_scatter'])}条")
