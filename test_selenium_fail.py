from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


# 配置 Chrome 选项，指定用户数据目录
options = Options()
# 替换为你的“个人资料路径”（注意：路径要写到“User Data”级别，而非“Default”）
options.add_argument(r"user-data-dir=C:\Users\97994.DESKTOP-61VTV3A\AppData\Local\Google\Chrome\User Data")

# 2. 添加必要的启动参数，解决崩溃问题
options.add_argument("--no-sandbox")  # 禁用沙箱（关键参数，解决多数启动失败问题）
options.add_argument("--disable-dev-shm-usage")  # 禁用共享内存限制
options.add_argument("--start-maximized")  # 最大化窗口启动
options.add_argument("--disable-gpu")  # 禁用GPU加速（部分系统需要）

# 启动浏览器时加载该用户数据
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # 1. 访问表格所在的页面（会自动处理登录态，若未登录可先模拟登录）
    driver.get("https://haoka.lot-ml.com/view/iframe.html")  # 替换为目标页面 URL

    # （可选）若需要登录，可先模拟输入账号密码
    # driver.find_element(By.ID, "username").send_keys("your_username")
    # driver.find_element(By.ID, "password").send_keys("your_password")
    # driver.find_element(By.ID, "login-btn").click()
    # time.sleep(2)  # 等待登录完成

    # 2. 等待表格数据加载完成（根据 Layui 表格的特征定位）
    # Layui 表格的 tbody 通常有 class="layui-table-body" 或包含 layui 前缀
    wait = WebDriverWait(driver, 10)  # 最长等待 10 秒
    input("按回车键关闭浏览器...")  # 等待用户输入，避免脚本立即结束
except Exception as e:
    print("出错了：", str(e))

finally:
    # 关闭浏览器（调试时可注释此行，保留浏览器窗口观察）
    # driver.quit()
    pass