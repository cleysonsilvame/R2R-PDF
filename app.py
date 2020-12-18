from paths import getPDFByPath, rename
import PySimpleGUI as sg
import threading


def layout():
    sg.theme('Dark Blue 3')
    return [
        [sg.Text('Selecione a pasta para renomear: ')],
        [sg.Input(), sg.FolderBrowse(key='-PATH-')],
        [
            sg.OK('Iniciar', disabled=True),
            sg.OK('Verificar Arquivos', disabled=True),
            sg.OK('Procurar Arquivos'),
            sg.CloseButton('Fechar')
        ],
        [sg.Output(size=(70, 12))],
        [sg.ProgressBar(100, orientation='h', size=(46, 20),
                        key='-PROGRESS_BAR-', visible=True)
         ],
    ]


def start(layout):
    window = sg.Window('Multithreaded Window', layout)
    start_button = window.FindElement('Iniciar')
    verify_button = window.FindElement('Verificar Arquivos')
    progress_bar = window.FindElement('-PROGRESS_BAR-')

    paths_filtered_by_PDF = []


# --------------------- EVENT LOOP ---------------------
    while True:

        event, values = window.read()

        if event == 'Procurar Arquivos':
            try:
                print(
                    "# ------------------------------------ PROCURANDO ARQUIVOS ------------------------------------")

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
                print(
                    "# ----------------------------------- RENOMEANDO ARQUIVOS -----------------------------------")

                thread = threading.Thread(
                    target=rename,
                    name="rename-pdf",
                    args=(paths_filtered_by_PDF, window),
                    daemon=True)

                thread.start()

            except Exception as err:
                sg.Popup('Ocorreu um erro!', err)

        elif event == 'Verificar Arquivos':
            string_output = ''

            for item in paths_filtered_by_PDF:
                string_output = string_output + \
                    'Nome -----> ' + str(item["name"]) + '\n'
                string_output = string_output + \
                    'Caminho -----> ' + str(item["path"]) + '\n'
                string_output = string_output + \
                    'Base -----> ' + str(item["root"]) + '\n\n'

            sg.popup_scrolled(
                f"Total de Arquivos Encontrados: {len(paths_filtered_by_PDF)}",
                "\n# ------------------------------------------------------------------------",
                string_output,
                size=(70, 10)
            )

        elif event == '-PROGRESS-':
            start_button.Update(disabled=True)
            verify_button.Update(disabled=True)

            progress = values[event]
            progress_bar.update_bar(progress)

        elif event == '-THREAD_DONE-':
            timer = values[event]

            print('Arquivos renomeados com sucesso: ', timer, '\n')

        elif event == '-THREAD_GET_PDF_BY_PATH-':
            paths_filtered_by_PDF = list(values[event])
            totalPaths = len(paths_filtered_by_PDF)

            print('O total de arquivos encontrados foi:', totalPaths, '\n')

            start_button.Update(disabled=False)
            verify_button.Update(disabled=False)

        elif event == 'Fechar' or event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    start(layout())
