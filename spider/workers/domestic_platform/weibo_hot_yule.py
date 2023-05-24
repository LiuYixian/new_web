import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
def get_info():
    # 创建Chrome浏览器实例
    browser = webdriver.Chrome()
    # 打开Google首页
    browser.get('https://weibo.com/newlogin?tabtype=entertainment&gid=&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F')
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
    hot_list = []
    for i in range(10):
        print('第{}轮'.format(i))
        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.vue-recycle-scroller__item-view')))
        results = browser.find_elements('css selector', 'div.vue-recycle-scroller__item-view')

        for result in results:
            # title_elem = result.find_element('css selector' ,'h3')
            # title = title_elem.text
            index = result.find_element('css selector', 'div')
            content = result.find_element('css selector', 'a')
            url = content.get_attribute('href')
            text_split = index.text.split('\n')
            if text_split[0].isnumeric():
                # 非置顶 普通热点
                hot_rank = text_split[0]
                hot_title = text_split[1]
                hot_score = text_split[-1]
                sample = {'hot_rank': hot_rank, 'hot_title': hot_title, 'hot_score': hot_score, 'url': url}
                hot_list.append(sample)
            else:
                continue
                # 置顶热点
                hot_rank = 0
                hot_title = text_split[0]
                sample = {'hot_rank': '0', 'hot_title': hot_title, 'hot_score': '0', 'url': url}
                hot_list.append(sample)
        print('------------------------')
        if len(hot_list) >= 50:
            break
        # 滚动
        # 记录滚动前的页面高度
        last_height = browser.execute_script("return window.scrollY")
        # 执行 JavaScript 向下滚动 1000 像素
        browser.execute_script("window.scrollBy(0, 1000);")

        # 获取当前页面高度和滚动条位置
        new_height = browser.execute_script("return window.scrollY")

        # 如果滚动条已到底部，停止滚动
        if new_height == last_height:
            break

        # browser.find_element('tag name', 'html').send_keys(Keys.END)
        # 等待加载新内容
        time.sleep(2)

    # with open('../result_yule.json', 'w', encoding='utf8') as wf:
    #     json.dump(hot_list, wf, ensure_ascii=False)
    #
    # x=1

    # 关闭浏览器<div class="HotTopic_rank1_1lpCB HotTopic_rankimg_2Y9y8"><span class="HotTopic_ranknum_MdimB">1</span></div>
    browser.quit()
    #rso > div:nth-child(1) > div > div > div > div > div > div > div.yuRUbf > a > h3
    return hot_list