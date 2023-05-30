import requests
from tools.chat_gpt_api import generate_reply

batch = 20
def translation_detail_to_chinese(hot_list):
    tran_result = []
    foreign = []
    # zh_texts = ''
    for a in hot_list:
        foreign.append(a['hot_title_for'])
        if len(foreign) >= batch:
            for i in range(3):
                zh_text = translate('\n\n'.join(foreign))
                zh_text = zh_text.replace('\n\n', '\n').replace('\n\n', '\n')
                zh_texts = zh_text.split('\n')
                zh_texts = [a for a in zh_texts if a.strip() != '']
                if len(zh_texts) >= batch:
                    break
            if len(zh_texts) == batch:
                tran_result.extend(zh_texts)
            else:
                if len(zh_texts) > batch:
                    zh_texts = zh_texts[:batch]
                else:
                    zh_texts = zh_texts + [''] * (batch - len(zh_texts))
                tran_result.extend(zh_texts)
            foreign = []
    if len(foreign) > 0:
        ori_len = len(foreign)
        for i in range(3):
            zh_text = translate('\n\n'.join(foreign))
            zh_text = zh_text.replace('\n\n', '\n').replace('\n\n', '\n')
            zh_texts = zh_text.split('\n')
            zh_texts = [a for a in zh_texts if a.strip() != '']
            if len(zh_texts) >= ori_len:
                break
        if len(zh_texts) == ori_len:
            tran_result.extend(zh_texts)
        else:
            if len(zh_texts) > ori_len:
                zh_texts = zh_texts[:ori_len]
            else:
                zh_texts = zh_texts + [''] * (ori_len - len(zh_texts))
            tran_result.extend(zh_texts)

    for i in range(len(tran_result)):
        hot_list[i]['hot_title'] = tran_result[i]
    return hot_list

def translate(text):
    message = [
              {"role": "system", "content": "Translate the following text to Chinese. Every line input should be translated to one Chinese sentence in a line."},
              {"role": "user", "content": text}
            ]
    alltext = generate_reply(message, stream=False)
    return alltext