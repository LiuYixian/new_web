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
    browser.get('http://www.people.com.cn/')
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
    nums = 0
    for i in range(1):
        print('第{}轮'.format(i))
        output_tag = ['body > div.main > div.sp_bg.cf',
                      '#rm_pljd > div.col.col-1.fl',
                      '#rm_pljd > div.col.col-2.fr',
                      '#rm_cpc > div.cpc_bg1.cf',
                      '#rm_ldly > div:nth-child(5) > ul.list4.cf',
                      '#rm_video > div.picg1.mt20.cf',
                      '#rm_hotzt > div.hotzt.cf',]
        id_tag = ['#rm_cj01', '#rm_cj02', '#rm_kj01', '#rm_kj02', '#rm_kj03', '#rm_gj01','#rm_gj02',
                  '#rm_gj03', '#rm_gj04', '#rm_df01', '#rm_df03', '#rm_df04', '#rm_wt01', '#rm_wt02',
                  '#rm_wt03', '#rm_jk01']


        for tag in output_tag:
            result = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tag)))
            result = browser.find_element('css selector', tag)
            samples = result.find_elements('css selector', 'a')
            for j, result in enumerate(samples):
                url = result.get_attribute('href')
                text = result.text
                if url is not None and text is not None and 'http' in url and len(text) > 4:
                    print(text + '\t' + url)
                    sample = {'hot_title': text, 'url': url}
                    hot_list.append(sample)
                    nums+=1
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
                    text = result.text
                    if url is not None and text is not None and 'http' in url and len(text) > 4:
                        print(text + '\t' + url)
                        sample = {'hot_title': text, 'url': url}
                        hot_list.append(sample)
                        nums += 1
                print('-----------------')
            except:
                print('错误tag {}'.format(tag))
                pass
            x=1
    browser.quit()
    return hot_list
