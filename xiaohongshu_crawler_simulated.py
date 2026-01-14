import json
import random

def generate_simulated_items(count=50):
    """
    生成模拟的小红书女装内容数据
    :param count: 生成数量
    :return: 模拟数据列表
    """
    titles = [
        "秋季必备温柔风针织衫，显瘦又高级",
        "百搭牛仔裤分享，显瘦显高神器",
        "小个子女生穿搭指南，秒变165",
        "法式复古连衣裙，温柔到骨子里",
        "秋冬外套合集，保暖又时髦",
        "平价替代大牌，质感不输专柜",
        "职场穿搭必备，专业又时尚",
        "约会穿搭小心机，让他眼前一亮",
        "减龄学院风，重返18岁",
        "微胖女生穿搭，遮肉显瘦技巧"
    ]
    
    authors = [
        "穿搭博主小C",
        "时尚达人Lily",
        "造型师Mike",
        "服装设计师Anna",
        "时尚编辑Sarah",
        "穿搭顾问Tom",
        "风格博主Emma",
        "时尚买手Kevin",
        "造型师Lisa",
        "穿搭达人David"
    ]
    
    items = []
    
    for i in range(count):
        likes = random.randint(100, 10000)
        comments = random.randint(10, 5000)
        collections = random.randint(50, 8000)
        
        item = {
            "id": f"note_{random.randint(1000000, 9999999)}",
            "title": random.choice(titles),
            "desc": f"这款女装真的太好看了！面料舒适，版型显瘦，适合各种场合穿着。强烈推荐给大家，入手不亏！",
            "likes": likes,
            "comments": comments,
            "collections": collections,
            "author": random.choice(authors),
            "avatar": f"https://example.com/avatar_{random.randint(1, 10)}.jpg",
            "cover": f"https://example.com/cover_{random.randint(1, 20)}.jpg",
            "url": f"https://www.xiaohongshu.com/explore/note_{random.randint(1000000, 9999999)}"
        }
        items.append(item)
    
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
    print("开始生成小红书女装爆款模拟数据...")
    
    # 生成模拟数据
    items = generate_simulated_items(count=100)
    
    if items:
        print(f"\n共生成 {len(items)} 条模拟内容")
        
        # 获取热度最高的前10个
        top_items = get_top_items(items, top_n=10)
        
        print("\n🔥 小红书女装十大爆款 🔥")
        print(format_output(top_items))
        
        # 保存结果到文件
        with open("xiaohongshu_top10.json", "w", encoding="utf-8") as f:
            json.dump(top_items, f, ensure_ascii=False, indent=2)
        print("\n结果已保存到 xiaohongshu_top10.json 文件")
    else:
        print("未生成任何内容")
