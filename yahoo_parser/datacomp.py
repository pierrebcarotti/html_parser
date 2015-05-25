__author__ = 'Admin'

import requests
import urllib
from lxml import html

TABLE_HEADERS = 'yfnc_tablehead1'
TABLE_VALUES = 'yfnc_tabledata1'


def get_fin_data(url):
    """
    Import fin data from yahoo server
    :param url: the full url name
    :return: a dictionary (field: value)
    """
    page = requests.get(url)
    tree = html.fromstring(page.text)
    elts_hd = tree.find_class(TABLE_HEADERS)
    elts_val = tree.find_class(TABLE_VALUES)
    keys = [k.text for k in elts_hd]
    vals = [v.text if v.text else v.getchildren()[0].text for v in elts_val]
    return {k: v for k,v in zip(keys, vals)}


