import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
# 创建Chrome浏览器实例
def get_info():
    browser = webdriver.Chrome()
    # 打开Google首页
    browser.get('https://www.douyin.com/hot')
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
        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.BHgRhxNh')))
        results = browser.find_elements('css selector', 'li.BHgRhxNh')
        for j, result in enumerate(results):
            # rank_title = result.find_element('css selector', 'dev.ThgqDnuv')
            # rank_img = rank_title.get_attribute('src')
            # rank = rank_img.split('/')[-1][:-4]
            rank = j
            # douyin-right-container > div:nth-child(2) > div > div.hMNE3E7I > ul > li:nth-child(1) > div.ThgqDnuv > img
            # title_elem = result.find_element('css selector' ,'h3')
            # title = title_elem.text

            # index = result.find_element('css selector', 'div')
            content = result.find_element('css selector', 'a')
            url = content.get_attribute('href')
            title = content.text

            try:
                hot = result.find_element('css selector', 'div.GsuT_hjh')
                hot = hot.text
            except:
                hot = 0
            # text_split = index.text.split('\n')
            if True:
                # 非置顶 普通热点
                hot_rank = rank
                hot_title = title
                hot_score = hot
                sample = {'hot_rank': hot_rank, 'hot_title': hot_title, 'hot_score': hot_score, 'url': url}
                hot_list.append(sample)
            # else:
            #     # 置顶热点
            #     hot_rank = 0
            #     hot_title = text_split[0]
            #     sample = {'hot_rank': '0', 'hot_title': hot_title, 'hot_score': '0', 'url': url}
            #     hot_list[hot_rank] = sample

        print('------------------------')
        if len(hot_list) >= 51:
            break
        # 滚动
        # 记录滚动前的页面高度
        # last_height = browser.execute_script("return window.scrollY")
        # # 执行 JavaScript 向下滚动 1000 像素
        # browser.execute_script("window.scrollBy(0, 1000);")
        #
        # # 获取当前页面高度和滚动条位置
        # new_height = browser.execute_script("return window.scrollY")

        # 如果滚动条已到底部，停止滚动
        # if new_height == last_height:
        #     break

        # browser.find_element('tag name', 'html').send_keys(Keys.END)
        # 等待加载新内容
        time.sleep(2)

    # with open('../result_douyin.json', 'w', encoding='utf8') as wf:
    #     json.dump(hot_list, wf, ensure_ascii=False)
    #
    # x=1

    # 关闭浏览器<div class="HotTopic_rank1_1lpCB HotTopic_rankimg_2Y9y8"><span class="HotTopic_ranknum_MdimB">1</span></div>
    browser.quit()
    #rso > div:nth-child(1) > div > div > div > div > div > div > div.yuRUbf > a > h3

    return hot_list