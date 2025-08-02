import requests
import csv
import re
from collections import defaultdict

# 定义请求头
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbXBJZCI6IjAiLCJFbXBSb2xlIjoiIiwiQWdlbnRJRCI6IjQ4MDE5OCIsImxvZ2luTmFtZSI6IuWkj-ebiuWbvSIsIlVzZXJOYW1lIjoi5rWB6YeP55yf55qE5Li6546LIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiNDgwMTk4IiwibmJmIjoxNzU0MTI3MDY0LCJleHAiOjE3NTQ3MzE4NjQsImlzcyI6IlpTU29mdC5EYVRpZS5BcGkiLCJhdWQiOiJaU1NvZnQuRGFUaWUuQXBpIn0.B4ML50f_M5W6kwK1ajo2B8JFnXFMtNRFSL5G7vMhD1w',
    'cache-control': 'no-cache',
    'origin': 'https://haoka.lot-ml.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://haoka.lot-ml.com/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

# 存储所有爬取到的数据
all_data = []

# 定义初始页码
page = 1
# 每页数据量
limit = 10

print("开始爬取数据...")

try:
    while True:
        # 设置当前页参数
        params = {
            'page': str(page),
            'limit': str(limit),
            'ProductName': '',
            'CommissionType': '',
            'Operator': '',
            'Area': '',
            'BackMoneyType': '',
            'Age1': '0',
            'Age2': '100',
            'NumberType': '',
            'PackageType': '',
            'SecSupplier': '',
            'PriceTime': '',
            'SendAddr': '',
            'Name1': '',
            'OnShop': 'true',
            'IsKuan': '',
        }
        
        # 发送请求
        response = requests.get(
            'https://haokaapi.lot-ml.com/api/Products/Query',
            params=params,
            headers=headers
        )
        
        # 解析JSON响应
        result = response.json()
        
        # 检查响应状态
        if result.get('code') != 0:
            print(f"第{page}页请求失败: {result.get('msg', '未知错误')}")
            break
        
        # 获取当前页数据
        current_data = result.get('data', [])
        
        # 如果当前页没有数据，停止爬取
        if not current_data:
            print(f"第{page}页没有数据，爬取结束")
            break
        
        # 保存当前页需要的字段
        for item in current_data:
            all_data.append({
                'productID': "https://h5.lot-ml.com/PackInfo/Detail/"+str(item.get('productID')),
                'productName': item.get('productName')
            })
        
        print(f"已爬取第{page}页，累计获取{len(all_data)}条数据")
        
        # 准备爬取下一页
        page += 1

except Exception as e:
    print(f"爬取过程中发生错误: {str(e)}")

# 对数据进行排序：按照productName中"元"前面的数字从小到大排列
def extract_price(name):
    """从产品名称中提取"元"前面的数字"""
    match = re.search(r'(\d+(\.\d+)?)元', name)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return float('inf')  # 无法转换的放在最后
    return float('inf')  # 没有找到价格的放在最后

# 排序数据
sorted_data = sorted(all_data, key=lambda x: extract_price(x['productName']))

# 保存到CSV文件
if sorted_data:
    try:
        with open('product_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['productID', 'productName']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in sorted_data:
                writer.writerow(item)
        
        print(f"数据已成功保存到product_info.csv，共{len(sorted_data)}条记录")
    except Exception as e:
        print(f"保存CSV文件失败: {str(e)}")
else:
    print("没有获取到任何数据，不生成CSV文件")
