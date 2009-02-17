#!/usr/bin/python
# -*- coding: utf-8 -*-
import string
import re
import gzip
import sys
from struct import *

class dict(object):
    def __init__(self, options):
        print 'From StarDict'
        print '============'
        name = options['dict_data']
        p = sys.path[0] + '/'
        files = {
                'inf_file': p + name + '/' + name + '.ifo',
                'idx_file': p + name + '/' + name + '.idx',
                'dic_file': p + name + '/' + name + '.dict'
                }
        self.engine = stardict_engine(files)
    def get_result(self, word):
        self.result = {}
        cords = self.engine.search_idx(word)
        data  = self.engine.search_word(cords)
        test  = data.split('\x00')
        self.result['word'] = word
        self.result['pron'] = test[0]
        del test[0]
        self.result['def']  = test
        return self.result

class stardict_engine(object):
    def __init__(self, options):
        self.options = options
        self.setup_info()
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
    def search_word(self, cords):
        try:
            self.dic_file = open(self.options['dic_file'], 'rb')
        except IOError:
            try:
                self.dic_file = gzip.open(self.options['dic_file'] + '.dz', 'rb')
            except IOError:
                print 'wrong'
        self.dic_file.seek(cords[0])
        bytes = self.dic_file.read(cords[1])
        return bytes

    def search_idx(self, search_word):
        f = open(self.options['idx_file'], 'rb')
        self.idx_file = f.read()
        # offset 
        if self.dict_info.has_key('idxoffsetbits'):
            idx_offset_bytes_size = self.dict_info['idxoffsetbits']/8
        else:
            idx_offset_bytes_size = 4
        idx_format = {4: 'L', 8: 'Q'}[idx_offset_bytes_size]
        # word data size
        idx_offset_bytes_size = idx_offset_bytes_size + 4
        record_regex = r'([\d\D]+?\x00[\d\D]{%s})' % idx_offset_bytes_size
        matched_records = re.findall(record_regex, self.idx_file)

        word_list = {}
        for record in matched_records:
            c = record.find('\x00') + 1
            record_tuple = unpack('!%sc%sL' % (c, idx_format), record)
            word  = record_tuple[0:c-1]
            cords = record_tuple[c:]
            word_list[''.join(word)] = cords
        return word_list[search_word]
