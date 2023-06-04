import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
def get_info():
    # 创建Chrome浏览器实例
    # 创建Chrome浏览器的选项对象
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    title_set = set()
    url_set = set()
    hot_list = []

    for i in [1,2,3,4]:
        browser = webdriver.Chrome(options=chrome_options)
        # 打开Google首页
        if i == 1:
            browser.get('https://www.3dmgame.com/news/game/')
        else:
            browser.get('https://www.3dmgame.com/news/game_{}/'.format(i))
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
        # 搜集
        #scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(1) > div > div > div > div > div
        # body > div.container > section > div.news_part > div.list_box > ul.excellent_list > li:nth-child(1) > div > a:nth-child(1)

        nums = 0
        for i in range(1):
            # print('第{}轮'.format(i))
            output_tag = ['#newsnav > div.Content_L > div.Revision_list',
]
            id_tag = []


            for tag in output_tag:
                result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag)))
                result = browser.find_element('css selector', tag)
                samples = result.find_elements('css selector', 'ul > li')
                for j, result in enumerate(samples):
                    content = result.find_element('css selector', 'div > a')
                    url = content.get_attribute('href')
                    text = content.text
                    desc = result.find_element('css selector', 'div > div.miaoshu').text

                    if url is not None and text is not None and 'http' in url and len(text) > 5\
                            and text not in title_set and url not in url_set:
                        # print(text + '\t' + url)
                        sample = {'hot_title': text, 'url': url, 'hot_desc': desc}
                        title_set.add(text)
                        url_set.add(url)
                        hot_list.append(sample)
                        nums += 1
                # print('------------')
                x = 1

        browser.quit()
    hot_list = hot_list[:60]
    return hot_list

if __name__ == '__main__':
    get_info()
