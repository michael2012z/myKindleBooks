# -*- coding: utf-8 -*-
import sys
from HTMLParser import HTMLParser
import urllib, urllib2, cookielib
import os, time
import xml.dom.minidom

#import locale
from decimal import Decimal
from re import sub

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

ctextBaseUrl = "http://ctext.org/"

# [[bookname, [[link, chaptername], [... ],...]],
#  [bookname, [[link, chaptername], [... ],...]]
# ]
bookList = [
    ['孟子', ['梁惠王上', '梁惠王下', '公孫丑上', '公孫丑下', '滕文公上', '滕文公下', '離婁上', '離婁下', '萬章上', '萬章下', '告子上', '告子下', '盡心上', '盡心下']],
]

    
class WebPageParser(HTMLParser):
    textOn = False
    text = []
    textPiece = ""
    cClass = "content"

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []
        self.textOn = False
        self.textPiece = ""
        self.cClass = "content"

    def parse(self, html):
        try:
            self.feed(html)
            return True
        except Exception, e:
            print e
            return False

    def getText(self):
        return self.text

    def handle_starttag(self,tag,attrs):
        if tag == "td" and len(attrs) == 1 and attrs[0] == ('class', 'ctext'):
            self.textOn = True
            self.textPiece = ""
            self.cClass = "content"

    def handle_data(self, data):
        if self.textOn == True:
            if data.strip() <> "":
                self.textPiece += data

    def handle_endtag(self, tag):
        if tag == "td" and self.textOn == True:
            self.text.append([self.cClass, self.textPiece])
            self.textOn = False

htmlText1 = '''
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-TW">
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
 <meta http-equiv="Content-Language" content="zh-TW" />
<title>'''

htmlText2 = '''</title>
<link rel="stylesheet" href="style.css" type="text/css" />
</head>
<body>
'''

htmlText3 = '''
</body></html>
'''

ncxText1 = '''
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" 
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
 <head>
 </head>
        <docTitle>
               <text>'''
ncxText2 = '''</text>
        </docTitle>
    <navMap>\n'''
ncxText3 = '''
	</navMap>
</ncx>\n'''


opfText1 = '''
<?xml version="1.0" encoding="utf-8"?>
<package unique-identifier="uid" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:asd="http://www.idpf.org/asdfaf">
    <metadata>
        <dc-metadata  xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openebook.org/namespaces/oeb-package/1.0/">
            <dc:Title>'''
opfText2 = '''</dc:Title>
            <dc:Language>zh-TW</dc:Language>
            <dc:Creator>第二月</dc:Creator>
            <dc:Copyrights>第二月</dc:Copyrights>
            <dc:Publisher>第二月</dc:Publisher>
        </dc-metadata>
    </metadata>
    <manifest>
        <item id="text" media-type="text/x-oeb1-document" href="welcome.html"></item>
        <item id="content" media-type="text/x-oeb1-document" href="toc.html"></item>
'''

opfText3 = '''
        <item id="ncx" media-type="application/x-dtbncx+xml" href="toc.ncx"/>
    </manifest>
    <spine toc="ncx">
        <itemref idref="text"/>
        <itemref idref="content"/>
'''

opfText4 = '''
    </spine>
    <guide>
        <reference type="toc" title="Table of Contents" href="toc.html"/>
        <reference type="text" title="'''

opfText5 = '''" href="welcome.html"/>
    </guide>
</package>
'''

if __name__ == '__main__':
    for book in bookList:
        bookName = book[0]
        chapterList = book[1]
        i = 0
        for chapter in chapterList:
            i += 1
            fileName = '' + bookName + '/raw/' + bookName + ' : ' + chapter + ' - 中國哲學書電子化計劃.html'
            print fileName
            f = open(fileName, "r")
            rawText = f.read()
            f.close()
            parser = WebPageParser()
            parser.parse(rawText)
            textLines = parser.getText()
            # chapter content
            htmlText = htmlText1
            htmlText += chapter
            htmlText += htmlText2
            htmlText += '<div id="ch' + str(i) + '"></div>\n'
            htmlText += '<h2>' + chapter + '</h2>\n'
            for textLine in textLines:
                htmlText += '<p class=\"' + textLine[0] + '\">' + textLine[1] + '</p>\n'
            htmlText += htmlText3
            fileName = bookName + "/" + bookName + "_" + chapter + ".html"
            f = open(fileName, 'w')
            f.write(htmlText)
            f.close()

        # generate TOC
        htmlText = htmlText1
        htmlText += 'Table Of Contents'
        htmlText += htmlText2
        htmlText += '<h2 id="toc">Table Of Contents</h2>\n'
        htmlText += '<ul>\n'
        i = 0
        for chapter in chapterList:
            i += 1
            fileName = bookName + "_" + chapter + ".html"
            htmlText += '<li><a href="' + fileName + '#ch' + str(i) + '">' + chapter + '</a></li>\n'
        htmlText += '</ul>\n'
        htmlText += htmlText3
        f = open(bookName + "/toc.html", 'w')
        f.write(htmlText)
        f.close()

        # generate NCX
        ncxText = ncxText1
        ncxText += bookName
        ncxText += ncxText2
        ncxText += '''
		<navPoint id="toc" playOrder="1">
			<navLabel>
				<text>
					Table of Contents
				</text>
			</navLabel>
			<content src="toc.html#toc" />
		</navPoint>'''
        i = 0
        for chapter in chapterList:
            i += 1
            fileName = bookName + "_" + chapter + ".html"
            ncxText += '''
		<navPoint id="''' + 'ch' + str(i) + '''" playOrder="''' + str(i+1) + '''">
			<navLabel>
				<text>
					''' + chapter + '''
				</text>
			</navLabel>
			<content src="''' + fileName + '#ch' + str(i) + '''" />
		</navPoint>'''   
        ncxText += '\n' + ncxText3
        f = open(bookName + "/toc.ncx", 'w')
        f.write(ncxText)
        f.close()

        # generate welcome page
        htmlText = htmlText1
        htmlText += bookName
        htmlText += htmlText2
        htmlText += '<h1>' + bookName+ '</h1>\n'
        htmlText += htmlText3
        f = open(bookName + "/welcome.html", 'w')
        f.write(htmlText)
        f.close()

        # generate opf page
        opfText = opfText1
        opfText += bookName
        opfText += opfText2
        i = 0
        for chapter in chapterList:
            i += 1
            opfText += '<item id="ch' + str(i) + '" media-type="text/x-oeb1-document" href="' + bookName + '_' + chapter + '.html" />\n'
        opfText += opfText3
        i = 0
        for chapter in chapterList:
            i += 1
            opfText += '<itemref idref="ch' + str(i) + '"/>\n'
        opfText += opfText4
        opfText += bookName
        opfText += opfText5
        f = open(bookName + "/" + bookName +".opf", 'w')
        f.write(opfText)
        f.close()

