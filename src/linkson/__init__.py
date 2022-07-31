import re
from .weibo import *
from .douban import *

def parse_url(raw_url, **kwargs):
    if 'weibo' in raw_url:
        url = re.split(r'[?#]', raw_url)[0]
        if url.startswith('https://weibo.com/'):
            return parse_weibo_url(url, **kwargs)
        elif url.startswith('https://m.weibo.cn/'):
            return parse_weibo_m_url(url, **kwargs)
        else:
            return {
                'success': False,
                'msg': '暂不支持的链接'
            }
    elif 'douban' in raw_url:
        url = re.split(r'[?#]', raw_url)[0]
        if url.startswith('https://www.douban.com/group/topic'):
            return parse_group_topic_url(url, **kwargs)
        else:
            return {
                'success': False,
                'msg': '暂不支持的链接'
            }
    else:
        return {
            'success': False,
            'msg': '暂不支持的链接'
        }