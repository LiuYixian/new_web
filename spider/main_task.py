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
                tgt_dir = 'data/{}/{}'.format(part, module_name)
                tgt_file = '{}/{}_{}.csv'.format(tgt_dir, date, hour)
                if os.path.exists(tgt_file):
                    print('skip {}'.format(file))
                    continue
                if part in ['domestic_news', 'foreign_news', 'foreign_platform']:
                    continue_mark = False
                    for h in range(12):
                        if int(hour) >= h and os.path.exists('{}/{}_{}.csv'.format(tgt_dir, date, int(hour) - h)):
                            continue_mark = True
                            break
                    if continue_mark:
                        print('skip {}'.format(file))
                        continue

                print('开始处理{}'.format(file))

                fun = getattr(module, fun_name)
                for i in range(5):
                    try:
                        result = fun()
                        if len(result) == 0:
                            raise NameError('空 result')
                        break
                    except Exception as ex:
                        print('出现异常\n{}'.format(ex))
                        result = None
                if result is None:
                    continue
                # 保存在 data/{key}/timestamp.csv

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
    run_spider(date, hour, 'game_webs')
    run_spider(date, hour, 'foreign_game_webs')

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
            for part in ['domestic_news', 'foreign_news', 'foreign_platform', 'game_webs', 'foreign_game_webs']:
                run_spider(date, hour, part)
            hour_num = 0
        time.sleep(60)
        min_num += 1
        if min_num == 60:
            hour_num += 1

