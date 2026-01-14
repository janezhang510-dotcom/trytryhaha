import requests
import json
import time
import random
from bs4 import BeautifulSoup

def get_headers():
    """生成随机请求头，模拟浏览器行为"""
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.xiaohongshu.com/",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Cookie": "abRequestId=3a4b5c6d-7e8f-9g0h-1i2j-3k4l5m6n7o8p; xsecappid=xhs-pc-web; a1=198bcf8b560h4w8qfkxj57mnp00w8z33s4f00vxr375000315941; webId=9f8e7d6c5b4a3s2d1f0g; gsid=1234567890abcdefghijklmnopqrstuvwxyz; webBuild=4.8.0; xhsTrackerId=12345678-90ab-cdef-ghij-klmnopqrstuv; sec_poison_id=abcdefghijklmnopqrstuvwxyz123456"
    }

def crawl_xiaohongshu(keyword, max_pages=5):
    """
    抓取小红书相关内容
    :param keyword: 搜索关键词
    :param max_pages: 最大抓取页数
    :return: 抓取的内容列表
    """
    items = []
    # 尝试使用不同的API端点
    base_urls = [
        "https://www.xiaohongshu.com/api/sns/v3/search/notes",
        "https://api.xiaohongshu.com/api/sns/v3/search/notes"
    ]
    
    for base_url in base_urls:
        print(f"尝试使用API端点: {base_url}")
        
        for page in range(1, max_pages + 1):
            params = {
                "keyword": keyword,
                "page": page,
                "page_size": 20,
                "sort": "popular"  # 按热度排序
            }
            
            try:
                headers = get_headers()
                # 添加随机延迟，避免被识别为爬虫
                time.sleep(random.uniform(1, 3))
                
                response = requests.get(base_url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    notes = data.get("data", {}).get("notes", [])
                    
                    if notes:
                        for note in notes:
                            item = {
                                "id": note.get("id"),
                                "title": note.get("title"),
                                "desc": note.get("desc"),
                                "likes": note.get("likes"),
                                "comments": note.get("comments"),
                                "collections": note.get("collections"),
                                "author": note.get("user", {}).get("nickname"),
                                "avatar": note.get("user", {}).get("avatar"),
                                "cover": note.get("image_list", [{}])[0].get("url", ""),
                                "url": f"https://www.xiaohongshu.com/explore/{note.get('id')}"
                            }
                            items.append(item)
                        
                        print(f"第 {page} 页抓取完成，获取 {len(notes)} 条内容")
                    else:
                        print(f"第 {page} 页无内容，可能需要登录")
                else:
                    print(f"第 {page} 页抓取失败，状态码: {response.status_code}")
                    # 打印响应内容，以便分析
                    if response.text:
                        print(f"响应内容: {response.text[:200]}...")
            
            except Exception as e:
                print(f"抓取第 {page} 页时出错: {str(e)}")
                time.sleep(5)
        
        # 如果已经获取到内容，停止尝试其他API端点
        if items:
            break
    
    return items

def calculate_hot_score(item):
    """
    计算热度分数
    :param item: 内容项
    :return: 热度分数
    """
    likes = item.get("likes", 0)
    comments = item.get("comments", 0)
    collections = item.get("collections", 0)
    
    # 权重分配：收藏 > 点赞 > 评论
    score = likes * 1 + comments * 2 + collections * 3
    return score

def get_top_items(items, top_n=10):
    """
    获取热度最高的前N个内容
    :param items: 内容列表
    :param top_n: 数量
    :return: 排序后的内容列表
    """
    items_with_score = []
    for item in items:
        item["hot_score"] = calculate_hot_score(item)
        items_with_score.append(item)
    
    # 按热度分数排序
    sorted_items = sorted(items_with_score, key=lambda x: x["hot_score"], reverse=True)
    return sorted_items[:top_n]

def format_output(items):
    """
    格式化输出结果
    :param items: 内容列表
    :return: 格式化的字符串
    """
    output = []
    for i, item in enumerate(items, 1):
        output.append(f"第 {i} 名:")
        output.append(f"标题: {item.get('title', '无标题')}")
        output.append(f"描述: {item.get('desc', '无描述')[:100]}...")
        output.append(f"热度分数: {item.get('hot_score')}")
        output.append(f"点赞: {item.get('likes', 0)}")
        output.append(f"评论: {item.get('comments', 0)}")
        output.append(f"收藏: {item.get('collections', 0)}")
        output.append(f"作者: {item.get('author', '未知')}")
        output.append(f"链接: {item.get('url')}")
        output.append("-" * 50)
    
    return "\n".join(output)

if __name__ == "__main__":
    print("开始抓取小红书女装爆款内容...")
    
    # 抓取女装相关内容
    items = crawl_xiaohongshu("女装", max_pages=10)
    
    if items:
        print(f"\n共抓取到 {len(items)} 条内容")
        
        # 获取热度最高的前10个
        top_items = get_top_items(items, top_n=10)
        
        print("\n🔥 小红书女装十大爆款 🔥")
        print(format_output(top_items))
        
        # 保存结果到文件
        with open("xiaohongshu_top10.json", "w", encoding="utf-8") as f:
            json.dump(top_items, f, ensure_ascii=False, indent=2)
        print("\n结果已保存到 xiaohongshu_top10.json 文件")
    else:
        print("未抓取到任何内容，请检查网络或请求参数")
