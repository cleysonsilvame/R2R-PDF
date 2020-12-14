import PySimpleGUI as sg
import PyPDF2 as pdf
import os
from datetime import datetime
import time
import re
from tabulate import tabulate
import threading


def start():
    sg.theme('Dark Blue 3')
    layout = [
        [sg.Text('Selecione a pasta para renomear: ')],
        [sg.Input(), sg.FolderBrowse(key='path')],
        [
            sg.OK('Iniciar', disabled=True),
            sg.OK('Verificar Arquivos'),
            sg.CloseButton('Fechar')
        ],
        [sg.Output(size=(70, 12))],
        [sg.ProgressBar(100, orientation='h', size=(46, 20),
                        key='progress_bar')],

    ]

    window = sg.Window('R2R-PDF', layout)
    ok_button = window.FindElement('Iniciar')

    while True:
        event, values = window.Read()

        if event == 'Verificar Arquivos':
            paths = getPDFByPath(values['path'])
            totalPaths = len(paths)
            namesPDF = map(lambda x: {"name": x["name"]}, paths)

            sg.popup_scrolled(
                "Total de Arquivos Encontrados: ",
                totalPaths,
                tabulate(namesPDF),
                size=(50, 10)
            )
            ok_button.Update(disabled=False)

        elif event == 'Iniciar':
            try:
                progress_value = 100 / totalPaths
                threading.Thread(target=rename, args=(
                    paths, window, progress_value), daemon=True).start()
            except Exception as err:
                sg.Popup('Ocorreu um erro!', err)

        elif event == '-THREAD-':
            print('Todos os arquivos renomeado com sucesso: ', values[event])

        elif event == 'Fechar' or event == sg.WIN_CLOSED:
            break


def getPDFByPath(selected_folder):
    folders = os.walk(selected_folder)
    paths_filtered_by_PDF = []

    for root, dirs, files in folders:
        for file in files:
            if file.endswith(".pdf"):
                pathObject = {
                    "name": file,
                    "path": root
                }
                paths_filtered_by_PDF.append(pathObject)

    return paths_filtered_by_PDF


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

    for indice in pageArray:
        if '000000' in indice:
            nameFile = indice

    return clearString(nameFile)


def rename(oldPaths, window, progress_value):
    progress_bar = window.FindElement('progress_bar')
    i = 0

    for item in oldPaths:
        oldNameFile = item["name"]

        oldPathFile = os.path.join(item["path"], item["name"])
        newNameFile = getPDFname(oldPathFile) + ".pdf"

        newPathFile = os.path.join(item["path"], newNameFile)

        if os.path.exists(newPathFile):
            time.sleep(1)

            now = datetime.now()
            localtime = now.strftime(
                "Data %m.%d.%Y - Hora %H.%M.%S")

            newPathFile = os.path.join(
                item["path"],
                newNameFile
                + ' - '
                + localtime
                + '.pdf'
            )

        print(
            'Nome: '
            + oldNameFile
            + ' ----> '
            + newNameFile
            + '\n'
        )
        os.rename(oldPathFile, newPathFile)
        i += progress_value
        progress_bar.UpdateBar(i)
    window.write_event_value('-THREAD-', '** DONE **')


if __name__ == '__main__':
    start()
