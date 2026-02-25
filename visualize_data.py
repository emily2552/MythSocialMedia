import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_scrape.video_id_crawl import BilibiliSearchScraper

# ======= 【1. 替换你爬取的真实数据】 =======
blibili_sracper = BilibiliSearchScraper("哪吒")
video_ids = blibili_sracper.crawl_bvids()
video_infos = blibili_sracper.crawl_video_infos(video_ids)

# ======= 【2. 数据清洗与格式化】 =======
df = pd.DataFrame(video_infos)


numeric_cols = ['view', 'like', 'danmaku', 'favorite', 'coin', 'share', 'reply', 'up_fans', 'total_duration']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# 支持中文字体显示（防止图表里的中文变成小方块）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ======= 【3. 开始画图】 =======
fig = plt.figure(figsize=(16, 12))

# 【图 1】：播放量排名前10的视频
ax1 = plt.subplot(2, 2, 1)
# 取播放量前10，升序排列以便在水平条形图中由高到低显示
top_10 = df.nlargest(10, 'view').sort_values(by='view', ascending=True)
ax1.barh(top_10['video_id'], top_10['view'], color='cornflowerblue')
ax1.set_title('播放量(view)排名前10的视频', fontsize=14)
ax1.set_xlabel('播放量')
ax1.set_ylabel('视频ID (video_id)')

# 【图 2】：UP主粉丝数 vs 播放量 (散点气泡图)
ax2 = plt.subplot(2, 2, 2)
sns.scatterplot(x='up_fans', y='view', size='like', data=df, ax=ax2, sizes=(20, 500), alpha=0.6, color='coral')
ax2.set_title('UP主粉丝数 vs 播放量\n(气泡大小代表点赞数)', fontsize=14)
ax2.set_xlabel('UP主粉丝数 (up_fans)')
ax2.set_ylabel('播放量 (view)')
ax2.legend([],[], frameon=False) # 隐藏图例

# 【图 3】：视频播放量分布直方图
ax3 = plt.subplot(2, 2, 3)
sns.histplot(df['view'], bins=20, kde=True, color='mediumseagreen', ax=ax3)
ax3.set_title('视频播放量(view)区间分布', fontsize=14)
ax3.set_xlabel('播放量')
ax3.set_ylabel('视频数量')

# 【图 4】：B站核心互动指标相关性分析热力图
ax4 = plt.subplot(2, 2, 4)
# 只取核心互动指标做相关性计算
interaction_metrics = ['view', 'like', 'coin', 'favorite', 'share', 'danmaku', 'reply']
available_metrics = [m for m in interaction_metrics if m in df.columns]

if len(available_metrics) > 1:
    corr = df[available_metrics].corr()
    sns.heatmap(corr, annot=True, cmap='Blues', ax=ax4, fmt=".2f")
    ax4.set_title('B站核心互动指标相关性分析', fontsize=14)

plt.tight_layout()

# ======= 【4. 保存并展示】 =======
plt.savefig('bilibili_analysis.png', dpi=300)
plt.show()
print("🎉 图表已生成，并保存为 bilibili_analysis.png")