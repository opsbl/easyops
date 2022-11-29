# -*- coding: utf-8 -*-

from ._base import APP, BaseAppPaths, Path


class SchedulerPaths(BaseAppPaths):
    default_app_name = "scheduler"

    tasks_list = Path("/api/v1/scheduler/task", method="GET", desc="Get task list")
    create_task = Path("/api/v1/scheduler/task", method="POST", desc="Create a scheduled task")
    update_task = Path("/api/v1/scheduler/task/{task_id}", method="PUT", desc="Update scheduled tasks")
    delete_task = Path("/api/v1/scheduler/task/{task_id}", method="DELETE", desc="Delete scheduled tasks")


class Scheduler(APP):
    paths = SchedulerPaths()
    name_service = "logic.scheduler"

    def create_task(self, options):
        """
        Create a scheduled task
        :return:
        """
        return self._call(self.paths.create_task, json=options)

    def delete_task(self, task_id):
        return self._call(self.paths.delete_task.fill_params(task_id=task_id))

    def update_task(self, task_id, data):
        return self._call(self.paths.update_task.fill_params(task_id=task_id), json=data)

    def get_tasks(self, **body):
        return self._call(self.paths.tasks_list, params=body, response=True).json()
