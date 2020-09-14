#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlrd


def get_province_city():
    xls_path = './tools/city.xls'
    print(xls_path)
    book = xlrd.open_workbook(xls_path)
    sheet = book.sheets()[0]
    name_ = list()
    for r in range(1, sheet.nrows):
        # code = sheet.cell(r, 0).value
        name = sheet.cell(r, 1).value
        temp = get_keyword(name)
        if temp:

            name_.append(temp[0])
            name_.append(temp[1])


    return name_

def get_keyword(word):
    if '省' in word:
        temp = word.replace('省','')
        return word,temp
    elif '市' in word:
        temp = word.replace('市','')
        return word,temp
    else:
        return None


def get_keyword_two(word):
    if '自治区' in word:
        word = word.replace('自治区', '')
        return word
    if '自治县' in word:
        word = word.replace('自治县', '')
        return word
    if '县' in word:
        if len(word) > 2:
            word = word.replace('县', '')
            return word
        else:
            return word
    if '区' in word:
        if len(word) > 2:
            word = word.replace('区', '')
            return word
        else:
            return word
    if '市' in word:
        if len(word) > 2:
            word = word.replace('市', '')
            return word
        else:
            return word
    if '省' in word:
        word = word.replace('省', '')
        return word
    if '旗' in word:
        word = word.replace('旗', '')
        return word
    else:
        return None

