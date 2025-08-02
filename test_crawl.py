import requests

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

params = {
    'page': '1',
    'limit': '10',
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

response = requests.get('https://haokaapi.lot-ml.com/api/Products/Query', params=params, headers=headers)


