# -*- coding: utf-8 -*-
import copy
import yaml
from ..helper import Path
from ..openapi import OpenApi
from ..org_client import OrgClient

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


class BaseAppPaths(object):
    _app_name = ""
    base_url = None
    default_app_name = ""

    def __init__(self, app_name=None, relative=False):
        """
        initialize
        :param app_name: Application Name
        :param relative: Relative paths, do not add '/' before the path
        """
        self._relative = relative

        self.app_name = app_name or self.default_app_name

    @property
    def app_name(self):
        return self._app_name

    @app_name.setter
    def app_name(self, val):
        self._app_name = val
        self.base_url = self._app_name if self._relative else ("/%s" % self._app_name)

    def get_all_paths(self):
        """
        Get all paths under the current instance
        :return:
        """
        return {
            name: getattr(self, name)
            for name in set(dir(self)) ^ set(dir(object))
            if isinstance(getattr(self, name), Path)
        }

    def generate_openapi_configs(self, service_name, host="", app_name=None,
                                 default_frequency=None,
                                 custom_frequency=None,
                                 app_route=False):
        """
        Openapi configuration required to produce the current APP
        :param service_name: service name. eg. logic.cmdb_service
        :param host: http host
        :param app_name: default self.default_app_name
        :param default_frequency: Global API request frequency, the default frequency defined by the Path object is used
        :param custom_frequency: is a dictionary that customizes the request frequency of some APIs:
            {"name": 123, "name2": 1200}
        :param app_route: Whether to add the app_route field
        :return:
        """
        custom_frequency = custom_frequency or {}
        app_name = app_name or self.app_name
        assert isinstance(custom_frequency, dict)
        assert app_name
        configs = []
        for name, path in self.get_all_paths().items():
            info = path.info
            if name in custom_frequency:
                frequency = custom_frequency[name]
                assert isinstance(frequency, int)
                info.update(frequency=frequency)
                configs.append(info)
                continue
            if default_frequency is not None:
                assert isinstance(default_frequency, int)
                info.update(frequency=default_frequency)
                configs.append(info)
                continue

            configs.append(info)

        data = {
            "app_name": app_name,
            "host": host,
            "service_name": service_name,
            "api_list": configs,
        }

        if app_route:
            data = {"app_route": [data]}
        else:
            data = [data]
        return yaml.safe_dump(data, default_flow_style=False, sort_keys=True, explicit_start=True)

    @classmethod
    def extend_paths(cls, paths):
        """
        extended paths
        :param paths: []
            e.g. [
                {"name": "path_name", "path": "path", "method": "POST", "desc": "describe"}
            ]
        :return:
        """
        for item in paths:
            name = item["name"]
            path = item["path"]
            method = item.get("method", "GET")
            desc = item.get("desc", "")
            setattr(cls, name, Path(path, method=method, desc=desc))

    def __str__(self):
        return "<%s app='%s'>" % (self.__class__.__name__, self.app_name)

    __repr__ = __str__


class APP(object):
    host = ""  # type: str  # for org universal_client
    paths = BaseAppPaths("")  # type: BaseAppPaths

    # Name service
    name_service = ""

    def __init__(self, client, app_name=None, host=None):
        self.paths = copy.deepcopy(self.paths)
        self.client = client
        if isinstance(client, OpenApi):
            self.app_name = app_name or self.paths.app_name
            assert self.app_name, "invalid app name"
        elif isinstance(client, OrgClient):
            self.app_name = ""
            self.client = client.clone()
            self.client.host = host or self.host
        else:
            raise ValueError("unknown client: %s" % type(client))

        self.paths.app_name = self.app_name

    def _call(self, path, *args, **kwargs):
        """
        make a generic request
        :param path:
        :param kwargs:
        :return:
        """
        return self.client.call(method=path.method, path=path, *args, **kwargs)

    def generate_openapi_configs(self, service_name, host="", app_name=None,
                                 default_frequency=None,
                                 custom_frequency=None,
                                 app_route=False):
        host = host or self.host
        app_name = app_name or self.app_name
        return self.paths.generate_openapi_configs(service_name, host, app_name,
                                                   default_frequency, custom_frequency,
                                                   app_route)

    def __getattr__(self, name):
        if hasattr(self.paths, name) and isinstance(getattr(self.paths, name), Path):
            path = getattr(self.paths, name)

            def call(*args, **kwargs):
                return self._call(path, *args, **kwargs)

            return call
        raise ValueError("no method named '%s'" % name)
