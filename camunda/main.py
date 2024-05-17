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

    worker1.subscribe(
        topic='processVoltage',
        func=process_voltage,
        variables=["data"]
    )
    worker1.subscribe(
        topic='processCurrent',
        func=process_current,
        variables=["data"]
    )
    worker1.run()


if __name__ == '__main__':
    main()