import requests
import time
import csv
import os
from typing import List, Dict

headers = {
    'User-Agent': ''
}

def fetch_replies(comment, video_id, root_uname: str = "", depth: int = 1) -> List[Dict]:
    """递归获取评论回复"""
    replies = []
    if 'replies' in comment and comment['replies']:
        for reply in comment['replies']:
            reply_info = {
                '用户昵称': reply['member']['uname'],
                '评论内容': reply['content']['message'],
                '被回复用户': root_uname if depth == 1 else comment['member']['uname'],
                '评论层级': f'{depth+1}级评论',
                '性别': reply['member']['sex'],
                '用户当前等级': reply['member']['level_info']['current_level'],
                '点赞数量': reply['like'],
                '回复时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reply['ctime']))
            }
            replies.append(reply_info)
            # 递归获取更深层的回复
            replies.extend(fetch_replies(reply, video_id, root_uname, depth+1))
    return replies

def fetch_comments(video_id, max_pages=1000) -> List[Dict]:
    """获取视频评论（包含二级评论）"""
    comments = []
    next_page = 1  # 初始next值
    
    for _ in range(max_pages):
        url = f'https://api.bilibili.com/x/v2/reply/main?next={next_page}&type=1&oid={video_id}&mode=3'
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"正在爬取第 {next_page} 页")
                
                if not data.get('data') or not data['data'].get('replies'):
                    break
                    
                for comment in data['data']['replies']:
                    # 一级评论
                    comment_info = {
                        '用户昵称': comment['member']['uname'],
                        '评论内容': comment['content']['message'],
                        '被回复用户': '',
                        '评论层级': '1级评论',
                        '性别': comment['member']['sex'],
                        '用户当前等级': comment['member']['level_info']['current_level'],
                        '点赞数量': comment['like'],
                        '回复时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment['ctime']))
                    }
                    comments.append(comment_info)
                    
                    # 获取该评论下的回复（二级及更深评论）
                    replies = fetch_replies(comment, video_id, comment['member']['uname'])
                    comments.extend(replies)
                
                # 更新next_page值
                next_page = data['data'].get('cursor', {}).get('next', 0)
                if next_page == 0:
                    break
                    
            else:
                print(f"请求失败，状态码: {response.status_code}")
                break
                
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            break
            
        time.sleep(1)
        
    return comments

def save_comments_to_csv(comments, video_bv):
    """保存评论到CSV文件"""
    os.makedirs('./result', exist_ok=True)
    with open(f'./result/{video_bv}.csv', mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            '用户昵称', '性别', '评论内容', '被回复用户', 
            '评论层级', '用户当前等级', '点赞数量', '回复时间'
        ])
        writer.writeheader()
        writer.writerows(comments)



if __name__ == '__main__':
    video_name = '直升机到底安全吗'
    video_bv = 'BV1Ax4y1H74L'
    
    print(f'开始爬取视频: {video_name}({video_bv})')
    comments = fetch_comments(video_bv)
    save_comments_to_csv(comments, video_name)
    print(f'爬取完成，共获取{len(comments)}条评论')
