#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import codecs
import re
import xml.dom.minidom

class dict(object):
    def __init__(self, options):
        self.result = {}
        self.name = 'Dict.CN'
        self.url = 'http://dict.cn/ws.php'
        self.values = {
            'q': '',
            'utf8':'true'
        }
        print 'From Dict.CN'
        print '============'
    def get_origin(self, word):
        self.values['q'] = word;
        self.data = urllib.urlencode(self.values)
        self.req  = urllib2.Request(self.url, self.data)
        try:
            self.origin = urllib2.urlopen(self.req)
        except HTTPError, e:
            print 'The server couldnot fulfill the request.'
            print 'Error code:', e.code
        except URLError, e:
            print 'Failed to reach a server.'
            print 'Reason:', e.reason
        return self.origin

    def process(self, response):
        doc = xml.dom.minidom.parse(response)
        pron  = doc.getElementsByTagName('pron')
        if pron:
            self.result['pron'] = pron[0].firstChild.data;
        else:
            self.result['pron'] = '';
        # def element is always contained, so no worries,
        # Just ues it
        exps  = doc.getElementsByTagName('def')[0].firstChild.data.split('\n')
        self.result['def'] = []
        for exp in exps:
            self.result['def'].append(exp)
        self.result['sentences'] = []
        sents = doc.getElementsByTagName('sent')
        s = self.result['sentences']
        for sent in sents:
            s.append({})
            s[len(s)-1]['o'] = sent.getElementsByTagName('orig')[0].firstChild.data
            s[len(s)-1]['t'] = sent.getElementsByTagName('trans')[0].firstChild.data

    def get_result(self, word):
        self.result['word'] = word
        self.get_origin(word)
        if self.origin:
            self.process(self.origin)
        if self.result:
            return self.result
        else:
            return {}
