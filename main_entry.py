from queue import Queue
import threading
import time

from main.gui import launch_gui
from main.splash import show_splash_then


def startup_tasks(progress_queue):
    progress_queue.put(("status", "Initializing Parsely"))
    progress_queue.put(("progress", 10))
    time.sleep(1)

    progress_queue.put(("status", "Loading search engine"))
    progress_queue.put(("progress", 40))
    time.sleep(1)

    progress_queue.put(("status", "Preparing interface"))
    progress_queue.put(("progress", 70))
    time.sleep(1)

    progress_queue.put(("status", "Finalizing startup"))
    progress_queue.put(("progress", 100))
    time.sleep(0.5)


if __name__ == "__main__":
    progress_queue = Queue()

    init_thread = threading.Thread(
        target=startup_tasks,
        args=(progress_queue,),
        daemon=True,
    )
    init_thread.start()

    show_splash_then(
        launch_gui,
        wait_thread=init_thread,
        progress_queue=progress_queue,
    )
