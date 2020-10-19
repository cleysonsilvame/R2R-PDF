import PyPDF2 as pdf
import os
from datetime import datetime
import time
import re


def clearString(nameFile):
    nameFile = re.sub('[^0-9]', '', nameFile)
    return nameFile


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
        return clearString(nameFile)

    for indice in pageArray:
        if '000000' in indice:
            nameFile = indice
            return clearString(nameFile)

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

                        oldNameFile = str(file)
                        newNameFile = getPDFname(oldFile)

                        newFile = os.path.join(
                            item, newNameFile + '.pdf')

                        if os.path.exists(newFile):
                            time.sleep(1)
                            now = datetime.now()
                            localtime = now.strftime(
                                "Data %m.%d.%Y - Hora %H.%M.%S")

                            newFile = os.path.join(
                                item, newNameFile + ' - ' + localtime + '.pdf')

                        print('Nome: ' + oldNameFile +
                              ' ----> ' + newNameFile + '\n')
                        os.rename(oldFile, newFile)
except Exception as err:
    print(err)
    print('Ocorreu um erro!')
    input()


print('Processo finalizado com sucesso, aperte qualquer tecla para sair!')

input()
