import os
import time
import timeit
from pdf import getPDFname, getLocalTime
from pathlib import Path


def getPDFByPath(selected_folder, window):
    files = Path(selected_folder)

    paths_filtered_by_PDF = map(lambda file: {
        "name": file.name,
        "path": file,
        "root": file.parent
    }, files.rglob("*.pdf"))

    window.write_event_value('-THREAD_GET_PDF_BY_PATH-', paths_filtered_by_PDF)


def rename(oldPaths, window):
    timer_start = timeit.default_timer()

    totalPaths = len(oldPaths)

    progress_value = 0

    for file in oldPaths:
        progress_value += 100 / totalPaths
        oldNameFile = file["name"]
        oldPathFile = file["path"]
        oldRootFile = file["root"]

        newNameFile = getPDFname(oldPathFile)
        newPathFile = os.path.join(oldRootFile, newNameFile + ".pdf")

        if os.path.exists(newPathFile):
            time.sleep(1)
            localtime = getLocalTime()

            newPathFile = os.path.join(
                oldRootFile,
                newNameFile
                + ' - '
                + localtime
                + ".pdf"
            )

        print(
            'Nome: '
            + oldNameFile
            + ' ----> '
            + newNameFile
            + ".pdf"
            + '\n'
        )

        os.rename(oldPathFile, newPathFile)
        window.write_event_value('-PROGRESS-', progress_value)

    timer_stop = timeit.default_timer()
    window.write_event_value('-THREAD_DONE-', (timer_stop - timer_start))
