from pyquery import PyQuery as pq
import time, httpx, re
from helium import *

'''
fanjiao share url: https://s.rela.me/c/1SqTNu?album_id={}
    redirect to: https://www.rela.me/game/operation42.html?album_id={}
    https://www.fanjiao.co/pages/share.html?album_id={}
manbo mobile url: 
    整部：https://manbo.hongdoulive.com/Activecard/radioplay?id={drama_id}&t={timestamp}
    单集: https://manbo.hongdoulive.com/Activecard/episode?id={ep_id}&radioDramaId={drama_id}
manbo pc url: https://manbo.hongdoulive.com/manbo/pc/detail?id={ep_id}&collectId={drama_id}
maoer pc url: https://www.missevan.com/mdrama/{}
maoer mobile url: https://m.missevan.com/drama/{}
'''

def selenium_opener(url):
    driver = start_chrome(url, headless=True)
    # 等待元素加载完成
    wait_until(Text("参演CV").exists)
    html = driver.page_source
    driver.quit()
    return html

def get_audio_detail(audio_url):
    if 'rela.me' in audio_url or 'fanjiao.co' in audio_url:
        album_id = audio_url.split('album_id=')[1]
        return get_fanjiao_info(album_id)
    elif audio_url.startswith('https://manbo.hongdoulive.com/Activecard/episode'):
        drama_id = audio_url.split('radioDramaId=')[1]
        return get_manbo_info(drama_id)
    elif audio_url.startswith('https://manbo.hongdoulive.com/Activecard/radioplay'):
        drama_id = re.split(r'[=&]', audio_url)[1]
        return get_manbo_info(drama_id)
    elif audio_url.startswith('https://manbo.hongdoulive.com/manbo/pc/detail'):
        drama_id = audio_url.split('collectId=')[1]
        return get_manbo_info(drama_id)
    elif 'missevan.com' in audio_url:
        return get_maoer_info(audio_url.split('/')[-1])
    else:
        return {
            'success': False,
            'error': '不支持的url格式'
        }

def get_fanjiao_info(album_id):
    url = f'https://www.rela.me/game/operation42.html?album_id={album_id}'
    doc = pq(url, opener=selenium_opener)
    if doc is not None:
        title = doc('.info > .title').text()
        cover = doc('.cover_img').attr('src')
        playCount = doc('.num > .play_num > span.strong').text()
        likeCount = doc('.num > .like_num > span.strong').text()
        if 'w' in playCount:
            playCount = int(float(playCount.replace('w', '')) * 10000)
        elif 'k' in playCount:
            playCount = int(float(playCount.replace('k', '')) * 1000)
        if 'w' in likeCount:
            likeCount = int(float(likeCount.replace('w', '')) * 10000)
        elif 'k' in likeCount:
            likeCount = int(float(likeCount.replace('k', '')) * 1000)
        intro = doc('.detail').text()
        return {
            'success': True,
            'data': {
                'name': title,
                'fjId': album_id,
                'fjPlayCount': playCount,
                'likeCount': likeCount,
                'intro': intro,
                'cover': cover,
                'platforms': [3]
            }
        }
    else:
        return {
            'success': False,
            'error': 'url解析出错'
        }


def get_maoer_info(drama_id):
    url = f'https://www.missevan.com/dramaapi/getdrama?drama_id={drama_id}'
    res = httpx.get(url)
    res_json = res.json()
    if 'info' in res_json and 'drama' in res_json['info']:
        intro = res_json['info']['drama']['abstract']
        playCount = res_json['info']['drama']['view_count']
        up = res_json['info']['drama']['author']
        cover = res_json['info']['drama']['cover']
        eps = res_json['info']['episodes']['episode']
        try:
            if len(eps) > 0:
                ep_id = eps[0]['sound_id']
                ep_res = httpx.get(f'https://www.missevan.com/sound/getsound?soundid={ep_id}')
                ep_json = ep_res.json()
                if 'info' in ep_json and 'user' in ep_json['info']:
                    up = ep_json['info']['user']['username']
        finally:
            pass
        return {
            'success': True,
            'data': {
                'name': res_json['info']['drama']['name'],
                'mrId': drama_id,
                'mrPlayCount': playCount,
                'intro': intro,
                'up': up,
                'cover': cover,
                'platforms': [4]
            }
        }
    else:
        return {
            'success': False,
            'error': 'url解析出错'
        }


def get_manbo_info(drama_id):
    url = f'https://manbo.hongdoulive.com/web_manbo/dramaDetail?dramaId={drama_id}'
    res = httpx.get(url)
    res_json = res.json()
    print(res_json)
    if 'code' in res_json and res_json['code'] == 200:
        title = res_json['data']['title']
        intro = res_json['data']['desc']
        cover = res_json['data']['coverPic']
        status = res_json['data']['endStatus'] # 0 连载中 1 已完结
        up = res_json['data']['ownerResp']['nickname']
        playCount = res_json['data']['watchCount']
        return {
            'success': True,
            'data': {
                'name': title,
                'mbId': drama_id,
                'mbPlayCount': playCount,
                'intro': intro,
                'cover': cover,
                'status': status,
                'up': up,
                'platforms': [5]
            }
        }
    else:
        return {
            'success': False,
            'error': 'url解析出错'
        }

if __name__ == "__main__":
    print(get_fanjiao_info(102015))
    # print(get_maoer_info(48438))
    # print(get_manbo_info(1615570361183633506))