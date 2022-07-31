from pyquery import PyQuery as pq

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def parse_group_topic_url(url):
    doc = pq(url, headers=header)
    imgs = doc('.topic-doc img').items()
    pics = []
    for i in imgs:
        pics.append(i.attr('src'))
    return {
        'url': url,
        'title': doc('.article h1').text(),
        'content': doc('.topic-doc p').text(),
        'time': doc('span.create-time').text(),
        'author': doc('span.from').text(),
        'author_pfp': doc('img.pil').attr('src'),
        'pics': pics
    }

if __name__ == '__main__':
    print(parse_group_topic_url('https://www.douban.com/group/topic/271430038/'))
