from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 创建一个 Options 对象
chrome_options = Options()

# 指定 Chrome 浏览器的二进制文件路径
chrome_options.binary_location = "D:\Downloads\Win_911514_chrome-win\chrome-win\chrome.exe"
# 初始化浏览器为chrome浏览器
# 指定绝对路径的方式（可选）
path = "D:\environment\conda\spider\chromedriver.exe"
browser = webdriver.Chrome(path)
# 关闭浏览器
browser.close()
