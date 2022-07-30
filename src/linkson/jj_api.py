from pyquery import PyQuery as pq
import requests

def parse_jjwxc_url(url):
    res = requests.get(url)
    res.encoding = 'gb2312'
    doc = pq(res.text)
    title = doc('span[itemprop=articleSection]').text()
    # title_en = translator.translate(title).text
    author = doc('span[itemprop=author]').text()
    # author_en = translator.translate(author).text
    status = doc('span[itemprop=updataStatus]').text()
    # status_en = translator.translate(status).text
    wordCount = doc('span[itemprop=wordCount]').text()
    collectedCount = doc('span[itemprop=collectedCount]').text()
    summary = doc('div[itemprop=description]').text().replace('~', '').replace('||', '|')
    # summary_en = translator.translate(summary).text.replace('~', '').replace('||', '|')
    tags = doc('div.smallreadbody>span>a').text().replace(' ', '/')
    cover = doc('img.noveldefaultimage').attr('src')
    # tags_en = translator.translate(tags).text
    return {
        # 'title': '{}({})'.format(title, title_en),
        # 'author': '{}({})'.format(author, author_en),
        # 'status': '{}/{}'.format(status, status_en),
        'title': title,
        'author': author,
        'status': status,
        'other_info': 'word count:{}\ncollected count: {}'.format(wordCount.replace('字', 'chars'), collectedCount),
        'tags': tags,
        'summary': summary,
        'cover': cover
    }

def get_novel_info(id):
    url = f'http://www.jjwxc.net/onebook.php?novelid={id}'
    req = requests.get(url)
    req.encoding = 'gb2312'  # 显示指定网页编码
    body = pq(req.text)
    novel_info = {}

    novel_info['authorName'] = body('span[itemprop=author]').text()
    novel_info['authorUrl'] = f'http://www.jjwxc.net/oneauthor.php?authorid={body("#authorid_").text()}'
    novel_info['bookUrl'] = url
    novel_info['url'] = url
    novel_info['title'] = body('span[itemprop=articleSection]').text()
    novel_info['type'] = body('span[itemprop=genre]').text()
    novel_info['style'] = body('ul.rightul li:nth-child(3)').text()[5:]
    novel_info['status'] = body('span[itemprop=updataStatus]').text()
    novel_info['collectionCount'] = body('span[itemprop=collectedCount]').text()
    novel_info['wordcount'] = body('span[itemprop=wordCount]').text()[:-1]
    novel_info['cover'] = body('img.noveldefaultimage').attr('src')
    novel_info['searchKeyword'] = body('div.smallreadbody span.bluetext').text()
    if '完' in novel_info['status']:
        novel_info['status'] = '完结'
    elif novel_info['status'] == '暂停':
        novel_info['status'] = '断更'
    elif novel_info['status'] == '连载中':
        novel_info['status'] = '连载'
    novel_info['bid'] = 'jj' + novel_info['bookUrl'].split('=')[-1]
    novel_info['aid'] = 'jj' + novel_info['authorUrl'].split('=')[-1]
            
    # handle tag
    tag_items = list(body('div.smallreadbody a').items())
    tag_name_list = [i.text() for i in tag_items]
    tag_href_list = [i.attr('href') for i in tag_items]
    tag_dict = {
        tag_name_list[i]: tag_href_list[i] for i in range(len(tag_name_list))
    }
    tag_remove_list = []
    for i in tag_dict.keys():
        if '?bq=' not in tag_dict[i] or len(i) > 4:
            tag_remove_list.append(i)
    for i in tag_remove_list:
        tag_dict.pop(i)
    novel_info['tags'] = [i.strip() for i in tag_dict.keys() if len(i.strip()) > 0]
    return novel_info

def get_novel_update_status(nid):
    """
    获取book状态
    :param bid: bookid
    :return: 0: 连载中 1: 已完结 2: 不存在 dict: {}
    """
    url = f'http://www.jjwxc.net/onebook.php?novelid={nid}'
    req = requests.get(url)
    req.encoding = 'gb2312'  # 显示指定网页编码
    body = pq(req.text)

    # 判定是否完结 span itemprop="updataStatus"
    status = 2
    title = body('title').text()
    spans = body('span').items()
    oneboolt = body('table#oneboolt')
    table = None
    if len(list(oneboolt.items())) == 0:
        status = 2
    else:
        table = list(oneboolt.items())[0]
    for s in spans:
        if s.attr('itemprop') == 'updataStatus':
            if '连载' in s.text():
                status = 0
            else:
                status = 1

    if table:
        trs = list(table('tr').items())
        last_chapter_tr = trs[-2]
        tds = list(last_chapter_tr('td').items())
        # print(last_chapter_tr.html())
        if tds[0].text() == "章节":
            return {'status': status,
                            'chapter_id': 0,
                            'chapter_title': "尚未开始连载",
                            'chapter_desc': "尚未开始连载",
                            'title': title}
        else:
            chapter_id = int(tds[0].text())
            chapter_title = tds[1].text().strip()
            chapter_desc = tds[2].text()
            return {'status': status,
            'chapter_id': chapter_id,
                            'chapter_title': chapter_title,
                            'chapter_desc': chapter_desc,
                            'title': title}
    else:
        return status, None

if __name__ == '__main__':
    print(get_novel_info('4947430'))
    print(parse_jjwxc_url('https://www.jjwxc.net/onebook.php?novelid=4472787'))
