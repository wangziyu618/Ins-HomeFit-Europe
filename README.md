# @homefit.europe — Instagram模拟运营项目 📱

> 90天欧洲居家健身Instagram账号运营复盘 | 内容策略 + 数据分析 + 可视化看板
>
> 个人海外社媒运营作品集

---

## 🎯 项目目标

从零运营一个面向欧洲上班族的居家健身Instagram账号（@homefit.europe），完整执行**账号定位→内容策略→90天发布→数据复盘→优化建议**的社媒运营全流程，验证"无器械+15分钟+上班族"细分定位的增长潜力。

---

## 📖 快速预览

| 文件 | 说明 | 链接 |
|------|------|------|
| 🖥️ **运营数据看板** | 交互式看板：粉丝增长/内容表现/受众画像/Top帖子 | [在线体验](https://wdnmdlgb.github.io/Ins-HomeFit-Europe/dashboard/) |
| 📋 运营复盘报告 | 90天完整复盘：策略执行+数据分析+优化建议 | [查看报告](https://github.com/wdnmdlgb/Ins-HomeFit-Europe/blob/master/report/运营复盘报告.md) |
| 📝 账号定位策略 | 定位/目标/内容支柱/发布节奏/增长策略 | [查看策略](https://github.com/wdnmdlgb/Ins-HomeFit-Europe/blob/master/strategy/账号定位与运营策略.md) |
| ✍️ 帖子文案库 | Reels/Carousel/Stories完整英文文案+标签 | [查看文案](https://github.com/wdnmdlgb/Ins-HomeFit-Europe/blob/master/content/帖子文案库.md) |

---

## 📊 90天运营成果

| 指标 | 目标 | 实际 |
|------|------|------|
| 粉丝数 | 5,000 | **4,253** |
| 平均互动率 | 4%+ | **6.61%** （高于行业3-6%基准） |
| 发布帖子 | 70+ | **83** （51 Reels + 26 Carousels + 6 Static） |
| 总点赞 | — | **33.4K** |
| 总收藏 | — | **5.8K** |
| 总触达 | — | **85万+** |
| Stories日更 | 80%+ | **100%** |

---

## 🛠️ 技术栈

| 工具 | 用途 |
|------|------|
| **Python Pandas** | 90天运营数据生成与统计分析 |
| **ECharts** | 交互式数据看板（7个图表，深色模式） |
| **CSV/JSON** | 结构化数据存储 |
| **GitHub Pages** | 看板在线部署 |

---

## 📁 仓库结构

```
Ins-HomeFit-Europe/
├── README.md
├── .gitignore
├── strategy/
│   └── 账号定位与运营策略.md        # 定位、目标、内容支柱、增长策略
├── content/
│   ├── content_calendar.csv        # 90天内容日历（167条发布记录）
│   └── 帖子文案库.md               # Reels/Carousel/Stories完整文案
├── data/
│   ├── daily_metrics.csv           # 90天每日运营数据
│   ├── posts_performance.csv       # 83条帖子明细数据
│   ├── audience_insights.json      # 受众画像（国家/年龄/性别/活跃时间）
│   ├── content_type_summary.json   # 内容类型表现汇总
│   ├── top_posts.json              # Top 10最佳帖子
│   └── insights.json               # 关键运营洞察
├── dashboard/
│   ├── index.html                  # 🖥️ 交互式运营数据看板
│   └── dashboard_data.json         # 看板聚合数据
├── report/
│   └── 运营复盘报告.md              # 90天完整复盘报告
└── scripts/
    ├── generate_data.py            # 运营数据生成脚本
    ├── generate_calendar.py        # 内容日历生成脚本
    └── generate_dashboard.py       # 看板HTML生成脚本
```

---

## 📈 看板包含的7个图表

1. **粉丝增长趋势** — 90天粉丝曲线 + 每日新增柱状图（双轴）
2. **内容类型对比** — Reels/Carousel/Static的点赞/收藏/分享对比
3. **受众国家分布** — 欧洲8国受众占比饼图
4. **受众年龄分布** — 5个年龄段柱状图
5. **受众活跃时间** — 18个时段活跃度曲线（CET时区）
6. **每日互动趋势** — 点赞/评论/收藏/分享堆叠面积图
7. **帖子互动率散点图** — 按类型区分，气泡大小反映点赞数

---

## 💡 关键发现

1. **Carousel互动率最高（8.49%）**，收藏占比大，教学类内容长尾价值强
2. **Reels是增长引擎**，贡献80%+新粉丝触达，算法推荐带来非粉丝流量
3. **Static帖子ROI最低**，互动率仅2-3%，建议削减
4. **20:00是流量高峰**（活跃度95%），应增加晚间Reels发布
5. **德国+英国占受众52%**，为核心市场；荷兰用户互动率最高
6. **爆款效应显著**，6%的帖子带来单日200+新增粉丝

---

## 🚀 如何复现

```bash
# 1. 生成运营数据
python scripts/generate_data.py

# 2. 生成内容日历
python scripts/generate_calendar.py

# 3. 生成看板HTML
python scripts/generate_dashboard.py

# 4. 浏览器打开 dashboard/index.html
```

---

## ⚠️ 数据说明

本项目为**模拟运营项目**，数据基于Instagram健身行业公开基准数据生成（健身微型博主互动率3-6%、Reels播放量为粉丝数2-8倍、Carousel收藏率高等），用于展示海外社媒运营的策略制定、内容规划和数据分析能力。文案为原创英文内容，可直接用于实际账号运营。

---

