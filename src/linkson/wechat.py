from pyquery import PyQuery as pq

def parse_wechat_url(url):
    doc = pq(url)
    author = doc('#profileBt > a').text()
    head = list(doc('img').items())[1].attr('data-src')
    img = doc('img.rich_pages:first').attr('data-src')
    title = doc('#activity-name').text()
    content = doc('#js_content').text().replace('\n\n\n', '\n').strip()[0:500]+'...'
    return {
        'title': title,
        'author': author,
        'head': head,
        'img': img,
        'content': content
    }

if __name__ == '__main__':
    print(parse_wechat_url('https://mp.weixin.qq.com/s/YwHhX-A8tRJ37RCNHqLxdQ '))