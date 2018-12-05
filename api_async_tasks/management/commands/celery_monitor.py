from celery import Celery
from django.core.management import BaseCommand

from api_async_tasks.models import Problem


def my_monitor(app):
    state = app.events.State()

    def update_task_status(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        try:
            task = state.tasks.get(event['uuid'])
            p, created = Problem.objects.get_or_create(task_id=task.uuid)
            p.status = event['state']
            # p.problem_type = task.name
            try:
                p.result = event['result']
            except KeyError:
                p.result = None
            p.save()
            print(f'TASK EVENT HAPPENED {event}: %s[%s] %s' % (
                task.name, task.uuid, task.info(),))
        except Exception as e:
            print(e)

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
            'task-sent': update_task_status,
            'task-received': update_task_status,
            'task-started': update_task_status,
            'task-succeeded': update_task_status,
            'task-failed': update_task_status,
            'task-rejected': update_task_status,
            'task-revoked': update_task_status,
            'task-retried': update_task_status,
            # '*': state.event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


class Command(BaseCommand):
    def handle(self, **options):
        app = Celery('tasks_project', broker='amqp://localhost')
        my_monitor(app)
