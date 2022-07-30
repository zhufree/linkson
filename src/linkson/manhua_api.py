from pyquery import PyQuery as pq
from helium import *
import time, httpx
'''
bili pc:
    detail: https://manga.bilibili.com/detail/mc28609
    single: https://manga.bilibili.com/mc28609/497005
bili mobile: https://b22.top/pyHVjTW 跳转到pc链接
'''
test_kuaikan_url = 'https://www.kuaikanmanhua.com/web/topic/9204/?Source=6&TimeStamp=2022-01-08%2B13%253A39%253A52%253A912'
test_bili_url = 'https://manga.bilibili.com/detail/mc27287'
test_bili_url = 'https://b22.top/hjAOgQa'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 '
                  'Safari/537.36'
    }
current_bili_url = ''

#用selenium访问url
def selenium_opener(url):
    global current_bili_url
    driver = start_chrome(url, headless=True)
    # 等待元素加载完成
    wait_until(Text("章节列表").exists)
    current_bili_url = driver.current_url
    html = driver.page_source
    driver.quit()
    return html

def get_manhua_detail(manhua_url):
    if manhua_url.startswith('https://www.kuaikanmanhua.com/'):
        return handle_kuaikan(manhua_url)
    elif manhua_url.startswith('https://manga.bilibili.com/') or manhua_url.startswith('https://b22.top/'):
        return handle_bilibili(manhua_url)
    else:
        pass
    return {
        'success': False,
        'error': '不支持的url格式'
    }


def bili_api(mId):
    url = 'https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device=pc&platform=web'
    data = {
        'comic_id': mId[2:]
    }
    res = httpx.post(url, data=data)
    res_json = res.json()
    if res_json['code'] == 0:
        manhua = res_json['data']
        return {
            'success': True,
            'data':{
                'name': manhua['title'],
                'intro': manhua['classic_lines'],
                'authorName': '/'.join(manhua['author_name']),
                'cover': manhua['vertical_cover'],
                'platforms': [9],
                'url': 'https://manga.bilibili.com/detail/' + mId,
                'mId': mId
            }
        }
    else:
        return {
            'success': False,
            'error': 'url解析出错'
        }

def handle_bilibili(url):
    global current_bili_url
    if 'detail' in url:
        mId = url.split('/')[-1]
        return bili_api(mId)
    elif 'b22.top' not in url:
        mId = url.split('/')[-2]
        return bili_api(mId)
    elif 'b22.top' in url:
        doc = pq(url, opener=selenium_opener)
        if doc is not None:
            title = doc('.manga-info h1.manga-title').text()
            intro = doc('.introduction-text').text()
            author_name = doc('h2.author-name').text().replace('，', '/')
            cover = doc('.header-info .manga-cover > img').attr('src').split('@')[0]
            return {
                'success': True,
                'data':{
                    'name': title,
                    'intro': intro,
                    'authorName': author_name,
                    'cover': cover,
                    'platforms': [9],
                    'url': current_bili_url,
                    'mId': current_bili_url.split('/')[-1]
                }
            }
    else:
        return {
            'success': False,
            'error': 'url解析出错'
        }


def handle_kuaikan(url):
    doc = pq(url)
    url_parts = url.split('?')
    if len(url_parts) > 1:
        url = url_parts[0]
    if doc is not None:
        title = doc('.TopicList .TopicHeader .title').text()
        intro = doc('.detailsBox').text()
        author_name = doc('.TopicList .TopicHeader .nickname').text()
        cover = doc('.TopicList .TopicHeader .left .img').attr('src')
        return {
            'success': True,
            'data':{
                'name': title,
                'intro': intro,
                'authorName': author_name,
                'cover': cover,
                'platforms': [10],
                'url': url,
                'mId': 'kk' + url.split('/')[-2]
            }
        }
    else:
        return {
            'success': False,
            'error': 'url解析出错'
        }


if __name__ == '__main__':
    # print(handle_kuaikan(test_kuaikan_url))
    print(handle_bilibili(test_bili_url))