import PyPDF2 as pdf
import os
from datetime import datetime
import time


def getPDFname(path):
    now = datetime.now()
    nameFile = now.strftime("%m.%d.%Y, %H.%M.%S")

    pdfPath = pdf.PdfFileReader(path)
    page = pdfPath.getPage(0)

    pageString = page.extractText()

    pageArray = pageString.split()


aun if ('Protocolo:' in pageArray):
        indexProto = pageArray.index('Protocolo:')
        indexProtoNumber = indexProto + 1
        nameFile = pageArray[indexProtoNumber]

    if ('PROTOCOLO' in pageArray):
        indexProto = pageArray.index('PROTOCOLO')
        indexProtoNumber = indexProto + 1
        nameFile = pageArray[indexProtoNumber]

    return nameFile


pastaAtual = os.path.dirname(os.path.realpath(__file__))

for item in os.listdir(pastaAtual):
    item = os.path.join(pastaAtual, item)
    if os.path.isdir(item):
        if item != os.path.join(pastaAtual, '.git') and item != os.path.join(pastaAtual, '.vscode'):
            for (root, dirs, files) in os.walk(item):
                for file in files:
                    oldFile = os.path.join(item, file)
                    newFile = os.path.join(item, getPDFname(oldFile) + '.pdf')
                    if os.path.exists(newFile):
                        now = datetime.now()
                        localtime = now.strftime("%m.%d.%Y, %H.%M.%S")
                        newFile = os.path.join(
                            item, getPDFname(oldFile) + ' - ' + localtime + '.pdf')
                        time.sleep(1)
                    os.rename(oldFile, newFile)
