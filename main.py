from city import get_province_city
city_list = get_province_city()
city_list.append('中国')
filt_list = ['ns','nis']
from pyhanlp import *

class KeyWord:

    def is_english_char(self,ch):
        if ord(ch) not in (97, 122) and ord(ch) not in (65, 90):
            return False
        return True

    def process_word(self,word):

        res = word.replace('《', '').replace('》', '')
        index1 = res.find('（')
        index2 = res.find('）')
        temp = res[index1:index2 + 1]
        res = res.replace(temp, '')
        flag1 = res[:2]
        flag2 = res[:3]
        flag3 = res[:4]
        if flag3 in city_list:
            res = res.replace(flag3, '')
        elif flag2 in city_list:
            res = res.replace(flag2, '')
        elif flag1 in city_list:
            res = res.replace(flag1, '')

        return res

    def extract(self,name):

        if self.is_english_char(name[0]):
            final_key = name[0]
            return final_key

        final_key = False
        name_type_dict = dict()
        #print(name)
        name = self.process_word(name)
        words = [_.toString() for _ in HanLP.segment(name)]
        filt_key = list()
        key_list = list()
        for word in words:
            key, flag = word.split('/')
            name_type_dict[key] = flag
            key_list.append(key)
            if flag in filt_list:
                filt_key.append(key)

        #print(words)
        for i in filt_key:
            key_list.remove(i)

        #print(key_list)

        if len(key_list) == 1: # 只有一个单词，看其长度是否<=4
            if len(key_list[0]) <= 4:
                final_key = key_list[0]
            else:
                final_key = self.extract_two(key_list[0])


        # 当只有两个词语的时候

        elif len(key_list) == 2:

            # 是英文，则用该英文作为返回值
            k1 = key_list[0]
            if name_type_dict[k1] == 'nx':
                final_key = k1
            # 如果第一个不是英文
            else:

                k2 = key_list[1]

                if len(k1) == 1:
                    if len(k2) == 1:
                        final_key = k1 + k2 # 两个单字，只能相加。
                    elif len(k2) == 2:
                        final_key = k1 + k2 # 三个字，ok
                    elif len(k2) == 3:
                        final_key = k1 + k2 # 四个字也ok
                    else:
                        temp = k1 + k2
                        final_key = temp[:4]

                elif len(k1) == 2:
                    if len(k2) == 1 or len(k2)==2:
                        final_key = k1 + k2
                    else:
                        temp = k1 + k2
                        final_key = temp[:4]

                # 如果第一个值长度为3,则最后的词长度为3or4.
                elif len(k1) == 3:
                    if len(k2) ==1:
                        final_key = k1 + k2
                    else:
                        if 'n' in name_type_dict[k1] :
                            final_key = k1

                        else:
                            final_key = k1 + k2[0]

                elif len(k1) == 4:
                    final_key = k1 # 长度为四，则直接使用k1
                else:
                    final_key = self.extract_two(k1)


        # 当候选词大于3个。
        else:
            if not key_list: # 没有候选词
                pass
            else:
                k1 = key_list[0]
                if name_type_dict[k1] == 'nx':
                    final_key = k1

                else:
                    k2 = key_list[1]
                    k3 = key_list[2]



                    if len(k1) == 1: # 如果第一个单词长度为1.则最终结果为3或者4.
                        if len(k2) == 1:
                            if len(k3) ==1 or len(k3)==2:
                                # 当第三个为1或者2，最终长度为3或者4
                                final_key = k1 + k2 + k3
                            else: # 最终长度为4
                                final_key = k1 + k2 + k3[:2]

                        elif len(k2) == 2:
                            if len(k3) >= 2:
                                final_key = k1 + k2
                            else:
                                final_key = k1 + k2 + k3
                        elif len(k2) == 3:
                            final_key = k1 + k2

                    elif len(k1) == 2: # 第一个单词长度为2
                        if len(k2) == 1:
                            if len(k3) == 1:
                                final_key = k1 + k2 + k3
                            else:
                                final_key = k1 + k2

                        elif len(k2) == 2:
                            final_key = k1 + k2
                        else:
                            temp = k1 + k2
                            final_key = temp[:4]
                    elif len(k1) == 3:
                        if 'n' in name_type_dict[k1] :
                            final_key = k1
                        else:
                            if len(k2) == 1:
                                final_key = k1 + k2
                            else:
                                final_key = k1 + k2[0]
                    elif len(k1) == 4:
                        final_key = k1
                    else:
                        final_key = self.extract_two(k1)

        if not final_key or len(final_key)==1:
            for item in name_type_dict.keys():
                final_key = item
                break

       #print(final_key)
        return final_key

    def extract_two(self,name):

        final_key = False
        name_type_dict = dict()
        name = self.process_word(name)
        words = [_.toString() for _ in HanLP.segment(name)]
        filt_key = list()
        key_list = list()
        for word in words:
            key, flag = word.split('/')
            name_type_dict[key] = flag
            key_list.append(key)
            if flag in filt_list:
                filt_key.append(key)

        for i in filt_key:
            key_list.remove(i)


        if len(key_list) == 1:
            if len(key_list[0]) <= 4:
                final_key = key_list[0]
            else:
                final_key = key_list[0][:4]



        # 当只有两个词语的时候

        elif len(key_list) == 2:

            # 是英文，则用该英文作为返回值
            k1 = key_list[0]
            if name_type_dict[k1] == 'nx':
                final_key = k1
            # 如果第一个不是英文
            else:

                k2 = key_list[1]

                if len(k1) == 1:
                    if len(k2) == 1:
                        final_key = k1 + k2 # 两个单字，只能相加。
                    elif len(k2) == 2:
                        final_key = k1 + k2 # 三个字，ok
                    elif len(k2) == 3:
                        final_key = k1 + k2 # 四个字也ok
                    else:
                        temp = k1 + k2
                        final_key = temp[:4]

                elif len(k1) == 2:
                    if len(k2) == 1 or len(k2)==2:
                        final_key = k1 + k2
                    else:
                        temp = k1 + k2
                        final_key = temp[:4]

                # 如果第一个值长度为3,则最后的词长度为3or4.
                elif len(k1) == 3:
                    if len(k2) ==1:
                        final_key = k1 + k2
                    else:
                        if 'n' in name_type_dict[k1] or 'l' in name_type_dict[k1] :
                            final_key = k1

                        else:
                            final_key = k1 + k2[0]

                elif len(k1) == 4:
                    final_key = k1 # 长度为四，则直接使用k1
                else:
                    final_key = self.extract_two(k1)


        # 当候选词大于3个。
        else:
            if not key_list: # 没有候选词
                pass
            else:
                k1 = key_list[0]
                if name_type_dict[k1] == 'nx':
                    final_key = k1

                else:
                    k2 = key_list[1]
                    k3 = key_list[2]



                    if len(k1) == 1: # 如果第一个单词长度为1.则最终结果为3或者4.
                        if len(k2) == 1:
                            if len(k3) ==1 or len(k3)==2:
                                # 当第三个为1或者2，最终长度为3或者4
                                final_key = k1 + k2 + k3
                            else: # 最终长度为4
                                final_key = k1 + k2 + k3[:2]

                        elif len(k2) == 2:
                            if len(k3) >= 2:
                                final_key = k1 + k2
                            else:
                                final_key = k1 + k2 + k3
                        elif len(k2) == 3:
                            final_key = k1 + k2

                    elif len(k1) == 2: # 第一个单词长度为2
                        if len(k2) == 1:
                            if len(k3) == 1:
                                final_key = k1 + k2 + k3
                            else:
                                final_key = k1 + k2

                        elif len(k2) == 2:
                            final_key = k1 + k2
                        else:
                            temp = k1 + k2
                            final_key = temp[:4]
                    elif len(k1) == 3:
                        if 'n' in name_type_dict[k1] :
                            final_key = k1
                        else:
                            if len(k2) == 1:
                                final_key = k1 + k2
                            else:
                                final_key = k1 + k2[0]
                    elif len(k1) == 4:
                        final_key = k1
                    else:
                        final_key = self.extract_two(k1)
        if not final_key:
            for item in name_type_dict.keys():
                final_key = item
                break
        return final_key

if __name__=='__main__':
    my_keyword =  KeyWord()
    word = my_keyword.extract('成都锤子科技有限公司')
    print(word)