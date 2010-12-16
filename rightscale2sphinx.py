#!uesr/bin/env python
# encoding: utf-8
"""
Created by Naotaka Jay HOTTA on 2010-12-10
Copyright (c) 2010 CMScom. All rights reserved.
"""

import logging
import os
from core import mindtouch2Sphinx

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=os.path.join(os.getcwd(), '/tmp/web2sphinx.log'),
                    filemode='w')

URL = "http://support.rightscale.com"

class RightScale2Sphinx(mindtouch2Sphinx):
    pass

if __name__ == '__main__':
    """
    """
    a = RightScale2Sphinx(URL)
    a.get_pages()
