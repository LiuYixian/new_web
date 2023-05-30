import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tools.translation_apt import translation_detail_to_chinese
from selenium.webdriver.chrome.options import Options
import time
def get_info(geo = "IN"):
    # 创建Chrome浏览器实例
    # 创建Chrome浏览器的选项对象
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(options=chrome_options)
    # 打开Google首页
    browser.get('https://trends.google.com/trends/trendingsearches/daily?geo={}&hl=zh-CN'.format(geo))
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
    for i in range(1):
        # print('第{}轮'.format(i))
        # output_tag = ['body > div.wrap > div.wrapBg > div > div.wrapCon']
        id_tag = []
        output_tag = ['body > div.trends-wrapper > div:nth-child(2) > div > div.feed-content > div > div.generic-container-wrapper > ng-include > div > div > div']
        # id_tag = ['#rm_cj01', '#rm_cj02', '#rm_kj01', '#rm_kj02', '#rm_kj03', '#rm_gj01','#rm_gj02',
        #           '#rm_gj03', '#rm_gj04', '#rm_df01', '#rm_df03', '#rm_df04', '#rm_wt01', '#rm_wt02',
        #           '#rm_wt03', '#rm_jk01']

        # feed-item-Tom\ Brady > div.details > div.title.title-break > span > span
        for tag in output_tag:
            result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag)))
            result = browser.find_element('css selector', tag)
            #feed-item-Tom\ Brady > div.details-wrapper > div.details
            results = result.find_elements('css selector', 'div.details')
            for result in results:
                # feed-item-Tom\ Brady > div.details-wrapper > div.details > div.details-top > div > span > a
                top_title_element = result.find_element('css selector', 'div.details-top > div > span > a')
                # feed-item-Tom\ Brady > div.details-wrapper > div.details > div.details-bottom > div.subtitles-text-wrapper.visible > div.summary-text > a
                button_detail_element = result.find_element('css selector', 'div.details-bottom > div.subtitles-text-wrapper.visible > div.summary-text > a')
                top_title = top_title_element.text
                top_url = top_title_element.get_attribute('href')
                butto_title = button_detail_element.text
                butto_url = button_detail_element.get_attribute('href')
                sample = {'hot_title_for': top_title + '-' + butto_title, 'url': butto_url}
                hot_list.append(sample)

    browser.quit()

    hot_list = hot_list[:60]
    hot_list = translation_detail_to_chinese(hot_list)

    return hot_list
if __name__ == '__main__':
    get_info()

