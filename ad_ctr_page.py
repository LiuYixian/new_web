from flask import Flask, render_template, request
from utils.chat_gpt_api import generate_reply
from utils.logger import info2file



app = Flask(__name__)

## chatgpt api 初始化


@app.route('/api/response', methods=['POST'])
def ad_analysis():
    # 解析用户输入

    info2file(task = 'ad_analysis', info = 'request: {}'.format(str(request.json)))
    text = request.json.get('text', '')
    name = request.json.get('name', '')
    intro = request.json.get('intro', '')
    channel = request.json.get('channel', '')
    motivation = request.json.get('motivation', '')
    num_limit = request.json.get('num_limit', '')
    channel_map = {
        'weixin_gzh': '微信公众号',
        'weixin_red': '微信红点广告',
        'qq_gzh': 'QQ公众号',
        'qq_red': 'QQ红点广告'
    }
    if text == '' and (name == ''):
        info2file(task = 'ad_analysis', info = 'result: {}'.format(str('请提供待分析文案，以能够进行分析。或者提供游戏名和广告目的，以提供文案建议。')))
        return {'错误': '请提供待分析文案，以能够进行分析。或者提供游戏名和广告目的，以提供文案建议。'}
    if text != '':
        request_str = '"{}"这是一条游戏广告文案标题。'.format(text)
        if name != '':
            request_str += '关于游戏《{}》。'.format(name)
        if intro != '':
            request_str += '这个游戏{}。'.format(intro)
        if channel != 'other':
            request_str += '这条广告将投放在{}。'.format(channel_map[channel])
        if motivation != '':
            request_str += '广告的宣传目的是{}。'.format(motivation)
        request_str += '现在请你以10分制为这个广告文案打分，分析其优点和缺点，提出改进建议，并且提供优化示例'
        if num_limit != '':
            request_str += '，优化结果尽量不要超过{}个字'.format(num_limit)
        request_str += '。'
        request_str = request_str.replace('。。', '。')

        message = [
            {"role": "user", "content": request_str},
        ]
    else:
        request_str = '请为《{}》游戏写几条广告素材文案标题。'.format(name)
        if intro != '':
            request_str += '该游戏是{}。'.format(intro)
        if channel != 'other':
            request_str += '这条广告将投放在{}。'.format(channel_map[channel])
        if motivation != '':
            request_str += '希望这条广告能够{}。'.format(motivation)
        if num_limit != '':
            request_str += '，优化结果尽量不要超过{}个字。'.format(num_limit)
        request_str = request_str.replace('。。', '。')
        message = [
            {"role": "user", "content": request_str},
        ]

    info2file(task = 'ad_analysis', info = 'message: {}'.format(str(message)))
    result = generate_reply(message = message, stream= False)
    info2file(task = 'ad_analysis', info = 'result: {}'.format(str(message)))


    if text != '':
        return {'分析结果': result}
    else:
        return {'生成结果': result}

@app.route('/api/check_pre_save_role')
def check_pre_save_role():
    print('function')
    result = {
        '钟离': "钟离",
        'hutao': "胡桃",
    }
    return result

@app.route('/api/get_role_config', methods=['POST'])
def get_role_config():
    return {
        'a': 'a',
        'b': 'b'
    }



@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/chat')
def chat_page():
    return render_template('chat_page.html')

@app.route('/ad')
def ad_page():
    return render_template('ad_ctr_page.html')

# @app.route('/ad_analysis' , methods=['POST'])
# def ad_analysis():
#     x=1
#     print('111111111111')
#     return json.dumps({'a': 'a', 'b': 'b'})

# @app.route('/')
# def index():
#     return render_template('main_page.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)