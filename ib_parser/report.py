'''
Created on 2 Dec 2014

@author: Admin
'''
import html_parser.ib_parser.parser as parser
# import html_parser

if __name__ == '__main__':
    fpath = 'C:\\Users\\Admin\\Documents\\U1152809_20141128.html'
    with open(fpath)as f:
        data = f.read()
    f.close
    ibparser = parser.ActivityParser()
    ibparser.feed(data)
#     ibparser.show()
    df = ibparser.position_report() 