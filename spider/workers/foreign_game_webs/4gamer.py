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
    browser.get('https://www.4gamer.net/')
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

        output_tag = ['#NEWS_SELECT_DAY_1','#NEWS_SELECT_DAY_2','#NEWS_SELECT_DAY_3','#NEWS_SELECT_DAY_4']

        for tag in output_tag:
            try:
                result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag)))
                result = browser.find_element('css selector', tag)
                samples = result.find_elements('css selector', 'div > div.V2_article_container')
                for j, result in enumerate(samples):
                        content = result.find_element('css selector', 'h2 > a')
                        url = content.get_attribute('href')
                        text = content.text
                        try:
                            desc = result.find_element('css selector', 'p').text
                        except:
                            desc = ''

                        if url is not None and text is not None and 'http' in url and len(text) > 4 and text not in titles\
                                and url not in urls:
                            titles.add(text)
                            urls.add(url)
                            # print(text)
                            sample = {'hot_title_for': text, 'url': url, 'hot_desc_for': desc}
                            hot_list.append(sample)
            except:
                pass
            # 滚动


    browser.quit()

    hot_list = hot_list[:60]
    hot_list = translation_detail_to_chinese(hot_list)

    return hot_list




if __name__ == '__main__':
    get_info()
