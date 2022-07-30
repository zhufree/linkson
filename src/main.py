from linkson import parse_url
from config import weibo_cookies

if __name__ == '__main__':
    print(parse_url('https://weibo.com/5147521764/LDKtmjg78', weibo_cookies=weibo_cookies))
    # print(parse_url('https://m.weibo.cn/5147521764/4794734364590178', weibo_cookies=weibo_cookies))