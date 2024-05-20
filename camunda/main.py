import threading
import pycamunda.processdef
import pycamunda.variable
from worker import Worker
from external_tasks_tidit import process_voltage, process_current

url = 'http://localhost:8088/engine-rest'
process_key = "tidit_id"
worker_id = "1"


def main():

    start_instance = pycamunda.processdef.StartInstance(url=url, key=process_key)
    start_instance()

    worker1 = Worker(url=url, worker_id=worker_id)
    worker2 = Worker(url=url, worker_id='2')

    worker1.subscribe(
        topic='processVoltage',
        func=process_voltage,
        variables=["data"]
    )
    worker2.subscribe(
        topic='processCurrent',
        func=process_current,
        variables=["data"]
    )

    thread1 = threading.Thread(target=worker1.run)
    thread2 = threading.Thread(target=worker2.run)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


if __name__ == '__main__':
    main()