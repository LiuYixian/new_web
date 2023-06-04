import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
def get_info():
    # 创建Chrome浏览器实例
    # 创建Chrome浏览器的选项对象
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(1280*2, 800*2)
    # 打开Google首页
    browser.get('https://www.gamersky.com/news/')
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
    hot_list = []
    title_set = set()
    url_set = set()
    nums = 0
    time.sleep(2)
    next_element = browser.find_element('css selector', 'body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_nav > div > a:nth-child(2)')
    next_element.click()

    for i in range(2):
        # print('第{}轮'.format(i))
        # body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block
        output_tag = [
            'body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block',
                      ]

        for tag in output_tag:
            result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag)))
            result = browser.find_element('css selector', tag)
            samples = result.find_elements('css selector', 'ul > li')

            for j, result in enumerate(samples):
                content = result.find_element('css selector', 'div.tit > a')
                url = content.get_attribute('href')
                text = content.text
                desc = result.find_element('css selector', 'div.con > div.txt').text
                if url is not None and text is not None and 'http' in url and len(text) > 5\
                        and text not in title_set and url not in url_set:
                    # print(text + '\t' + url)
                    sample = {'hot_title': text, 'url': url, 'hot_desc': desc}
                    title_set.add(text)
                    url_set.add(url)
                    hot_list.append(sample)
                    nums+=1
            # print('------------')
            x = 1

        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pe100_page_pic_tu1 > a.p1.nexe')))
        actions = ActionChains(browser)
        time.sleep(2)
        actions.move_to_element(element).perform()
        time.sleep(2)
        element.click()
        time.sleep(2)
        # pe100_page_pic_tu > a.p1.nexe
    browser.quit()
    hot_list = hot_list[:60]
    return hot_list

if __name__ == '__main__':
    get_info()
