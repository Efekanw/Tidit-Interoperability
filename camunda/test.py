import pycamunda.processdef
import pycamunda.variable
from worker import Worker
import docker
import os
from external_tasks import insert_car, insert_person, start_fuseki, detect_object, select_object


url = 'http://localhost:8088/engine-rest'
process_key = "sayac"
worker_id = "1"


def main():
    dir_path = os.path.join(os.path.dirname(__file__), 'images')
    print(dir_path)

    client_d = docker.from_env()

    # anahtar_listesi = detect_object(client, dir_path)

    # process_objects(anahtar_listesi)

    start_instance = pycamunda.processdef.StartInstance(url=url, key=process_key)

    start_instance()

    worker1 = Worker(url=url, worker_id=worker_id)

    worker1.subscribe(
        topic='selectObject',
        func=select_object,
    )
    worker1.subscribe(
        topic='detectObject',
        func=detect_object,
    )
    worker1.subscribe(
        topic='insertPerson',
        func=insert_person,
        variables=["person"]
    )
    worker1.subscribe(
        topic='insertCar',
        func=insert_car,
        variables=["car"]
    )
    worker1.subscribe(
        topic='startFuseki',
        func=start_fuseki,
        variables=["fuseki"]
    )
    worker1.run()


if __name__ == '__main__':
    main()