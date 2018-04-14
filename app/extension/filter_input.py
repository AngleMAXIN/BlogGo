#/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

class TextData(object):

    """检验输入类"""
    def __init__(self, dict_data=dict()):

        self.str_dict = dict_data

    @property
    def test_email(self):

        """对用户输入的数据进行检验"""

        pattern = r'[0-9a-z]{0,12}@[0-9a-z]{2,10}.com'
        if re.match(pattern, self.str_dict['email']):
            return True
        else:
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

class Testlogin(object):
    """检查登录的数据合法性"""
    def __init__(self, dict_data=dict()):
        self.str_dict = dict_data

    def test_password(self):
        pass

    @property
    def test_input_text(self,):
        """判断输入的是邮箱还是用户名,如果是邮箱就返回False，反则，返回True"""
        pattern = r'@'
        if re.search(pattern, self.str_dict['input_text']):
            return False
        else:
            return True



