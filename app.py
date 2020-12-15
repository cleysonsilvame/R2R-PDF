import PySimpleGUI as sg
from tabulate import tabulate
import threading
from paths import getPDFByPath, rename


def window():
    sg.theme('Dark Blue 3')
    layout = [
        [sg.Text('Selecione a pasta para renomear: ')],
        [sg.Input(), sg.FolderBrowse(key='-PATH-')],
        [
            sg.OK('Iniciar', disabled=True),
            sg.OK('Verificar Arquivos'),
            sg.CloseButton('Fechar')
        ],
        [sg.Output(size=(70, 12))],
        [sg.ProgressBar(100, orientation='h', size=(46, 20),
                        key='-PROGRESS_BAR-')],
    ]

    window = sg.Window('R2R-PDF', layout)
    return window


def start(window):
    start_button = window.FindElement('Iniciar')

    while True:
        event, values = window.Read()

        if event == 'Verificar Arquivos':

            # totalPaths = len(paths)
            # namesPDF = map(lambda x: {"name": x["name"]}, paths)

            # sg.popup_scrolled(
            #     "Total de Arquivos Encontrados: ",
            #     totalPaths,
            #     tabulate(namesPDF),
            #     size=(50, 10)
            # )
            # start_button.Update(disabled=False)

            try:
                selected_folder = values['-PATH-']
                thread = threading.Thread(
                    target=getPDFByPath,
                    name="getPDFByPath",
                    args=(selected_folder, window),
                    daemon=True)

                thread.start()

            except Exception as err:
                sg.Popup('Ocorreu um erro!', err)

        elif event == 'Iniciar':
            try:
                progress_value = 100 / totalPaths
                thread = threading.Thread(
                    target=rename,
                    name="rename-pdf",
                    args=(paths, window, progress_value),
                    daemon=True)

                thread.start()

            except Exception as err:
                sg.Popup('Ocorreu um erro!', err)

        elif event == '-THREAD-':
            print('Todos os arquivos renomeado com sucesso: ', values[event])

        elif event == 'Fechar' or event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    start(window())
