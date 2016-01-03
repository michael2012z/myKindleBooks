# -*- coding: utf-8 -*-
from pyPdf import PdfFileWriter, PdfFileReader

def dividePdfPagesTopBottom(sourceFileName, pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap):
    targetFileName = sourceFileName[:-4] + "_div2_raw.pdf"
    input1 = PdfFileReader(file(sourceFileName, "rb"))
    input2 = PdfFileReader(file(sourceFileName, "rb"))
    output = PdfFileWriter()
    outputstream = file(targetFileName, "wb")
    numOfPages = input1.getNumPages()

    topBlockUpperLeftX, topBlockUpperLeftY = dividerX, dividerY+textBlockHeight
    topBlockUpperRightX, topBlockUpperRightY = dividerX+textBlockWidth, dividerY+textBlockHeight
    topBlockLowerLeftX, topBlockLowerLeftY = dividerX, dividerY-overlap
    topBlockLowerRightX, topBlockLowerRightY = dividerX+textBlockWidth, dividerY-overlap


    bottomBlockUpperLeftX, bottomBlockUpperLeftY = dividerX, dividerY+overlap
    bottomBlockUpperRightX, bottomBlockUpperRightY = dividerX+textBlockWidth, dividerY+overlap
    bottomBlockLowerLeftX, bottomBlockLowerLeftY = dividerX, dividerY-textBlockHeight
    bottomBlockLowerRightX, bottomBlockLowerRightY = dividerX+textBlockWidth, dividerY-textBlockHeight

    print "cutting {} ...".format(sourceFileName)

    for i in range(0, numOfPages):
        pageTop = input1.getPage(i)
        pageTop.mediaBox.upperLeft = topBlockUpperLeftX, topBlockUpperLeftY
        pageTop.mediaBox.upperRight = topBlockUpperRightX, topBlockUpperRightY
        pageTop.mediaBox.lowerLeft = topBlockLowerLeftX, topBlockLowerLeftY
        pageTop.mediaBox.lowerRight = topBlockLowerRightX, topBlockLowerRightY
        output.addPage(pageTop)
        pageBottom = input2.getPage(i)
        pageBottom.mediaBox.upperLeft = bottomBlockUpperLeftX, bottomBlockUpperLeftY
        pageBottom.mediaBox.upperRight = bottomBlockUpperRightX, bottomBlockUpperRightY
        pageBottom.mediaBox.lowerLeft = bottomBlockLowerLeftX, bottomBlockLowerLeftY
        pageBottom.mediaBox.lowerRight = bottomBlockLowerRightX, bottomBlockLowerRightY
        output.addPage(pageBottom)

    output.write(outputstream)
    outputstream.close()
    print "{} generated".format(targetFileName)


