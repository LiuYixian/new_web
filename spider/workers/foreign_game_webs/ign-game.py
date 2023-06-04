import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools.translation_apt import translation_detail_to_chinese
from selenium.webdriver.chrome.options import Options
import time
def get_info():
    # 创建Chrome浏览器实例
    hot_list = []
    titles = set()
    urls = set()

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(options=chrome_options)
    # 打开Google首页
    browser.get('https://www.ign.com/?filter=games')
    '''
        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"
        '''
    x=1
    wait = WebDriverWait(browser, 10)

    for i in range(1):

        output_tag = ['#main-content > section > div.content-feed-grid-wrapper']

        for tag in output_tag:
            result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag)))
            for i in range(2):
                # 记录滚动前的页面高度
                last_height = browser.execute_script("return window.scrollY")
                # 执行 JavaScript 向下滚动 1000 像素
                browser.execute_script("window.scrollBy(0, 100000);")

                # 获取当前页面高度和滚动条位置
                new_height = browser.execute_script("return window.scrollY")

                # 如果滚动条已到底部，停止滚动
                if new_height == last_height:
                    break

                # browser.find_element('tag name', 'html').send_keys(Keys.END)
                # 等待加载新内容
                time.sleep(2)
            results = browser.find_elements('css selector', tag)
            for result in results:
                samples = result.find_elements('css selector', 'section > section.main-content > div > a')
                for j, result in enumerate(samples):
                    url = result.get_attribute('href')
                    text = result.find_element('css selector', 'div.stack.jsx-3935032277.item-details > span')
                    text = text.text
                    desc = result.find_element('css selector', 'div.stack.jsx-3935032277.item-details > div.interface.jsx-1545499971.jsx-957202555.item-subtitle.small')
                    desc = desc.text.split('\n')[-1]
                    if url is not None and text is not None and 'http' in url and len(text.split(' ')) > 4 and text not in titles\
                            and url not in urls:
                        titles.add(text)
                        urls.add(url)
                        # print(text)
                        sample = {'hot_title_for': text, 'url': url, 'hot_desc_for': desc}
                        hot_list.append(sample)
        # 滚动


    browser.quit()

    browser = webdriver.Chrome(options=chrome_options)
    # 打开Google首页
    browser.get('https://www.ign.com/')
    '''
        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"
        '''
    x = 1
    wait = WebDriverWait(browser, 10)

    for i in range(1):

        output_tag = ['#main-content > section > div.content-feed-grid-wrapper']

        for tag in output_tag:
            result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag)))
            for i in range(2):
                # 记录滚动前的页面高度
                last_height = browser.execute_script("return window.scrollY")
                # 执行 JavaScript 向下滚动 1000 像素
                browser.execute_script("window.scrollBy(0, 100000);")

                # 获取当前页面高度和滚动条位置
                new_height = browser.execute_script("return window.scrollY")

                # 如果滚动条已到底部，停止滚动
                if new_height == last_height:
                    break

                # browser.find_element('tag name', 'html').send_keys(Keys.END)
                # 等待加载新内容
                time.sleep(2)
            results = browser.find_elements('css selector', tag)
            for result in results:
                samples = result.find_elements('css selector', 'section > section.main-content > div > a')
                for j, result in enumerate(samples):
                    url = result.get_attribute('href')
                    text = result.find_element('css selector', 'div.stack.jsx-3935032277.item-details > span')
                    text = text.text
                    desc = result.find_element('css selector',
                                               'div.stack.jsx-3935032277.item-details > div.interface.jsx-1545499971.jsx-957202555.item-subtitle.small')
                    desc = desc.text.split('\n')[-1]
                    if url is not None and text is not None and 'http' in url and len(
                            text.split(' ')) > 4 and text not in titles \
                            and url not in urls:
                        titles.add(text)
                        urls.add(url)
                        # print(text)
                        sample = {'hot_title_for': text, 'url': url, 'hot_desc_for': desc}
                        hot_list.append(sample)
        # 滚动

    browser.quit()





    hot_list = hot_list[:60]
    hot_list = translation_detail_to_chinese(hot_list)

    return hot_list




if __name__ == '__main__':
    get_info()
