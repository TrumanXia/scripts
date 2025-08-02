import requests
import csv
import re
from bs4 import BeautifulSoup

#流量卡后台网站数据爬取
# 请求头配置（保持与浏览器请求一致，避免被拦截）
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

# 存储所有产品数据的列表
all_products = []

def parse_max_age(age_str):
    """解析办卡年龄字符串，返回最大年龄值"""
    # 处理空值或特殊情况
    if not age_str or age_str.strip() in ['无', '未知', '提取失败']:
        return None
    
    # 清除无关字符
    cleaned = re.sub(r'[^\d-]', '', age_str)
    
    # 匹配年龄范围格式（如18-65、18-60）
    match = re.search(r'(\d+)-(\d+)', cleaned)
    if match:
        return int(match.group(2))  # 返回范围中的最大值
    
    # 匹配单个年龄值（如60）
    single_match = re.search(r'(\d+)', cleaned)
    if single_match:
        return int(single_match.group(1))
    
    # 无法解析的情况
    return None

def extract_detail_fields(product_id):
    """提取详情页的四个目标字段"""
    detail_url = f'https://h5.lot-ml.com/PackInfo/Detail/{product_id}'
    try:
        # 发送详情页请求
        response = requests.get(detail_url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析页面文本
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().replace('\r', '').replace('\t', '')  # 清理文本格式
        
        # 1. 提取办卡年龄
        age_pattern = re.compile(r'办卡年龄(.*?)(?=合约期|不发货地区|快递方式|$)', re.DOTALL)
        age_match = age_pattern.search(page_text)
        age = age_match.group(1).strip() if age_match else '未知'
        
        # 2. 提取合约期
        contract_pattern = re.compile(r'合约期(.*?)(?=不发货地区|办卡年龄|快递方式|$)', re.DOTALL)
        contract_match = contract_pattern.search(page_text)
        contract = contract_match.group(1).strip() if contract_match else '未知'
        
        # 3. 提取不发货地区
        area_pattern = re.compile(r'不发货地区(.*?)(?=定向范围|合约期|快递方式|$)', re.DOTALL)
        area_match = area_pattern.search(page_text)
        no_delivery_area = area_match.group(1).strip() if area_match else '无限制'
        
        # 4. 提取优惠详情
        discount_pattern = re.compile(r'优惠详情(.*?)(?=快递方式|激活方式|办卡年龄|$)', re.DOTALL)
        discount_match = discount_pattern.search(page_text)
        discount = discount_match.group(1).strip().replace('\n', ' ') if discount_match else '无'
        
        return {
            '办卡年龄': age,
            '合约期': contract,
            '不发货地区': no_delivery_area,
            '优惠详情': discount
        }
    
    except Exception as e:
        print(f"产品ID {product_id} 详情提取失败: {str(e)}")
        return {
            '办卡年龄': '提取失败',
            '合约期': '提取失败',
            '不发货地区': '提取失败',
            '优惠详情': '提取失败'
        }

def extract_price_from_name(name):
    """从产品名称中提取"元"前面的数字，用于排序"""
    price_pattern = re.compile(r'(\d+(\.\d+)?)元')
    match = price_pattern.search(name)
    return float(match.group(1)) if match else float('inf')

# 主爬取逻辑
def main():
    page = 1
    limit = 10
    print("开始爬取产品数据...")
    
    try:
        while True:
            # 构建列表页请求参数
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
            
            # 请求产品列表页
            list_response = requests.get(
                'https://haokaapi.lot-ml.com/api/Products/Query',
                params=params,
                headers=headers,
                timeout=10
            )
            list_data = list_response.json()
            
            # 检查列表请求是否成功
            if list_data.get('code') != 0:
                print(f"第{page}页列表请求失败: {list_data.get('msg', '未知错误')}")
                break
            
            current_products = list_data.get('data', [])
            if not current_products:
                print(f"第{page}页无数据，爬取结束")
                break
            
            # 处理当前页产品
            for item in current_products:
                product_id = item.get('productID')
                product_name = item.get('productName', '未知名称')
                print(f"处理产品: {product_id} - {product_name}")
                
                # 获取详情页字段
                detail_fields = extract_detail_fields(product_id)
                
                # 解析最大年龄并过滤
                max_age = parse_max_age(detail_fields['办卡年龄'])
                if max_age is not None and max_age < 33:
                    print(f"  过滤：最大年龄{max_age}小于33岁，不保存")
                    continue

                # 整合数据
                all_products.append({
                    'productID': "https://h5.lot-ml.com/PackInfo/Detail/"+str(product_id),
                    'productName': product_name,
                    **detail_fields
                })
            
            print(f"第{page}页处理完成，累计数据: {len(all_products)}条")
            page += 1
    
    except Exception as e:
        print(f"爬取过程出错: {str(e)}")
    
    # 按价格排序
    sorted_products = sorted(all_products, key=lambda x: extract_price_from_name(x['productName']))
    
    # 保存到CSV
    if sorted_products:
        try:
            with open('产品详细信息2.csv', 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['productID', 'productName', '办卡年龄', '合约期', '不发货地区', '优惠详情']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(sorted_products)
            print(f"数据已成功保存到'产品详细信息.csv'，共{len(sorted_products)}条记录")
        except Exception as e:
            print(f"保存CSV失败: {str(e)}")
    else:
        print("未获取到任何产品数据，不生成CSV文件")

if __name__ == "__main__":
    main()