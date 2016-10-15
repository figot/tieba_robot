# coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
import json
import sys
# import login
import tuling_api
import huitie
import time

reload(sys)
sys.setdefaultencoding('utf-8')

while True:
    r = requests.get("http://tieba.baidu.com/f?kw=华中科技大学&fr=index")
    # print (r.text)
    page = BeautifulSoup(r.text, "html.parser")

    li_list = page.find_all('li', attrs={'class': re.compile("( j_thread_list clearfix)")})

    # tag块去掉无用部分
    before = "'>\n"
    after = "data-field='"
    title_before = '">'
    title_after = 'title="'
    for t_list in li_list:
        a = str(t_list)
        a = a[:a.index(before)]
        t_json = a[a.index(after) + len(after):]
        # 写入json
        t_id = json.loads(t_json)
        author_name = t_id["author_name"]
        id = t_id["id"]
        reply_num = t_id["reply_num"]
        # print t_id

        # if author_name == "华科大粽子" and reply_num == 0:
        #    print "华科大粽子",
        #    print id
        if reply_num == 0:
            # author_name == "我叫红领巾800":
            # print "我叫红领巾800",
            print '贴号:' + str(id) + ',' + str(reply_num)
            # login.post()
            # 把标题扣出来,又得来一遍
            title_match = "/p/" + str(id)
            # print title_match
            title = page.find_all('a', attrs={'href': re.compile(title_match)})
            # 只有一个元素的数组
            title = str(title[0])
            title = title[:title.index(title_before)]
            title = title[title.index(title_after) + len(title_after):]
            print '<' + title
            t_text = tuling_api.post_text(title)
            print '>' + t_text
            huitie.reply(t_text, id)
            time.sleep(3)

            # print content
            # if reply_num == 0:
            #    print "reply_0",
            #    print id
    i = 1
    i = i + 1

    if i == 10:
        break
    time.sleep(30)