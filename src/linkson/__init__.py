import re
from .weibo import *
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