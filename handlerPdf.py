import PyPDF2 as pdf
from datetime import datetime
import re


def getPDFname(path):
    nameFile = ''

    pdfPath = pdf.PdfFileReader(str(path))
    page = pdfPath.getPage(0)

    pageString = page.extractText()

    pageArray = pageString.split()

    if ('Protocolo:' in pageArray):
        indexProto = pageArray.index('Protocolo:')
        indexProtoNumber = indexProto + 1
        nameFile = pageArray[indexProtoNumber]

    for indice in pageArray:
        if '000000' in indice:
            nameFile = indice

    return clearString(nameFile)


def clearString(nameFile):
    nameFile = re.sub('[^0-9]', '', nameFile)
    return nameFile


def getLocalTime():
    now = datetime.now()
    localtime = now.strftime("Data %m.%d.%Y - Hora %H.%M.%S")
    return localtime
