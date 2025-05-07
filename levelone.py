import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def analyze_daily_first_level_comments():
    """
    统计每日一级评论数并绘制条形图（直接指定文件路径）
    """
    # 直接在此处指定文件路径 ↓
    input_csv = ".csv"
    
    try:
        # 1. 检查文件是否存在
        if not os.path.exists(input_csv):
            raise FileNotFoundError(f"文件不存在: {input_csv}")

        # 2. 读取数据
        df = pd.read_csv(input_csv, encoding='utf-8-sig')
        
        # 3. 筛选一级评论（兼容不同表述）
        first_level = df[df['评论层级'].str.contains('1级|一级|主评论', na=False)].copy()
        
        if first_level.empty:
            print("文件中没有找到一级评论！")
            return
        
        # 4. 转换日期格式并提取日期
        first_level['日期'] = pd.to_datetime(first_level['回复时间']).dt.date
        
        # 5. 按日期统计评论数
        daily_counts = first_level['日期'].value_counts().sort_index()
        
        # 6. 准备绘图数据
        dates = [d.strftime('%Y-%m-%d') for d in daily_counts.index]
        counts = daily_counts.values
        
        # 7. 创建条形图
        plt.figure(figsize=(14, 7))
        bars = plt.bar(dates, counts, color=plt.cm.viridis(range(len(dates))))
        
        # 8. 添加图表元素
        plt.title(f' Daily first-level comment statistics', fontsize=16, pad=20)
        plt.xlabel('data', fontsize=12)
        plt.ylabel('Number of reviews', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        
        # 9. 添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height)}',
                     ha='center', va='bottom', fontsize=8)
        
        # 10. 保存图表
        output_file = input_csv.replace('.csv', '_每日评论统计.png')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        

    except Exception as e:
        print(f"\n处理过程中出错: {str(e)}")

if __name__ == "__main__":
    analyze_daily_first_level_comments()
