'''
Created on 2 Dec 2014

@author: Admin
'''
from html.parser import HTMLParser 
import locale
import pandas as pd

class ActivityParser(HTMLParser):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.__is_table = False
        self.__tables = {}
        self.__table = []
        self.__headers = {}
        self.__header = []
        self.__tagtree = []
        self.__div_name = []
        self.__linedata = []
        self.__uncatched = []
        self.__current_header = ''
    
    def purge(self):
        name = self.__div_name.pop()
        self.__headers[name] = self.__current_header
        self.__tables[name] = self.__table.copy()
        self.__table = []
        self.__header = []
        
    def handle_starttag(self, tag, attrs):
        self.__tagtree.append(tag)
        if tag == 'table':
            self.__is_table = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.__is_table = False
            self.purge()
        elif tag == 'tr' and self.__is_table:
            if self.__header:
                self.__current_header = self.__header.copy()
                self.__header = []
            else:
                self.__table.append(self.__linedata)
                self.__linedata = []
        self.__tagtree.pop()
        
    def handle_data(self, data):
        try:
            if self.__is_table and data != '\n':
                if self.__tagtree[-1] == 'th':
                    self.__header.append(data)
                else:
                    self.__linedata.append(data)
            elif self.__tagtree[-1] == 'div' and not data.isspace():
                self.__div_name.append(data)
            else:
                self.__uncatched.append(data)
        except IndexError:
            print('data with no tag : ', data)
    
    def show(self):
        for k, v in self.__tables.items():
            print('table : {0}'.format(k))
            print('headers')
            print(self.__headers.get(k))
            print('body')
            for l in v:
                print(l)
            print('****end table****')

    def get_table(self, table_name):
        return self.__tables.get(table_name)
    
    def get_table_headers(self, table_name):
        return self.__headers.get(table_name)

    def get_table_name(self):
        return self.__tables.keys()
    
    def position_report(self):
        '''
        return te position report as a dataframe
        '''
        locale.setlocale(locale.LC_NUMERIC, 'us_US')
        outlist = []
        for l in self.get_table('Open Positions'):
            if l and len(l) == 1 and len(l[0]) == 3: #Currency trigram
                curr = l[0]
            if l and l[0] == '+': #new summary line
                line = []#l.copy()
                for i in l:
                    try:
                        line.append(locale.atof(i))
                    except:
                        line.append(i)
                line.append(curr)
                outlist.append(line[1:])
        headers = ['Symbol',
                   'Open',
                   'Quantity',
                   'Mult',
                   'Cost_Price',
                   'Cost_basis',
                   'Close_Price',
                   'Value',
                   'Unrealized_PnL',
                   'Currency']
        return pd.DataFrame(outlist, columns=headers)
        
            