#/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

class TextData(object):

    """检验输入类"""
    def __init__(self, dict_data):

        self.str_dict = dict_data
        # self.email = False
        # self.name = False
        # self.password = False
    # def test(self):
    #
    #     """汇总检验数据，如果全都合法返回True"""
    #
    #     if self._test_name():
    #         self.name = True
    #     elif self._test_name():
    #         self.email = True
    #     elif self._test_password():
    #         self.password = True
    #
    #     if self.password and self.email and self.password:
    #         return True

    @property
    def test_email(self):

        """对用户输入的数据进行检验"""

        pattern = r'[0-9a-z]{0,12}@[0-9a-z]{2,10}.com'
        if re.match(pattern, self.str_dict['email']):
            return True
        else:`
            return False

    @property
    def test_name(self):

        """对用户名的检验"""
        if len(self.str_dict['username']) > 15:
            return False

        pattern = r'\d+|\W|_'
        if re.search(pattern, self.str_dict['username']):
            return False
        else:
            return True

    @property
    def test_password(self):

        """对注册密码的检验"""

        if len(self.str_dict['password']) > 15:
            return False

        pattern = r'^\s|\s'
        if re.match(pattern, self.str_dict['password']):
            return False
        else:
            return True


    def test_input_text(self,input_text):

        """判断输入的是邮箱还是用户名"""

        pattern = r'@'
        if re.search(pattern, input_text):
            return False
        else:
            return True



