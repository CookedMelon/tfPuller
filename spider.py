# pre标签内的直接省去

# 爬虫获取网页源代码

import requests
import logging
import yaml
import os
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 创建一个 Options 对象
# chrome_options = Options()
# chrome_options.add_argument('--ignore-ssl-errors=yes')
# chrome_options.add_argument('--ignore-certificate-errors')
# 指定 Chrome 浏览器的二进制文件路径
# chrome_options.binary_location = "D:\Downloads\Win_911514_chrome-win\chrome-win\chrome.exe"
# 初始化浏览器为chrome浏览器
# 指定绝对路径的方式（可选）
path = "D:\env\geckodriver.exe"
# path = "D:\environment\conda\spider\chromedriver.exe"
# driver = webdriver.Chrome(path)
# driver = webdriver.Chrome(service=Service(path), options=chrome_options)
driver = webdriver.Firefox(service=Service(path))
api_list=[]
def createyaml(dir_name,api,yaml_data):
    # Check if the directory exists
    if not os.path.exists(dir_name):
        # If not, create the directory
        os.makedirs(dir_name)
    # 生成yaml保存在本地
    with open(f'{dir_name}/{api}.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_data)
# print(api_list)
def load_api_list2(apis):
    global api_list
    for api in apis:
        url=api.replace('.','/')
        url='https://www.tensorflow.org/api_docs/python/'+url
        api_list.append({'api':api,'url':url})
def load_api_list(api_path):
    global api_list
    with open(api_path,'r') as f:
        for line in f.readlines():
            # 替换其中的.为/
            line=line.replace('.','/')
            line='https://www.tensorflow.org/api_docs/python/'+line
            api_list.append(line.strip())
# 去除所有的除字母下划线数字以外的字符
def remove_other_char(content):
    # 正则表达式，匹配除字母、数字和下划线以外的所有字符
    pattern = re.compile(r'[^a-zA-Z0-9_]')
    
    # 使用 sub 函数替换匹配到的字符为空字符串
    result_str = pattern.sub('', content)
    
    return result_str
# 去除元素中除最外层外的所有的标签只提取标签内的文字
def remove_tag(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()
def spider(url: str)->dict:
    print(url)
    error_message = ''
    api_dict = {}
    api_dict['url'] = url
    api_dict['warn_message']=[]    
    # 执行自动化操作
    driver.get(url)  # 打开网页
    time.sleep(0)  # 等待5秒
        # 通过class name找到父元素
    print("finish wait")

    # try:
    #     parent_element = WebDriverWait(driver,10).until(
    #         EC.presence_of_element_located((By.TAG_NAME, 'devsite-content'))
    #     )
    #     parent_element = driver.find_element(By.TAG_NAME, 'devsite-content')
    # except Exception as e:
    #     print(f"Error: {e}")
    parent_element = driver.find_element(By.TAG_NAME, 'devsite-content')
    # 在父元素内，通过class name找到所有的子元素
    table_elements = parent_element.find_elements(By.CLASS_NAME,'responsive')
    # print()
    print("tables len:",len(table_elements))
    # 遍历子元素列表并获取每个元素的内容
    for child in table_elements:
    # try:
        print('child:',child)
        trs=child.find_elements(By.TAG_NAME,'tr')
        if len(trs)==0:
            continue
        headtr=trs[0]
        bodytrs=trs[1:]
        headtxt=remove_tag(headtr.get_attribute('innerHTML'))
        print('headtxt:',headtxt)
        if headtxt=='Args':
            print('in args')
            if api_dict.get('args'):
                error_message='Multiple args'
                print(error_message)
                api_dict['error_message'] = error_message
                logging.error(error_message)
                return api_dict
            api_dict['args']={}
            # arg_desc=remove_tag(tds[1].get_attribute('innerHTML'))
            # print('arg_desc:',arg_desc)
            for bodytr in bodytrs:
                tds=bodytr.find_elements(By.TAG_NAME,'td')
                if len(tds)!=2:
                    error_message='tds len error.[Args need 2 tds]'
                    print(error_message)
                    api_dict['error_message'] = error_message
                    logging.error(error_message)
                    return api_dict
                arg_name=remove_other_char(remove_tag(tds[0].get_attribute('innerHTML')))
                print('arg_name:',arg_name)
                arg_desc=remove_tag(tds[1].get_attribute('innerHTML')).replace('\n','')
                print('arg_desc:',arg_desc)
                # arg_name和arg_desc长度过长触发warn
                if len(arg_name)>100 or len(arg_desc)>200:
                    warn_message='arg_name or arg_desc too long'
                    api_dict['warn_message'].append(warn_message)
                    logging.warning(warn_message)
                api_dict['args'][arg_name]=arg_desc
        elif headtxt=='Returns':
            print('in Returns')
            if api_dict.get('returns'):
                error_message='Multiple Returns'
                api_dict['error_message'] = error_message
                logging.error(error_message)
                return api_dict
            api_dict['returns'] = {}
            # arg_desc=remove_tag(tds[1].get_attribute('innerHTML'))
            # print('arg_desc:',arg_desc)
            for bodytr in bodytrs:
                tds=bodytr.find_elements(By.TAG_NAME,'td')
                if len(tds)!=1:
                    error_message='tds len error.[Returns need 1 tds]'
                    api_dict['error_message'] = error_message
                    logging.error(error_message)
                    return api_dict
                ret_desc=remove_tag(tds[0].get_attribute('innerHTML')).replace('\n','')
                print('ret_desc:',ret_desc)
                # ret_desc长度过长触发warn
                if len(ret_desc)>200:
                    warn_message='ret_desc too long'
                    api_dict['warn_message'].append(warn_message)
                    logging.warning(warn_message)
                api_dict['returns']=ret_desc
        else :
            print('in else, do nothing')
    return api_dict
                    


    input()
    # 在这里执行你的网页操作

    # 最后关闭浏览器
    # driver.quit()

# 查找文件中是否有哪一行和文本相同
def find_line(file_path, text):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if text == line.strip():
                    return True
    except FileNotFoundError:
        pass  # 文件不存在，直接返回 False
    return False

def main():
    # api_path='/home/cc/Workspace/tfconstraint/tf_valid_apis.txt'
    apis=[]
    with open('apilist.txt','r') as f:
        apis=f.readlines()
    for i in range(len(apis)):
        apis[i]=apis[i].strip()
    load_api_list2(apis)
    for item in api_list:
        url=item['url']
        api=item['api']
        print('url',url)
        api_dict=spider(url)
        api_dict['name']=api
        print(api_dict)
        error_message = api_dict.get('error_message', None)
        warn_message = api_dict.get('warn_message', None)
        # if 'error_message' in api_dict:
        #     del api_dict['error_message']
        if warn_message==[]:
            del api_dict['warn_message']
        
        yaml_data = yaml.dump(api_dict, default_flow_style=False, allow_unicode=True)

        if error_message!=None:
            logging.error('get error',error_message)
            # 生成yaml保存在本地
            createyaml("apis_error",api,yaml_data)
            # 向api2文件追加api
            if not find_line('api3.txt', api):
                with open('api3.txt', 'a+', encoding='utf-8') as f:
                    f.write(api+'\n')
            continue

        if warn_message!=None and len(warn_message) != 0:
            print('warn_message',warn_message)
            logging.warning('get warn',warn_message)
        # 生成yaml保存在本地
            createyaml("apis_warn",api,yaml_data)
            # 向api2文件追加api
            if not find_line('api2.txt', api):
                with open('api2.txt', 'a+', encoding='utf-8') as f:
                    f.write(api+'\n')
            continue

        # 生成yaml保存在本地
        createyaml("apis_trust",api,yaml_data)
        # 向api1文件追加api
        if not find_line('api1.txt', api):
            with open('api1.txt', 'a+', encoding='utf-8') as f:
                f.write(api+'\n')

        
    # for url in api_list:
    #     spider(url)
if __name__ == '__main__':
    main()