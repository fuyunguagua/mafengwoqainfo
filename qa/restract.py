
__author__ = 'WY'

import re
from scrapy.selector import Selector
def filter_text2(text,flags):
    for item in flags:
        if text.find(item) is -1:
            pass
        else:
            text =  text.replace(item,' ')
    return text

def restract(regex, text, func=None):
    pattern = re.compile(regex,re.S)
    r = pattern.findall(text)
    if func is None:
        return r
    else:
        if callable(func):
            func(r)
        else:
            raise Exception('参数三不可被调用')

def showResult(list):
    for i, item in enumerate(list):
        print(i,item)

def restract_question_title(htmlText):
    question_title_re = '<h1>(.*?)</h1>'
    return restract(question_title_re, htmlText)[0].strip()


def restract_address(htmlText):
    address_re = 'class="location"><i></i>(.*?)</a>'
    return restract(address_re, htmlText)[0]


def restract_question_detail(htmlText):
    seletor = Selector(text=htmlText)
    result = seletor.xpath('//*[@id="_js_askDetail"]/div[1]/div[2]/text()').extract()
    return ''.join(result)


def restract_lables_list(htmlText):
    seletor = Selector(text=htmlText)
    result = seletor.xpath('//*[@id="_js_askDetail"]/div[1]/div[3]/div[1]').extract_first()
    res = '<a class.*?>(.*?)</a>'
    return restract(res, result)


def restract_answer_list(htmlText):
    seletor = Selector(text=htmlText)
    result = seletor.xpath('//*[@id="normal_answer_wrap"]/li').extract()
    return result


def restract_one_answer(anwer_div):
    # 获得纯文本
    anwer_text_re = '<div class="_j_answer_html">(.*)</div>\s*<!-- 问答版权名片 -->'
    anwer_text = restract(anwer_text_re, anwer_div)[0]
    img_re = '<img src.*?>'
    result = re.sub(img_re, '', anwer_text, flags=re.S)
    address_re = '<div class="area_tags _j_tip_mdd".*?<a.*?>.*?</a>\s*<div class="at_info.*?></div>\s*?</div>'
    result = result.replace('{','《')
    result = result.replace('}','》')
    address_pass_text = re.sub(address_re, '{}', result, flags=re.S)
    address_key_re = '<a data-cs-p="qa_mdd".*?>(.*?)</a>'
    address_list = restract(address_key_re, anwer_text)
    result = address_pass_text.format(*address_list)
    # 清洗特殊字符
    answer_text = clean_text(result)
    # 获得赞数
    num_zan = restract_num_zan(anwer_div)

    return [num_zan, answer_text]


def clean_text(result):
    filter_re = '<span.*?</span>'
    result = re.sub(filter_re, '', result, flags=re.S)
    filter_re = '<div.*?</div>'
    result = re.sub(filter_re, '', result, flags=re.S)
    filter_re = '<div.*?>'
    result = re.sub(filter_re, '', result, flags=re.S)
    filter_re = '<a.*?</a>'
    result = re.sub(filter_re, '', result, flags=re.S)
    result = filter_text2(result, ('<br>', '<b>', '</b>', '</div>', '\n'))
    filter_re = '图自.*? '
    answer_text = re.sub(filter_re, '', result, flags=re.S)
    return answer_text


def restract_num_zan(answer_div):
    num_vote_re = '<a class="btn-ding _js_zan.*?data-real_num="(\d*?)"'
    return restract(num_vote_re, answer_div)[0]


class Restractor(object):
    @staticmethod
    def restract_qa_info(html):
        info = {}
        info['title'] = restract_question_title(html)
        info['detail'] = restract_question_detail(html)
        info['location'] = restract_address(html)
        info['lables'] = restract_lables_list(html)
        answer_list = []
        answer_div_list = restract_answer_list(html)
        for answer_div in answer_div_list:
            answer_list.append(restract_one_answer(answer_div))
        info['answer'] = answer_list
        return info


