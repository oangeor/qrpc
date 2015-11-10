# coding=utf-8
import abc
import json

import six

from qrpc.job import Job


@six.add_metaclass(abc.ABCMeta)
class SchedulerBase(object):
    @abc.abstractmethod
    def add_request(self, req):
        """
        an abstract method need to be implemented
        """

    @abc.abstractmethod
    def get_result(self):
        """
        an abstract method need to be implemented
        """


class SchedulerBatch(SchedulerBase):
    def __init__(self, server_proxy):
        self._job_list = []
        self._server_proxy = server_proxy
        self.evaluated = False

    def add_request(self, req):
        job = Job(req=req)
        self._job_list.append(job)
        return job

    def get_result(self, job):
        self.evaluate()
        return job.result

    def evaluate(self):
        if self.evaluated:
            return
        payload = json.dumps([job.req.to_json for job in self._job_list])

        result_list = self._server_proxy.run_request(
            params={
                'requests': payload
            }
        )
        assert len(self._job_list) == len(result_list)

        for job, result in zip(self._job_list, result_list):
            job.result = result
