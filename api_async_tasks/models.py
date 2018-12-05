import uuid
from enum import Enum

from celery.result import AsyncResult
from django.contrib.postgres.fields import JSONField
from django.db import models
from api_async_tasks.tasks import integration, prime_factoring

# Create your models here.
from tasks_project.settings import INTEGRATE_TASK_NAME, PRIME_FACTORING_TASK_NAME


class ProblemType(Enum):
    integrate = INTEGRATE_TASK_NAME
    prime_factoring = PRIME_FACTORING_TASK_NAME


class Problem(models.Model):
    task_id = models.UUIDField(unique=True, default=uuid.uuid4,
                               editable=False)
    problem_type = models.CharField(max_length=256, choices=[(x.value, x.value) for x in ProblemType])
    argument = JSONField(max_length=256)

    @property
    def result_realtime(self):
        """
        Obtains the result on the fly from the result backend
        :return:
        """
        result = AsyncResult(str(self.task_id))
        return str(result.result)

    @property
    def state_realtime(self):
        """
        Obtains the status of the task on the fly from the result backend
        :return:
        """
        result = AsyncResult(str(self.task_id))
        return str(result.state)
