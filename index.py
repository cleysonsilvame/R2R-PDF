import PyPDF2 as pdf
import os
from datetime import datetime
import time


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

    if ('PROTOCOLO' in pageArray):
        indexProto = pageArray.index('PROTOCOLO')
        indexProtoNumber = indexProto + 1
        nameFile = pageArray[indexProtoNumber]

    return nameFile


try:
    pastaAtual = os.path.dirname(os.path.realpath(__file__))

    for item in os.listdir(pastaAtual):
        item = os.path.join(pastaAtual, item)
        if os.path.isdir(item):
            for (root, dirs, files) in os.walk(item):
                for file in files:
                    if file.endswith(".pdf"):
                        oldFile = os.path.join(item, file)
                        newFile = os.path.join(
                            item, getPDFname(oldFile) + '.pdf')

                        if os.path.exists(newFile):
                            time.sleep(1)
                            now = datetime.now()
                            localtime = now.strftime(
                                "Data %m.%d.%Y - Hora %H.%M.%S")

                            newFile = os.path.join(
                                item, getPDFname(oldFile) + ' - ' + localtime + '.pdf')

                        os.rename(oldFile, newFile)
except Exception as err:
    print(err)
    print('Ocorreu um erro!')
    input()
