import pandas as pd
import matplotlib.pyplot as plt
import os

# 文件路径列表
csv_files = [

]

# 主要梗关键词（命中乘点赞数）
primary_keywords = []

# 次级梗关键词（命中加1分）
secondary_keywords = []

# 存储每个文件的梗词得分和总评论数
meme_scores = []
total_comments = []
file_labels = [os.path.splitext(os.path.basename(f))[0] for f in csv_files]

# 遍历每个文件处理
for file in csv_files:
    meme_score = 0
    comment_count = 0
    try:
        # 读取CSV
        df = pd.read_csv(file, encoding="utf-8-sig")
        df.columns = df.columns.str.strip().str.replace('\ufeff', '').str.replace('　', '').str.replace(' ', '')

        # 自动识别评论列和点赞列
        comment_col = next((col for col in df.columns if '评论内容' in col), None)
        like_col = next((col for col in df.columns if '赞' in col), None)

        if not comment_col or not like_col:
            print(f"❌ Missing required columns in {file}. Available: {df.columns.tolist()}")
            meme_scores.append(0)
            total_comments.append(1)  # 避免除以0
            continue

        df[comment_col] = df[comment_col].astype(str)
        df[like_col] = pd.to_numeric(df[like_col], errors='coerce').fillna(0).astype(int)

        # 计算总评论数
        comment_count = len(df)
        total_comments.append(comment_count)

        # 分析每条评论
        primary_match_count = 0
        secondary_match_count = 0
        for _, row in df.iterrows():
            content = row[comment_col]
            likes = row[like_col]
            
            # 检查主要关键词（得分加点赞数）
            if any(kw in content for kw in primary_keywords):
                if likes == 0:
                    likes = 1  # 点赞为0视为1
                meme_score += likes
                primary_match_count += 1
            
            # 检查次级关键词（得分加1）
            elif any(kw in content for kw in secondary_keywords):
                meme_score += 1
                secondary_match_count += 1

        print(f" {file}: matched {primary_match_count} primary and {secondary_match_count} secondary comments, raw score: {meme_score}, total comments: {comment_count}")
        meme_scores.append(meme_score)

    except Exception as e:
        print(f"❌ Error reading {file}: {e}")
        meme_scores.append(0)
        total_comments.append(1)  # 避免除以0

# 归一化处理（得分 / 总评论数）
normalized_scores = [score / comments if comments > 0 else 0 for score, comments in zip(meme_scores, total_comments)]

# 绘制条形图
plt.figure(figsize=(10, 6))
plt.bar(file_labels, normalized_scores, color="skyblue")
plt.title("Normalized Meme Influence Score (Score per Comment)", fontsize=16)
plt.ylabel("Meme Score per Comment", fontsize=12)
plt.xlabel("CSV File", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("normalized_meme_influence_analysis.png", dpi=300)
plt.show()
