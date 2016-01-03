# -*- coding: utf-8 -*-
import os

filesRaw = '''
十三经注疏_01_周易正義_div2_raw.pdf  十三经注疏_06_禮記正義_div2_raw.pdf        十三经注疏_11_爾雅注疏_div2_raw.pdf
十三经注疏_02_尚書正義_div2_raw.pdf  十三经注疏_07_春秋左傳正義_div2_raw.pdf    十三经注疏_12_孟子注疏_div2_raw.pdf
十三经注疏_03_毛詩正義_div2_raw.pdf  十三经注疏_08_春秋公羊傳注疏_div2_raw.pdf  十三经注疏_13_孝經注疏_div2_raw.pdf
十三经注疏_04_周禮注疏_div2_raw.pdf  十三经注疏_09_春秋穀梁傳注疏_div2_raw.pdf
十三经注疏_05_儀禮注疏_div2_raw.pdf  十三经注疏_10_論語注疏_div2_raw.pdf
'''

files = filesRaw.split()
bookNames = []

for file in files:
    bookNames.append(file[:-13])

for bookName in bookNames:
    print bookName
    os.system('pdftoppm -png ' + bookName + '/' + bookName + '_div4_raw.pdf ' + bookName + '/' + bookName + '_div4')
    