def dividePdfPagesTopBottomPlus(sourceFileName, pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlapX, overlapY):
    targetFileName = sourceFileName[:-4] + "_div4_raw.pdf"
    input1 = PdfFileReader(file(sourceFileName, "rb"))
    input2 = PdfFileReader(file(sourceFileName, "rb"))
    input3 = PdfFileReader(file(sourceFileName, "rb"))
    input4 = PdfFileReader(file(sourceFileName, "rb"))
    output = PdfFileWriter()
    outputstream = file(targetFileName, "wb")
    numOfPages = input1.getNumPages()

    topRightBlockUpperLeftX, topRightBlockUpperLeftY = dividerX+textBlockWidth-overlapX, dividerY+textBlockHeight
    topRightBlockUpperRightX, topRightBlockUpperRightY = dividerX+textBlockWidth*2, dividerY+textBlockHeight
    topRightBlockLowerLeftX, topRightBlockLowerLeftY = dividerX+textBlockWidth-overlapX, dividerY-overlapY
    topRightBlockLowerRightX, topRightBlockLowerRightY = dividerX+textBlockWidth*2, dividerY-overlapY

    topLeftBlockUpperLeftX, topLeftBlockUpperLeftY = dividerX, dividerY+textBlockHeight
    topLeftBlockUpperRightX, topLeftBlockUpperRightY = dividerX+textBlockWidth+overlapX, dividerY+textBlockHeight
    topLeftBlockLowerLeftX, topLeftBlockLowerLeftY = dividerX, dividerY-overlapY
    topLeftBlockLowerRightX, topLeftBlockLowerRightY = dividerX+textBlockWidth+overlapX, dividerY-overlapY


    bottomRightBlockUpperLeftX, bottomRightBlockUpperLeftY = dividerX+textBlockWidth-overlapX, dividerY+overlapY
    bottomRightBlockUpperRightX, bottomRightBlockUpperRightY = dividerX+textBlockWidth*2, dividerY+overlapY
    bottomRightBlockLowerLeftX, bottomRightBlockLowerLeftY = dividerX+textBlockWidth-overlapX, dividerY-textBlockHeight
    bottomRightBlockLowerRightX, bottomRightBlockLowerRightY = dividerX+textBlockWidth*2, dividerY-textBlockHeight

    bottomLeftBlockUpperLeftX, bottomLeftBlockUpperLeftY = dividerX, dividerY+overlapY
    bottomLeftBlockUpperRightX, bottomLeftBlockUpperRightY = dividerX+textBlockWidth+overlapX, dividerY+overlapY
    bottomLeftBlockLowerLeftX, bottomLeftBlockLowerLeftY = dividerX, dividerY-textBlockHeight
    bottomLeftBlockLowerRightX, bottomLeftBlockLowerRightY = dividerX+textBlockWidth+overlapX, dividerY-textBlockHeight

    print "cutting {} ...".format(sourceFileName)

    for i in range(0, numOfPages):
        pageTopRight = input1.getPage(i)
        pageTopLeft = input2.getPage(i)
        pageBottomRight = input3.getPage(i)
        pageBottomLeft = input4.getPage(i)

        pageTopRight.mediaBox.upperLeft = topRightBlockUpperLeftX, topRightBlockUpperLeftY
        pageTopRight.mediaBox.upperRight = topRightBlockUpperRightX, topRightBlockUpperRightY
        pageTopRight.mediaBox.lowerLeft = topRightBlockLowerLeftX, topRightBlockLowerLeftY
        pageTopRight.mediaBox.lowerRight = topRightBlockLowerRightX, topRightBlockLowerRightY

        pageTopLeft.mediaBox.upperLeft = topLeftBlockUpperLeftX, topLeftBlockUpperLeftY
        pageTopLeft.mediaBox.upperRight = topLeftBlockUpperRightX, topLeftBlockUpperRightY
        pageTopLeft.mediaBox.lowerLeft = topLeftBlockLowerLeftX, topLeftBlockLowerLeftY
        pageTopLeft.mediaBox.lowerRight = topLeftBlockLowerRightX, topLeftBlockLowerRightY

        pageBottomRight.mediaBox.upperLeft = bottomRightBlockUpperLeftX, bottomRightBlockUpperLeftY
        pageBottomRight.mediaBox.upperRight = bottomRightBlockUpperRightX, bottomRightBlockUpperRightY
        pageBottomRight.mediaBox.lowerLeft = bottomRightBlockLowerLeftX, bottomRightBlockLowerLeftY
        pageBottomRight.mediaBox.lowerRight = bottomRightBlockLowerRightX, bottomRightBlockLowerRightY

        pageBottomLeft.mediaBox.upperLeft = bottomLeftBlockUpperLeftX, bottomLeftBlockUpperLeftY
        pageBottomLeft.mediaBox.upperRight = bottomLeftBlockUpperRightX, bottomLeftBlockUpperRightY
        pageBottomLeft.mediaBox.lowerLeft = bottomLeftBlockLowerLeftX, bottomLeftBlockLowerLeftY
        pageBottomLeft.mediaBox.lowerRight = bottomLeftBlockLowerRightX, bottomLeftBlockLowerRightY

        output.addPage(pageTopRight)
        output.addPage(pageTopLeft)
        output.addPage(pageBottomRight)
        output.addPage(pageBottomLeft)

    output.write(outputstream)
    outputstream.close()
    print "{} generated".format(targetFileName)



