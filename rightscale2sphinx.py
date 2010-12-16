#!uesr/bin/env python
# encoding: utf-8
"""
Created by Naotaka Jay HOTTA on 2010-12-10
Copyright (c) 2010 CMScom. All rights reserved.
"""

# import StringIO
import logging
import codecs
import os
import re
import urllib2
# from xml.sax.saxutils import unescape
from xml.etree import ElementTree
from html2rst import html2text

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=os.path.join(os.getcwd(), '/tmp/web2sphinx/core.log'),
                    filemode='w')

URL = "http://support.rightscale.com"
PAGE_LIST_FILE = 'pages_list.txt'
HTML_SAVE_DIR = 'html'
REST_SAVE_DIR = 'rest/root'


class Web2SphinxBase(object):
    """
    """

    def __init__(self):
        """
        """
        base_os_path = os.getcwd()
        self.page_list_File = os.path.join(base_os_path, PAGE_LIST_FILE)
        self.html_save_dir = os.path.join(base_os_path, HTML_SAVE_DIR)
        self.rest_save_dir = os.path.join(base_os_path, REST_SAVE_DIR)


    def _html_validate(self, html):
        return html


    def _path_localize(self, dom):
        return dom


    def _change_charactor(self, text, org, new):
        text = re.sub(org, new, text)
        # print text
        return text


    def _clean_charactor(self, text, org):
        text = self._change_charactor(text, org, "")
        #print text
        return text




class RightScale2Sphinx(Web2SphinxBase):
    """
    """

    def __init__(self):
        """
        """
        self.url_list_api = URL + "/@api/deki/pages"


    def _get_page_content(self, elem):
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


    def save_data_file(self, root_path, path, file_name, body):
        dir_path = os.path.join(root_path, path)
        file_path = os.path.join(dir_path, file_name)
        try:
            os.makedirs(dir_path)
        except OSError:
            pass
        with open(file_path, 'w') as f:
            f = codecs.lookup('utf-8')[-1](f)
            f.write(body)

            logging.info(file_path)
        print file_path


    def get_page_content(self, path, name, title, apiurl):
        try:
            s = urllib2.urlopen(apiurl)
            xml = s.read()
            # print xml
        except Exception, e:
            print "Error: root api ", e
        else:
            s.close()
            dom = ElementTree.fromstring(xml)
            import pdb; pdb.set_trace()
            # dom = _link_path_localize(dom)
            body = dom.findtext('.//body')
            html = "<html><head><title>%s</title></head><body>%s</body></html>" % (title, body,)
            rst = html2text(html)
            self.save_data_file(self.HTML_SAVE_DIR, path, name + '.html', html)
            self.save_data_file(self.REST_SAVE_DIR, path, name + '.rst', rst)


    def get_pages(self, root='/'):
        try:
            s = urllib2.urlopen(self.url_list_api)
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
            data = self._get_page_content(page)
            self. get_page_content(data[4], data[0], data[2], data[3])


if __name__ == '__main__':
    """
    """
    pass
    # get_pages()
