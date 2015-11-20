#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import os
import collections
from bosonnlp import BosonNLP
import urllib2, urllib


def loadFolder(data_folder, words_to_extract):
    return

def convert(data):
    if isinstance(data, basestring):
        print(data)
        return data
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

    
# Sensitivity (1 - 5) gives balance of Type 1 and Type 2 error.
# 1 Finds more entities, 5 is more accuracy on found entity
def bosonNer(text, sensitivity):
    nlp = BosonNLP('O8M_j1Nd.4200.wIlhsL46w9-C')
    return nlp.ner(text, sensitivity)

def ltpGet(text):
    url_get_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = '056101h4HiqDWAVesOgY6EdXmRLWRkIfmRxbweav'
    format = 'json'
    pattern = ''
    text = urllib.quote(text)
    result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
    content = result.read().strip()
    print(content)

def main():
    text = '''辽宁 纪检监察 机关 公布 一批 大要案 　         鞍山 市委 原副 书记 张文效 倒卖 股票 认购证 被 开除党籍 
 
 1995.02 . 24 
 
 
 
           本报讯     笔者 从 中纪委 、 监察部 获悉 ： 辽宁省 反腐败 斗争 和 查处 大要案 工作 又 取得 新 成果 。 近日 ， 辽宁省 纪委 和 省 监察厅 公布 了 一批 大要案 的 查处 情况 。 
 
           中共 鞍山 市委 原副 书记 张文效 于 1992 年 5 月 至 1993 年 3 月 ， 为 谋取私利 ， 利用职权 ， 向 他人 索要 股票 认购证 70 张 （ 交款 200 元 ） ， 其中 由 本人 和 亲属 高价 倒卖 46 张 ， 共 非法所得 12 · 4 万元 ； 由 他人 利用 报废 的 居民身份证 ， 为 其 购买 内部 职工 股票 进行 倒卖 ， 获 不 正当 收入 7 · 2 万元 。 张文效 为 隐瞒 高价 倒卖 股票 认购证 及 内部 职工 股票 问题 ， 在 组织 调查 期间 ， 订立 攻守同盟 ， 编造 伪证 ， 欺骗 组织 。 经 省委 决定 ， 给予 张文效 开除党籍 处分 ， 非法所得 及 不 正当 收入 19 · 6 万元 ， 收缴 归公 。 
 
           昌图县 人大常委会 主任 、 党组书记 娄登亚 ， 在 任 昌图 县委书记 期间 ， 对 该县 特大 倒卖 粮食 资材 和 原 粮食 局长 桂秉权 （ 已 被 处决 ） 贪污受贿 等 严重 违法犯罪 活动 长期 失察 、 负有 重要 领导 责任 ， 犯有 严重 官僚主义 失职 错误 。 省委 决定 撤销 娄登亚县 人大常委会 党组书记 职务 ， 建议 依法罢免 其 昌图县 人大常委会 主任 职务 。 
 
           铁岭市 政府 副 秘书长 杨 国民 ， 在 任 昌图县 县长 期间 ， 对 本县 粮食 系统 资材 严重 超储 、 超亏 ， 没有 采取有效 措施 加以解决 。 杨 还 利用职权 多次 为 亲属 和 关系人 给 县 粮食 局长 桂秉权 等 人 写 倒卖 粮食 资材 的 条子 ， 起到 了 支持 倒卖 粮食 资材 的 违法违纪 活动 作用 ， 经 铁岭 市委 决定 给予 杨 国民 撤职处分 。 
 
           在 公布 的 大要案 中 ， 还有 丹东市 旅游局 局长 郜福东 受贿案 、 北镇 满族 自治县 副县长 刘景宇 受贿案 、 抚顺市 抚东 钢厂 厂长 赵玉顺 受贿案 ， 上述 三 人均 受到 开除党籍 和 撤职处分 ， 并 将 被 追究 刑事责任 。 
 
           中共 辽宁省 纪委 副 书记 王文谦 还 披露 ， 去年 ， 全省 纪检监察 机关 共 立案查处 各类 违法违纪 案件 7101 件 ， 处分 党员干部 5593 人 ， 其中 县 、 处级 以上 干部 315 人 ， 有力 地 保护 了 改革开放 和 经济 建设 的 顺利进行 。     （ 钟吉闻 ） 
 
           《 人民日报 》         〔 19950224 № Ｃ 〕 
 
'''
    # outputList = bosonNer(text, sensitivity = 3)
    # for item in outputList:
    #     print(type(item))
    #     if type(item) == dict:
    #         for key2, value2 in item.iteritems():
    #             print(key2)
    #             for x in value2:
    #                 print(x)
    #     else:
    #         print(item)
    ltpGet(text)


    # 1. Load datasets
    # 2. word segmentation
    # 3. word embedding
    # 4. (optional) syntactic parsing
    # 5. name correspondence
    # 6. evaluation
    # foldername = ""
    # allfiles = loadFolder(folder)

    # segmented = segmentation(allfiles)

    # embedded = embedding(segmented)

    # # Syntactic parsing omitted

    # correspondence = summarize(embedded)

    # for name, crime, amount in enumerate(correspondence):
    #     print "NAME:", name, "CRIME:", crime, "AMOUNT", amount

    # evaluate(correspondence)


if __name__ == "__main__":
    main()
    #cProfile.run('main()') # if you want to do some profiling