import pycamunda.externaltask
import json


class ExternalTaskException(Exception):
    def __init__(self, *args, message, details='', retry_timeout=15000, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.details = details
        self.retry_timeout = retry_timeout


class Worker:

    def __init__(self, url, worker_id, max_tasks=5, async_response_timeout=15000):
        self.fetch_and_lock = pycamunda.externaltask.FetchAndLock(
            url, worker_id, max_tasks, async_response_timeout=async_response_timeout
        )
        self.complete_task = pycamunda.externaltask.Complete(
            url, id_=None, worker_id=worker_id
        )
        self.handle_failure = pycamunda.externaltask.HandleFailure(
            url,
            id_=None,
            worker_id=worker_id,
            error_message='',
            error_details='',
            retries=5,
            retry_timeout=5000
        )

        self.stopped = False
        self.topic_funcs = {}

    def subscribe(self, topic, func, lock_duration=5000, variables=None):
        self.fetch_and_lock.add_topic(topic, lock_duration, variables)
        self.topic_funcs[topic] = func

    def run(self):
        self.stopped = False
        while not self.stopped:
            tasks = self.fetch_and_lock()
            # if not tasks:
            #     self.stopped = True
            for task in tasks:
                try:
                    return_variables = self.topic_funcs[task.topic_name](task.variables)
                except ExternalTaskException as exc:
                    self.handle_failure.id_ = task.id_
                    self.handle_failure.error_message = exc.message
                    self.handle_failure.error_details = exc.details
                    self.handle_failure.retry_timeout = exc.retry_timeout
                    if task.retries is None:
                        self.handle_failure.retries = 3
                    else:
                        self.handle_failure.retries = task.retries - 1
                    self.handle_failure()
                else:
                    self.complete_task.variables = {}
                    self.complete_task.id_ = task.id_
                    if return_variables:
                        for key, value in return_variables.items():
                            string_value = json.dumps(value)
                            self.complete_task.add_variable(name=key, value=string_value, type_="Json")
                    self.complete_task()