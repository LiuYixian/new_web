import pandas as pd
import importlib
import os
import time
import json
from datetime import datetime


def run_spider(date, hour):
    with open('worker_list.json', encoding='utf8') as f:
        web_dict = json.load(f)
    # web_dict =
    # parts = ['foreign_news']
    for part in web_dict:
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



                df.to_csv('{}/{}_{}.csv'.format(tgt_dir, date, hour), index=False, sep='\t')


if __name__ == '__main__':
    last_label = ''
    while True:

            date = str(datetime.now())[:10]
            hour = datetime.now().hour
            minute = datetime.now().minute
            t_label = '{}_{}'.format(date, hour)
            if t_label != last_label:
                run_spider(date, hour)
            time.sleep(60)
            last_label = t_label
            break





