#!/usr/bin/python
# -*- coding: utf-8 -*-
import string

class dict(object):
    def __init__(self, options):
        name = options['dict_data']
        files = {
            'inf_file': name + '/' + name + '.ifo',
            'idx_file': name + '/' + name + '.idx',
            'dic_file': name + '/' + name + '.dic'
        }
        self.engine = stardict_engine(files)
    def get_result(self, word):
		self.result = {}
		self.result['word'] = word
		self.result['pron'] = 'sdfj'
		self.result['def']  = ['test']
		return self.result

class stardict_engine(object):
    def __init__(self, options):
        self.options = options
        self.setup_info()
        self.search_idx('test')
    def setup_info(self):
        f = self.options['inf_file']
        f = open(f, 'r')
        # ignore the first line
        f.readline()
        self.dict_info = {}
        for line in f:
            tmp = string.split(line, '=')
            tmp[1].strip()
            self.dict_info[str(tmp[0])] = str(tmp[1].strip())
        return self.dict_info
    def search_idx(self, word):
        f = open(self.options['idx_file'], 'rb')
        f.read()
        print f.tell()



