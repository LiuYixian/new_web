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
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(options=chrome_options)
    # 打开Google首页
    browser.get('https://www.indiatoday.in/')
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
    titles = set()
    for i in range(2):
        print('第{}轮'.format(i))
        # output_tag = ['body > div.wrap > div.wrapBg > div > div.wrapCon']
        id_tag = []
        output_tag = ['#main > div > div > div.content__section > main > div.lhs__section']
        # id_tag = ['#rm_cj01', '#rm_cj02', '#rm_kj01', '#rm_kj02', '#rm_kj03', '#rm_gj01','#rm_gj02',
        #           '#rm_gj03', '#rm_gj04', '#rm_df01', '#rm_df03', '#rm_df04', '#rm_wt01', '#rm_wt02',
        #           '#rm_wt03', '#rm_jk01']


        for tag in output_tag:
            result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag)))
            result = browser.find_element('css selector', tag)
            samples = result.find_elements('css selector', 'a')
            for j, result in enumerate(samples):
                url = result.get_attribute('href')
                text = result.text.replace('\n', ' ')


                if url is not None and text is not None and 'http' in url and len(text.split(' ')) > 4 and text not in titles:
                    titles.add(text)
                    print(text)
                    sample = {'hot_title_for': text, 'url': url}
                    hot_list.append(sample)
            print('------------')
            x = 1

        for tag in id_tag:
            tag = tag.strip('#')
            try:
                results = wait.until(EC.presence_of_all_elements_located((By.ID, tag)))
                result = browser.find_element('id', tag)
                samples = result.find_elements('css selector', 'a')
                # result = results[0]
                # results = result.find_elements('css selector', 'a')
                for j, result in enumerate(samples):
                    url = result.get_attribute('href')
                    text = result.text.replace('\n', ' ')
                    if url is not None and text is not None and 'http' in url and len(text.split(' ')) > 4:
                        print(text + '\t' + url)
                        sample = {'hot_title_for': text, 'url': url}
                        hot_list.append(sample)
                print('-----------------')
            except:
                print('错误tag {}'.format(tag))
                pass
            x=1
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
    browser.quit()

    hot_list = hot_list[:60]
    hot_list = translation_detail_to_chinese(hot_list)

    return hot_list




if __name__ == '__main__':
    get_info()
