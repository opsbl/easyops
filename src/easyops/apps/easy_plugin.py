from ._base import BaseAppPaths, Path, APP


class PluginApis(BaseAppPaths):
    execute = Path("/", method="POST", desc="execute plugin")


class Plugin(APP):
    paths = PluginApis("plugin")
    name_service = "logic.plugin"

    def execute(self, name, options=None):
        """
        execute plugin
        :param name: plugin name
        :param options:
        :return:
        """
        return self.client.call(self.paths.execute.method, self.paths.execute, json={
            "name": name,
            "inputs": options or {}
        })
