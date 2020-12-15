import asyncio
from paths import test
from multiprocessing.pool import ThreadPool

import PySimpleGUI as sg

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


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


async def gui_window_loop(window):
    while True:
        event, values = window.Read(0)

        if event == "__TIMEOUT__":
            continue

        if event == 'Verificar Arquivos':
            try:
                pool = ThreadPool(processes=1)


                async_test = pool.apply_async(test)

                # thread = threading.Thread(
                #     target=test,
                #     name="rename-pdf",
                #     args=(),
                #     daemon=True)

                # thread.start()
                print(async_test.get())

            except Exception as err:
                sg.Popup('Ocorreu um erro!', err)

        if event == "Exit" or event == None:
            break


try:
    window_main = asyncio.ensure_future(gui_window_loop(window()))


    loop.run_forever()

except:

    canceltasks = [task.cancel() for task in asyncio.all_tasks()]

    try:

        print(f"cancelling {len(canceltasks)} tasks")

        loop.run_until_complete(asyncio.wait(canceltasks, timeout=10))

    except asyncio.TimeoutError:

        print("timeout when trying to cancel running tasks")

finally:

    print("closing loop")

    loop.close()

# main = form.Layout(layout)
