import time
import json
from flask import  Response, stream_with_context
import requests

## chatgpt api 初始化
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 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",
  }
time_sleep = 10
class Timer():
    def __init__(self):
        self.last_time = time.time()
        self.last_time -= time_sleep
    def step(self):
        t_time = time.time()
        if t_time - self.last_time < time_sleep:
            time.sleep(time_sleep - (t_time - self.last_time))
            self.last_time = t_time
my_timer = Timer()

def generate_reply(message, stream=False):
    # 解析用户输入
    t_time = time.time()
    x=1
    if t_time - my_timer.last_time < time_sleep:
        time2sleep = time_sleep - (t_time - my_timer.last_time)
        my_timer.last_time = my_timer.last_time + time_sleep
        print("sleep {}s".format(round(time2sleep)))
        # yield "sleep {}s".format(round(time2sleep))
        time.sleep(time2sleep)
        print('sleep down')
    else:
        my_timer.last_time = time.time()
    print(my_timer.last_time)

    def my_generate():
        data = {
            "model": "gpt-3.5-turbo",
            "messages": message,
            "temperature": 1,
            "stream": False,  # 启用流式API
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            stream=False,  # 同样需要启用流式API
        )
        return json.loads(response.text)['choices'][0]['message']['content']


    def my_generate_stream():
        data = {
            "model": "gpt-3.5-turbo",
            "messages": message,
            "temperature": 1,
            # "max_tokens": 2048,
            "stream": True,  # 启用流式API
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            stream=True,  # 同样需要启用流式API
        )

        alltext = ''
        for chunk in response.iter_content(chunk_size=None):

            if chunk:
                chunk = chunk.decode("utf-8")
                if 'error' in chunk:
                    print('error')
                x = chunk.find('content')
                if x > 0:
                    for line in chunk.split('\n'):
                        if 'content' in line:
                            text = line[line.find('content') + 10:line.find('"},"index"')]
                            text = text.replace('\\n', '\n')
                            break
                    print(text, end='\n')
                    yield text
    # 返回流式响应
    if stream:
        return Response(stream_with_context(my_generate_stream()), mimetype='text/plain')
    else:
        return my_generate()