import PyPDF2 as pdf
from datetime import datetime
import re

def getPDFname(path):
    now = datetime.now()
    nameFile = now.strftime("Data %m.%d.%Y - Hora %H.%M.%S")

    pdfPath = pdf.PdfFileReader(path)
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