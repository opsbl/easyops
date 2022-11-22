# coding: utf-8


import io

from ..helper import types
from ._base import BaseAppPaths, Path, APP


class ToolPaths(BaseAppPaths):
    tools = Path("/tools", method="GET", desc="Get a list of tools")
    categories = Path("/tools/v2/categories", method="GET", desc="Get categories")

    create = Path("/tools", method="POST", desc="Create tool")
    update = Path("/tools/{tool_id}", method="PUT", desc="Modify the tool")
    delete = Path("/tools/{tool_id}", method="DELETE", desc="Delete the tool")

    detail = Path("/tools/{tool_id}", method="GET", desc="Gets the tool information")

    versions = Path("/tools/{tool_id}/versions", method="GET", desc="Query the tool version list")
    approval = Path("/tools/{tool_id}/changeEnvType", method="POST", desc="Tools for examination and approval of")

    lib_create = Path("/tools/lib", method="POST", desc="Create a tool dynamic library")
    lib_delete = Path("/tools/lib/{id}", method="DELETE", desc="Delete a tool dynamic library")
    lib_update = Path("/tools/lib/{id}", method="PUT", desc="Update a tool dynamic library")
    lib_export = Path("/api/tools/v1/libs/export/{id}", method="GET", desc="Export a tool dynamic library")
    lib_import = Path("/api/tools/v1/libs/import", method="POST", desc="Import a tool dynamic library")

    import_tool = Path("/tools/import", method="POST", desc="Import tools")
    export_tool = Path("/tools/{tool_id}/export", method="POST", desc="Export tools")

    exec_pre_check = Path("/tools/execution/preCheck", method="POST", desc="tools to perform before the examination")
    exec_callback = Path("/tools/execution/callback", method="POST", desc="Performs a tool callback")
    exec_debug = Path("/tools/debug", method="POST", desc="The execution of a debugging tool")
    terminate = Path("/tools/terminate/{task_id}", method="PUT", desc="Terminates an ongoing task")
    logs_by_exec_id = Path("/tools/execution/logs/{exec_id}", method="GET",
                           desc="According to the execId bulk access tool execution log")
    exec_snapshot = Path("/tools/execution/snapshot", method="POST", desc="Snapshot before tool execution")
    result_form_table = Path("/tools/execution/{exec_id}/table", method="GET",
                             desc="Access tools to perform table results")
    execution = Path("/tools/execution", method="POST", desc="execution tool")
    result_to_excel = Path("/tools/execution/{exec_id}/table/export", method="GET",
                           desc="Export the output table of the tool execution results")
    result_to_csv = Path("/tools/execution/csv/{exec_id}/table/export", method="GET",
                         desc="Export the tool execution results to a CSV file")
    debug_snapshot = Path("/tools/debug/snapshot", method="POST", desc="An execution snapshot of the debugging tool")
    result_list = Path("/tools/result/list", method="GET", desc="Get Tool execution results in bulk")
    result = Path("/tools/execution/{exec_id}", method="GET", desc="Gets the results of tool execution")

    def __init__(self, app_name="tool"):
        super(ToolPaths, self).__init__(app_name, relative=False)


class Tool(APP):
    host = "tool.easyops-only.com"
    paths = ToolPaths("tool")

    def tools(self, page=1, page_size=10, category=None, name=None, permissions="ignoreWhiteList", plugin=False,
              type=None, view_whitelist=None, **kwargs):
        """
        Get a list of tools
        :param page:
        :param page_size:
        :param category:
        :param name:
        :param permissions:
        :param plugin:
        :param type:
        :param view_whitelist:
        :param kwargs:
        :return:
        """
        return self.client.get(self.paths.tools, params=dict(
            page=page,
            pageSize=page_size,
            category=category,
            name=name,
            permissions=permissions,
            plugin=plugin,
            type=type,
            viewWhitelist=view_whitelist,
            **kwargs
        ))

    def categories(self, **params):
        return self.client.get(self.paths.categories, params=params)

    def execution(self, **options):
        """

        http[s]://DOMAIN/next/developers/providers-v2/tool?group=execute&api-name=execute-tool&debugger-expand=0
        :param options:
        :return:
        """
        return self.client.post(self.paths.execution, json=options)

    def export_result_to_file(self, exec_id, dest, close=True):
        """
        Export results to excel sheet, Support BytesIO
        :param exec_id:
        :param dest:
        :param close:
        :return:
        """
        resp = self.client.get(self.paths.result_to_excel, url_params={"exec_id": exec_id}, response=True)
        if isinstance(dest, (str, types.bytes)):
            with open(dest, "wb+") as fd:
                fd.write(resp.content)
            return
        elif isinstance(dest, (io.IOBase, types.file)):
            dest.write(resp.content)
            if close:
                dest.close()

        raise ValueError(dest)

    def terminate(self, task_id):
        return self.client.put(self.paths.terminate, url_params={"task_id": task_id})

    def logs_by_exec_id(self, exec_id):
        return self.client.get(self.paths.logs_by_exec_id, url_Params={"exec_id": exec_id})

    def detail(self, tool_id):
        return self.client.get(self.paths.detail, url_params={"tool_id": tool_id})