def dividePdfPagesLeftRight(sourceFileName, pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap):
    targetFileName = sourceFileName[:-4] + "_divided.pdf"
    input1 = PdfFileReader(file(sourceFileName, "rb"))
    input2 = PdfFileReader(file(sourceFileName, "rb"))
    output = PdfFileWriter()
    outputstream = file(targetFileName, "wb")
    numOfPages = input1.getNumPages()

    rightBlockUpperLeftX, rightBlockUpperLeftY = dividerX-overlap, dividerY
    rightBlockUpperRightX, rightBlockUpperRightY = dividerX+textBlockWidth, dividerY
    rightBlockLowerLeftX, rightBlockLowerLeftY = dividerX-overlap, dividerY-textBlockHeight
    rightBlockLowerRightX, rightBlockLowerRightY = dividerX+textBlockWidth, dividerY-textBlockHeight

    leftBlockUpperLeftX, leftBlockUpperLeftY = dividerX-textBlockWidth, dividerY
    leftBlockUpperRightX, leftBlockUpperRightY = dividerX+overlap, dividerY
    leftBlockLowerLeftX, leftBlockLowerLeftY = dividerX-textBlockWidth, dividerY-textBlockHeight
    leftBlockLowerRightX, leftBlockLowerRightY = dividerX+overlap, dividerY-textBlockHeight

    print "cutting {} ...".format(sourceFileName)

    for i in range(0, numOfPages):
        pageRight = input1.getPage(i)
        pageRight.mediaBox.upperLeft = rightBlockUpperLeftX, rightBlockUpperLeftY
        pageRight.mediaBox.upperRight = rightBlockUpperRightX, rightBlockUpperRightY
        pageRight.mediaBox.lowerLeft = rightBlockLowerLeftX, rightBlockLowerLeftY
        pageRight.mediaBox.lowerRight = rightBlockLowerRightX, rightBlockLowerRightY
        output.addPage(pageRight)

        pageLeft = input2.getPage(i)
        pageLeft.mediaBox.upperLeft = leftBlockUpperLeftX, leftBlockUpperLeftY
        pageLeft.mediaBox.upperRight = leftBlockUpperRightX, leftBlockUpperRightY
        pageLeft.mediaBox.lowerLeft = leftBlockLowerLeftX, leftBlockLowerLeftY
        pageLeft.mediaBox.lowerRight = leftBlockLowerRightX, leftBlockLowerRightY
        output.addPage(pageLeft)
        
    output.write(outputstream)
    outputstream.close()
    print "{} generated".format(targetFileName)


