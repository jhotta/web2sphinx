#!uesr/bin/env python
# encoding: utf-8
"""
Created by Manabu TERADA on 2010-12-07.
Modified by Naotaka Jay HOTTA on 2010-12-10
Copyright (c) 2010 CMScom. All rights reserved.
diescription: test programing to get contents from web site and make ReST files for sphinx.
"""

import codecs
import os
import urllib2
from xml.etree import ElementTree
# import lxml.html
# from lxml.etree import ParserError
from html2rst import html2text

URL_LIST_API = "http://support.rightscale.com/@api/deki/pages"

base_os_path = os.getcwd()
PAGE_LIST_FILE = os.path.join(base_os_path, 'pages_list.txt')
SAVE_DIR = os.path.join(base_os_path, 'ROOT')


def save_data_file(path, name, body):
    save_path = os.path.join(SAVE_DIR, path)
    try:
        os.makedirs(save_path)
    except OSError:
        pass
    with open(os.path.join(save_path, name), 'w') as f:
        f = codecs.lookup('utf-8')[-1](f)
        f.write(body)


def _get_page_content(elem):
    id = elem.get('id')
    title = elem.findtext('.//title')
    apiurl = elem.get('href').split("?")[0] + '/contents'
    url = elem.findtext('.//uri.ui')
    path = elem.findtext('.//path')
    path_list = path.rsplit('/', 1)
    if len(path_list) > 1:
        os_path, name = path_list
    else:
        os_path, name = ('', path_list[0] or 'root')
    return (name, id, title, apiurl, os_path, url)


def get_page_content(path, name, title, apiurl):
    try:
        s = urllib2.urlopen(apiurl)
        xml = s.read()
    except Exception, e:
        print "Error: root api ", e
    else:
        s.close()
        dom = ElementTree.fromstring(xml)

        import pdb ; pdb.set_trace()

        body = dom.findtext('.//body')
        html = "<html><head><title>%s</title></head><body>%s</body></html>" % (title, body,)
        rst_body = html2text(html)
        save_data_file(path, name, rst_body)


def get_pages(root='/'):
    try:
        s = urllib2.urlopen(URL_LIST_API)
        try:
            xml = s.read()
        except Exception, e:
            print "Error: root api ", e
        finally:
            s.close()
    except Exception, e:
        print "Error: root api", e
    dom = ElementTree.fromstring(xml)
    pages = dom.findall('.//page')
    for page in pages:
        data = _get_page_content(page)
        get_page_content(data[4], data[0] + '.txt', data[2], data[3])


if __name__ == '__main__':
    """
    """
    get_pages()
