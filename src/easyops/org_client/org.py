# -*- coding: utf-8 -*-
import sys
import copy
import requests
from ..exceptions import ValidError
from ..helper import get_application_by_name

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding("utf-8")


class OrgClient(object):
    def __init__(self, server, org, user, host="localhost", debug=False, valid=True, skip_ssl=False):
        self._base_url = server.rstrip("/")
        self._host = host
        self._org = org
        self._user = user
        self._debug = debug
        self._valid = valid
        self._skip_ssl = skip_ssl
        self._headers = {
            "Org": str(org),
            "User": self._user,
            "User-Agent": "Org/Client"
        }
        if self._host:
            self._headers["Host"] = self._host

    @property
    def server(self):
        return self._base_url

    def clone(self):
        """
        copy the current instance
        :return:
        """
        return copy.deepcopy(self)

    def get_application(self, name, server=None, host=None, user=None, org=None, **ops):
        """
        Get APP instance
        :param name: app name
        :param server: ip address or hostname
        :param host: The `Host` parameter in the request header
        :param user: The `User` parameter in the request header
        :param org: The `Org` parameter in the request header
        :param ops: options
        :return:
        """
        app = get_application_by_name(name)
        if app is None:
            raise ValueError("%s app does not exist" % name)
        server = server or self._base_url
        host = host or app.host
        user = user or self.user
        org = org or self._org

        default = {
            "debug": self._debug,
            "valid": self._valid,
            "skip_ssl": self._skip_ssl,
        }
        default.update(ops)
        client = self.__class__(server, host, org, user, **default)
        return app(client)

    def debug(self, msg, *args, **kwargs):
        """
        日志输出
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """

        if not self._debug:
            return
        msg = str(msg)
        end = kwargs.pop("end_", "\n")
        sys.stderr.write(msg.format(*args, **kwargs) + end)
        sys.stderr.flush()

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, val):
        self._host = val
        self._headers.update({
            "Host": self._host,
        })

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, val):
        self._user = val
        self._headers.update({
            "User": self._user,
        })

    def call(self, method, path, *args, **kwargs):
        """
        发出请求
        :param method:
        :param path:
        :param args:
        :param kwargs:
        :return:
        """
        response = kwargs.pop("response", False)  # Return the response object directly
        if hasattr(path, "fill_params"):
            url = self._base_url + path.fill_params(**kwargs.pop("url_params", {}))
        else:
            url = self._base_url + path
        with requests.Session() as session:
            session.verify = not self._skip_ssl
            session.headers.update(self._headers)

            stream = kwargs.pop("stream", None)
            verify = kwargs.pop("verify", None)
            cert = kwargs.pop("cert", None)

            request = requests.Request(method=method,
                                       url=url,
                                       *args,
                                       **kwargs)

            prep = session.prepare_request(request)

            proxies = session.proxies or {}

            settings = session.merge_environment_settings(
                prep.url, proxies,
                stream,
                verify,
                cert,
            )

            # Send the request.
            send_kwargs = {
                'timeout': kwargs.pop("timeout", None),
                'allow_redirects': kwargs.pop("allow_redirects", True),
            }
            send_kwargs.update(settings)
            self.debug("Request: \n"
                       "\tURL: {}\n"
                       "\tMethod: {}\n"
                       "\tHeaders: {}\n"
                       "\tBody: {}\n", prep.url, prep.method, prep.headers, prep.body)
            resp = session.send(prep, **send_kwargs)
            self.debug("Response: \n"
                       "\tHttpStatus: {}\n"
                       "\tHeaders: {}\n"
                       "\tBody: {}\n", resp.status_code, resp.headers, resp if response else resp.text)

            if response:
                if self._valid and (resp.status_code >= 300 or resp.status_code < 200):
                    raise ValidError(code=-1, message="Response is not OK", data=resp)
                return resp
            full_data = resp.json()
            code = full_data.get("code")
            data = full_data.get("data")
            message = full_data.get("error") or full_data.get("message")

            if self._valid and code != 0:
                raise ValidError(code=code, message=message, data=data)

            return data

    def get(self, path, *args, **kwargs):
        return self.call("GET", path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.call("POST", path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.call("DELETE", path, *args, **kwargs)

    def update(self, path, *args, **kwargs):
        return self.call("UPDATE", path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return self.call("PUT", path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return self.call("PATCH", path, *args, **kwargs)

    def option(self, path, *args, **kwargs):
        return self.call("OPTION", path, *args, **kwargs)
