import time
import timeit
from handlerPdf import getPDFname, getLocalTime
from pathlib import Path, PurePath


def getPDFByPath(selected_folder, window):
    files = Path(selected_folder)

    paths_filtered_by_PDF = map(lambda file: {
        "name": file.name,
        "path": file,
        "root": file.parent
    }, files.rglob("*.pdf"))

    window.write_event_value('-THREAD_GET_PDF_BY_PATH-', paths_filtered_by_PDF)


def setPDFName(oldPaths, window):
    timer_start = timeit.default_timer()

    totalPaths = len(oldPaths)

    progress_value = 0

    for file in oldPaths:
        progress_value += 100 / totalPaths
        oldNameFile = file["name"]
        oldPathFile = Path(file["path"]).resolve()
        oldRootFile = Path(file["root"]).resolve()

        newNameFile = getPDFname(oldPathFile)

        newPathFile = Path(oldRootFile, newNameFile + ".pdf").resolve()

        if newPathFile.exists():
            time.sleep(1)
            localtime = getLocalTime()

            newNameFile += ' - ' + localtime

            newPathFile = Path(
                oldRootFile,
                newNameFile
                + ".pdf"
            ).resolve()

        print(
            'Nome: '
            + oldNameFile
            + ' ----> '
            + newNameFile
            + ".pdf"
            + '\n'
        )

        oldPathFile.rename(newPathFile)
        window.write_event_value('-PROGRESS-', progress_value)

    timer_stop = timeit.default_timer()
    window.write_event_value('-THREAD_DONE-', (timer_stop - timer_start))
