from pyquery import PyQuery as pq
import httpx
import re

# uid 用户id
# mblogid  "LDKtmjg78" web端的博文id
# mid "4794734364590178" 移动端的博文id
# containerId 1076031669879400
# web端链接格式：https://weibo.com/{uid}/{mblogid}
# 移动端链接格式：https://m.weibo.cn/{uid}/{mid}

detail_base_url = 'https://weibo.com/ajax/statuses/show?id=' # mblogid或mid均可

def parse_weibo_m_url(url, weibo_cookies=None):
    mid = url.split('/')[-1]
    uid = url.split('/')[-2]
    web_url = 'https://weibo.com/{}/{}'.format(uid, mid)
    return parse_weibo_url(web_url, weibo_cookies)


def parse_weibo_url(url, weibo_cookies=None):
    mid = url.split('/')[-1]
    uid = url.split('/')[-2]
    mblogid = ''
    detail_url = detail_base_url + mid
    res = httpx.get(detail_url)
    detail_json = res.json()
    pics = []
    video_url = ''
    res = httpx.get(detail_url)
    detail_json = res.json()
    pics = []
    video_url = ''
    long_content = None
    if detail_json['ok'] == 1:
        mblogid = detail_json['mblogid']
        if 'pic_infos' in detail_json:
            for pic_info in detail_json['pic_infos'].values():
                pics.append(pic_info['large']['url'])
        if 'page_info' in detail_json and 'media_info' in detail_json['page_info']:
            video_url = detail_json['page_info']['media_info']['h5_url']
        if 'continue_tag' in detail_json and weibo_cookies != None:
            expand_res = httpx.get('https://weibo.com/ajax/statuses/longtext?id=' + mid, headers={'Cookie': weibo_cookies})
            expand_json = expand_res.json()
            if expand_json['ok'] == 1:
                long_content = expand_json['data']['longTextContent']
        content = long_content if long_content != None else detail_json['text_raw']
        return {
            'url': f'https://weibo.com/{uid}/{mblogid}',
            'murl': f'https://m.weibo.cn/{uid}/{mid}',
            'title': content.split('\n')[0],
            'author': detail_json['user']['screen_name'],
            'head': detail_json['user']['profile_image_url'],
            'content': content,
            'pics': pics,
            'video_url': video_url
        }
    else:
        return None

if __name__ == '__main__':
    print(parse_weibo_url('https://weibo.com/6303705511/LC4ECDFJC'))
    # print(parse_weibo_url('https://m.weibo.cn/5147521764/4794734364590178'))
