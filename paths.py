import os
from datetime import datetime
import time
from pdf import getPDFname


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
