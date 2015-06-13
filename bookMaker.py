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

# [[bookname, [groupname, [chaptername, ...], ...]],
#  [bookname, [groupname, [chaptername, ...], ...]],
# ]
bookList = [
    ['孟子', [['', ['梁惠王上', '梁惠王下', '公孫丑上', '公孫丑下', '滕文公上', '滕文公下', '離婁上', '離婁下', '萬章上', '萬章下', '告子上', '告子下', '盡心上', '盡心下']]]],
    ['論語', [['', ['學而', '為政', '八佾', '里仁', '公冶長', '雍也', '述而', '泰伯', '子罕', '鄉黨', '先進', '顏淵', '子路', '憲問', '衛靈公', '季氏', '陽貨', '微子', '子張', '堯曰']]]],
    ['禮記', [['', ['曲禮上', '曲禮下', '檀弓上', '檀弓下', '王制', '月令', '曾子問', '文王世子', '禮運', '禮器', '郊特牲', '內則', '玉藻', '明堂位', '喪服小記', '大傳', '少儀', '學記', '樂記', '雜記上', '雜記下', '喪大記', '祭法', '祭義', '祭統', '經解', '哀公問', '仲尼燕居', '孔子閒居', '坊記', '中庸', '表記', '緇衣', '奔喪', '問喪', '服問', '間傳', '三年問', '深衣', '投壺', '儒行', '大學', '冠義', '昏義', '鄉飲酒義', '射義', '燕義', '聘義', '喪服四制']]]],
    ['莊子', [['內篇', ['逍遙遊', '相關討論', '', '齊物論', '養生主', '人間世', '德充符', '大宗師', '應帝王', '相關討論']], ['外篇', ['駢拇', '馬蹄', '胠篋', '在宥', '天地', '天道', '天運', '刻意', '繕性', '秋水', '至樂', '達生', '山木', '田子方', '知北遊']], ['雜篇', ['庚桑楚', '徐無鬼', '則陽', '外物', '寓言', '讓王', '盜跖', '說劍', '漁父', '列御寇', '天下']]]],
    ['四書章句集注', [['大學章句', ['大學章句序', '大學章句']], ['中庸章句', ['中庸章句序', '中庸章句']], ['論語集注', ['論語序說', '讀論語孟子法', '學而第一', '為政第二', '八佾第三', '里仁第四', '公冶長第五', '雍也第六', '述而第七', '泰伯第八', '子罕第九', '鄉黨第十', '先進第十一', '顏淵第十二', '子路第十三', '憲問第十四', '衛靈公第十五', '季氏第十六', '陽貨第十七', '微子第十八', '子張第十九', '堯曰第二十']], ['孟子集注', ['孟子序說', '梁惠王章句上', '梁惠王章句下', '公孫丑章句上', '公孫丑章句下', '滕文公章句上', '滕文公章句下', '離婁章句上', '離婁章句下', '萬章章句上', '萬章章句下', '告子章句上', '告子章句下', '盡心章句上', '盡心章句下']]]]
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
        groupList = book[1]
        for group in groupList:
            groupName = group[0]
            chapterList = group[1]
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
        groupList = book[1]
        for group in groupList:
            groupName = group[0]
            chapterList = group[1]
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
        groupList = book[1]
        for group in groupList:
            groupName = group[0]
            chapterList = group[1]
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
        groupList = book[1]
        for group in groupList:
            groupName = group[0]
            chapterList = group[1]
            i = 0
            for chapter in chapterList:
                i += 1
                opfText += '<item id="ch' + str(i) + '" media-type="text/x-oeb1-document" href="' + bookName + '_' + chapter + '.html" />\n'
        opfText += opfText3
        groupList = book[1]
        for group in groupList:
            groupName = group[0]
            chapterList = group[1]
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