def cutShiSanJingA():
    pageWidth = 515
    pageHeight = 728 
    #textBlockWidth = int(pageWidth * 0.73)
    textBlockWidth = int(pageWidth * 0.69)
    textBlockHeight = int(pageHeight * 0.35)
    #dividerX = int(pageWidth * 0.13)
    dividerX = int(pageWidth * 0.15)
    dividerY = int(pageHeight * 0.527)
    overlap = 0
    dividePdfPagesTopBottom('十三经注疏_01_周易正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesTopBottom('十三经注疏_02_尚書正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesTopBottom('十三经注疏_03_毛詩正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +5, overlap)
    dividePdfPagesTopBottom('十三经注疏_04_周禮注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +3, overlap)
    dividePdfPagesTopBottom('十三经注疏_05_儀禮注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +5, overlap)
    dividePdfPagesTopBottom('十三经注疏_06_禮記正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +3, overlap)
    dividePdfPagesTopBottom('十三经注疏_07_春秋左傳正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +2, overlap)
    dividePdfPagesTopBottom('十三经注疏_08_春秋公羊傳注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY+5, overlap)
    dividePdfPagesTopBottom('十三经注疏_09_春秋穀梁傳注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +2, overlap)
    dividePdfPagesTopBottom('十三经注疏_10_論語注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +5, overlap)
    dividePdfPagesTopBottom('十三经注疏_11_爾雅注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +1, overlap)
    dividePdfPagesTopBottom('十三经注疏_12_孟子注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +5 , overlap)
    dividePdfPagesTopBottom('十三经注疏_13_孝經注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +2, overlap)

def cutShiSanJingB():
    pageWidth = 515
    pageHeight = 728 
    #textBlockWidth = int(pageWidth * 0.73)
    textBlockWidth = int(pageWidth * 0.69 / 2)
    textBlockHeight = int(pageHeight * 0.35)
    #dividerX = int(pageWidth * 0.13)
    dividerX = int(pageWidth * 0.15)
    dividerY = int(pageHeight * 0.527)
    overlapX = int(textBlockWidth * 0.04)
    overlapY = 0
    dividePdfPagesTopBottomPlus('十三经注疏_01_周易正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_02_尚書正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_03_毛詩正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +5, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_04_周禮注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +3, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_05_儀禮注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +5, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_06_禮記正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +3, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_07_春秋左傳正義.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +2, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_08_春秋公羊傳注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY+5, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_09_春秋穀梁傳注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +2, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_10_論語注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +5, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_11_爾雅注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +1, overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_12_孟子注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +5 , overlapX, overlapY)
    dividePdfPagesTopBottomPlus('十三经注疏_13_孝經注疏.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +2, overlapX, overlapY)




def cutShiSanJingC():
    pageWidth = 842
    pageHeight = 1191 
    textBlockWidth = int(pageWidth * 0.46)
    textBlockHeight = int(pageHeight * 0.45)
    dividerX = int(pageWidth * 0.51)
    dividerY = int(pageHeight * 0.885)
    overlap = 10
    dividePdfPagesLeftRight('十三经注疏_01_周易兼義九卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesLeftRight('十三经注疏_02_尚書註疏二十卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesLeftRight('十三经注疏_03_毛詩註疏二十卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesLeftRight('十三经注疏_04_周禮註疏四十二卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesLeftRight('十三经注疏_05_儀禮註疏十七卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesLeftRight('十三经注疏_06_禮記註疏六十三卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesLeftRight('十三经注疏_07_春秋左傳註疏六十卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesLeftRight('十三经注疏_08_春秋公羊傳註疏二十八卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +30, overlap)
    dividePdfPagesLeftRight('十三经注疏_09_春秋穀梁傳註疏二十卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +30, overlap)
    dividePdfPagesLeftRight('十三经注疏_10_論語註疏解經二十卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +10, overlap)
    dividePdfPagesLeftRight('十三经注疏_11_孝經正義九卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY, overlap)
    dividePdfPagesLeftRight('十三经注疏_12_爾雅註疏十一卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +12, overlap)
    dividePdfPagesLeftRight('十三经注疏_13_孟子註疏解經十四卷.pdf', pageWidth, pageHeight, textBlockWidth, textBlockHeight, dividerX, dividerY +10, overlap)




def checkSize():
    input1 = PdfFileReader(file('十三经注疏_01_周易正義_divided.pdf', "rb"))
    numOfPages = input1.getNumPages()

    for i in range(0, numOfPages):
        page = input1.getPage(i)
        print page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y(), page.mediaBox.getLowerRight_x(), page.mediaBox.getLowerRight_y(), page.mediaBox.getUpperLeft_x(), page.mediaBox.getUpperLeft_y(), page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y()

# checkSize()
cutShiSanJingA()
cutShiSanJingB()

