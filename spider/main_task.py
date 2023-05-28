import pandas as pd
import importlib
import os
import time
import json
from datetime import datetime


def run_spider(date, hour, part):
    with open('worker_list.json', encoding='utf8') as f:
        web_dict = json.load(f)
    # web_dict =
    # parts = ['foreign_news']
    # for part in web_dict:
    if True:
        for file in os.listdir('{}/{}'.format('workers', part)):
            if file.endswith('.py'):
                module_name = file[:-3]
                fun_name = 'get_info'
                module = importlib.import_module('workers.{}.{}'.format(part, module_name))
                fun = getattr(module, fun_name)
                result = fun()
                # 保存在 data/{key}/timestamp.csv
                tgt_dir = 'data/{}/{}'.format(part, module_name)
                os.makedirs(tgt_dir, exist_ok=True)

                New_data = dict()
                result = [a for a in result if 'hot_title' in a]
                for k in result[0].keys():
                    New_data[k] = [a[k] for a in result]
                x = 1
                df = pd.DataFrame(New_data)
                if 'hot_rank' in df:
                    x = 1
                    df['hot_rank'] = df['hot_rank'].astype(int)
                    df = df.sort_values('hot_rank').drop_duplicates()
                df = df.drop_duplicates(subset = ['hot_title'], keep = 'first')
                if 'hot_title_for' in df:
                    df.loc[df['hot_title'] == '', 'hot_title'] = df['hot_title_for']

                df.to_csv('{}/{}_{}.csv'.format(tgt_dir, date, hour), index=False, sep='\t')


if __name__ == '__main__':

    date = str(datetime.now())[:10]
    hour = datetime.now().hour
    minute = datetime.now().minute
    run_spider(date, hour, 'domestic_news')
    run_spider(date, hour, 'domestic_platform')
    run_spider(date, hour, 'foreign_news')
    run_spider(date, hour, 'foreign_platform')

    min_num = 0
    hour_num = 0
    while True:
        # 60 分钟一次， domestic_platform
        date = str(datetime.now())[:10]
        hour = datetime.now().hour
        minute = datetime.now().minute
        if min_num == 60:
            run_spider(date, hour, 'domestic_platform')
            min_num = 0
        if hour_num == 12:
            for part in ['domestic_news', 'foreign_news', 'foreign_platform']:
                run_spider(date, hour, part)
            hour_num = 0
        time.sleep(60)
        min_num += 1
        if min_num == 60:
            hour_num += 1

