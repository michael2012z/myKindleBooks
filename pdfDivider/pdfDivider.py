# -*- coding: utf-8 -*-
import sys
import os
from pyPdf import PdfFileWriter, PdfFileReader

# generate new pdf file, divided the file horizentally
def dividePdfFileH(fileName, segments, overlapRate):
    sourceFileName = fileName
    targetFileName = sourceFileName[:-4] + "_div" + str(segments)+ ".pdf"
    print "dividing {}".format(sourceFileName)
    readers = []
    for i in range(segments):
        readers.append(PdfFileReader(file(sourceFileName, "rb")))
    output = PdfFileWriter()
    outputstream = file(targetFileName, "wb")
    numOfPages = readers[0].getNumPages()
    for i in range(numOfPages):
        page = readers[0].getPage(i)
        llx, lly = page.mediaBox.getLowerLeft_x(), page.mediaBox.getLowerLeft_y()
        lrx, lry = page.mediaBox.getLowerRight_x(), page.mediaBox.getLowerRight_y()
        ulx, uly = page.mediaBox.getUpperLeft_x(), page.mediaBox.getUpperLeft_y()
        urx, ury = page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y()
        heightLeft = uly - lly
        heightRight = ury - lry
        subpageHeightLeft = int((float(heightLeft)*1.0)/(segments * 1.0 + 2 * overlapRate))
        subpageHeightRight = int((float(heightRight)*1.0)/(segments * 1.0 + 2 * overlapRate))
        overlapSizeLeft = int(subpageHeightLeft * overlapRate)
        overlapSizeRight = int(subpageHeightRight * overlapRate)
        spageHL = subpageHeightLeft
        spageHR = subpageHeightRight
        uly -= overlapSizeLeft
        ury -= overlapSizeRight
        lly += overlapSizeLeft
        lry += overlapSizeRight
        for j in range(segments):
            spage = readers[j].getPage(i)
            spage.mediaBox.upperLeft = ulx, uly - spageHL * j + overlapSizeLeft
            spage.mediaBox.upperRight = urx, ury - spageHR * j + overlapSizeRight
            spage.mediaBox.lowerLeft = llx, uly - spageHL * (j + 1) - overlapSizeLeft
            spage.mediaBox.lowerRight = urx, ury - spageHR * (j + 1) - overlapSizeRight
            output.addPage(spage)
    output.write(outputstream)
    outputstream.close()
    pdfToPpmCmdText = 'pdftoppm -png -r 300 ' + targetFileName + ' ' + targetFileName[:-4] + '-tmp-'
    print pdfToPpmCmdText
    os.system(pdfToPpmCmdText)
    rmCmdText = 'rm -f ' + targetFileName
    print rmCmdText
    os.system(rmCmdText)
    cvtCmdText = 'convert *-tmp-*.png ' + targetFileName
    print cvtCmdText
    os.system(cvtCmdText)
    rmCmdText = 'rm -f *-tmp-*.png'
    print rmCmdText
    os.system(rmCmdText)
    print "{} generated".format(targetFileName)

# arguments
numOfSegments = int(sys.argv[2])
sourceFileName = sys.argv[1]

overlapRate = 0.07

dividePdfFileH(sourceFileName, numOfSegments, overlapRate)

