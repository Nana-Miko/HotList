import os
import traceback
import requests
import simuse
from bs4 import BeautifulSoup
import yaml
import time
import datetime
import DrawImg

url = "https://tophub.today"
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    nodes = soup.find_all('div', class_='cc-cd')
    return nodes


def search(net):
    print('获取{}榜单中...'.format(net))
    res = requests.request('get', url, headers=headers)
    #print(res)
    nodes = get_data(res.text)
    content_list = []
    for node in nodes:
        source = node.find('div', class_='cc-cd-lb').text.strip()
        messages = node.find('div',
                             class_='cc-cd-cb-l nano-content').find_all('a')
        mine = node.find('div', class_='cc-cd-is').find_all('a')[0]

        mine_url = url + mine['href']
        if source.lower() == net.lower():
            for message in messages:
                content = message.find('span', class_='t').text.strip()
                content_list.append(content)
            break

    return mine_url, content_list


def auto_search(net_list):
    print('获取{}榜单中...'.format(str(net_list)))
    content_dict = {}
    url_dict = {}
    for i in net_list:
        content_dict[i.lower()] = []
        url_dict[i.lower()] = ''

    res = requests.request('get', url, headers=headers)
    #print(res)
    nodes = get_data(res.text)

    for node in nodes:
        source = node.find('div', class_='cc-cd-lb').text.strip()
        messages = node.find('div',
                             class_='cc-cd-cb-l nano-content').find_all('a')
        mine = node.find('div', class_='cc-cd-is').find_all('a')[0]

        mine_url = url + mine['href']
        if source.lower() in content_dict.keys():
            for message in messages:
                content = message.find('span', class_='t').text.strip()
                content_dict[source.lower()].append(content)
                url_dict[source.lower()] = mine_url

    return url_dict, content_dict


def source_default():
    res = requests.request('get', url, headers=headers)
    sources = set()
    nodes = get_data(res.text)
    for node in nodes:
        source = node.find('div', class_='cc-cd-lb').text.strip()
        sources.add(source.lower())

    return sources


def send_res(res_, source, group):
    mine_url = res_[0]
    content_list = res_[1]

    im = DrawImg.draw_img(source,
                          content_list,
                          edge=data['edge'],
                          num=data['sum'])
    im.save('send_img.png', 'PNG')
    im.close()

    messagechain = [{
        'type': 'Image',
        'path': os.getcwd() + '\\send_img.png'
    }, {
        'type': 'Plain',
        'text': mine_url
    }]
    #print(os.getcwd()+'\\send_img.png')
    CT.Send_Message_Chain(group, 1, messagechain)


def auto_send():
    global day
    now_ = datetime.datetime.now()
    now_time = now_.strftime('%H:%M')
    now_day = now_.strftime('%d')
    #print(now_time,now_day,data['autoSendTime'])
    if now_time == data['autoSendTime'] and now_day != day:
        res_ = auto_search(data['autoSearch'])
        url_dict = res_[0]
        content_dict = res_[1]

        for source in content_dict:
            im = DrawImg.draw_img(source,
                                  content_dict[source],
                                  edge=data['edge'],
                                  num=data['sum'])
            im.save('{}.png'.format(source), 'PNG')
            im.close()

        for group in data['autoSendGroup']:
            CT.Send_Message(group, 1, data['autoSendTip'], 1)
            for source in url_dict:
                messagechain = [{
                    'type': 'Image',
                    'path': os.getcwd() + '\\{}.png'.format(source)
                }, {
                    'type': 'Plain',
                    'text': url_dict[source]
                }]
                CT.Send_Message_Chain(group, 1, messagechain)

        day = now_day

    else:
        return None


#data={"command":['{}热榜','热榜 {}'],'autoSendTime':'08:00','autoSendGroup':[123456,789456123],'HelpCommand':['热榜help']}
#yaml.dump(data,open('setting.yml','w',encoding='utf-8-sig'),allow_unicode=True)

if __name__ == '__main__':
    day = None
    print('正在初始化...')
    data = yaml.load(open('setting.yml', 'r', encoding='utf-8-sig'),
                     Loader=yaml.FullLoader)

    sources = source_default()
    print(sources)

    CT = simuse.Client()
    print('正在监听中...')
    while True:
        try:
            message = CT.Fetch_Message()
            auto_send()
            if type(message) == type(0):
                time.sleep(0.5)
                continue

            for i in message:
                if i['type'] == 'GroupMessage':
                    group = i['group']
                    messagechain = i['messagechain']
                    command = messagechain[1]

                    if command['type'] == 'Plain' and command['text'][
                            0] == '#' and command['text'][-2:] == '榜单':
                        source = command['text'][1:-2]
                        if source.lower() not in sources:
                            CT.Send_Message(group, 1,
                                            '未找到名为"{}"的榜单'.format(source), 1)
                            continue

                        res_ = search(source)
                        send_res(res_, source, group)
                    elif command['type'] == 'Plain' and command['text'] in data['HelpCommand']:
                        CT.Send_Message(group,1,os.getcwd()+'\\help.png',2,path=1)

        except Exception as e:
            traceback.print_exc()
        finally:
            time.sleep(0.5)
            continue
