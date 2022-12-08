# -*- coding: utf-8 -*-
import sys
import time
import hmac
import hashlib
import requests
import warnings
from ..common import logger
from ..exceptions import ValidError
from ..helper import get_application_by_name

try:
    from urllib.parse import unquote_plus
except ImportError:
    from urllib import unquote_plus

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding("utf-8")


class OpenApi(object):
    logger = logger

    def __init__(self, server, access_key, secret_key, valid=True, skip_ssl=False, **kwargs):
        """
        :param server: platform address, e.g. http[s]://192.168.234.143
        :param access_key: API Gateway access key
        :param secret_key: API Gateway secret key
        :param valid: Verify that the return code is equal to 0, otherwise a ValidError will be thrown
        :param skip_ssl: Ignore SSL certificate errors
        """
        self._access_key = access_key
        self._secret_key = secret_key
        self._base_url = server.rstrip("/")
        self._headers = {
            "Host": "openapi.easyops-only.com",
            "User-Agent": "OpenApi/Client"
        }
        self._kwargs = kwargs
        if "debug" in self._kwargs:
            warnings.warn("The 'debug' parameter is deprecated, "
                          "use 'easyops.set_debug()' instead", DeprecationWarning, 2)
        self._valid = valid
        self._skip_ssl = skip_ssl

    @property
    def server(self):
        return self._base_url

    def get_application(self, name, new_name=None):
        """
        根据名称获取APP实例
        :param name:
        :param new_name: 使用新的app名称
        :return:
        """
        app = get_application_by_name(name)
        return app(self, new_name or name)

    def sign(self, request):  # type: (OpenApi, requests.PreparedRequest) -> requests.PreparedRequest
        """
        签名
        :param request:
        :return:
        """
        split = request.path_url.split("?", 1)
        url, params_string = split if len(split) == 2 else (split[0], "")
        params = {}
        if params_string:
            for item in params_string.split("&"):
                key, value = item.split("=", 1)
                key, value = unquote_plus(key), unquote_plus(value)
                params[key] = value

        sign_params = "".join(["%s%s" % (key, params[key]) for key in sorted(params.keys())])

        content_type = request.headers.get("Content-Type", "")
        content_md5 = ""
        if request.body:
            md5 = hashlib.md5()
            md5.update(request.body)
            content_md5 = md5.hexdigest()
        request.headers["Content-MD5"] = content_md5
        timestamp = int(time.time())
        raw_string = "\n".join(map(str, [
            request.method,
            url,
            sign_params,
            content_type,
            content_md5,
            timestamp,
            self._access_key,
        ]))

        signature = hmac.new(self._secret_key.encode(), raw_string.encode("utf-8"), hashlib.sha1).hexdigest()
        self.logger.debug("Signature original string: \n------Start------\n%s\n------End------", raw_string)
        self.logger.debug("Signature result: %s", signature)

        request.prepare_url(request.url, {
            "accesskey": self._access_key,
            "signature": signature,
            "expires": timestamp,
        })
        return request

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
            session.headers.update(self._headers)

            stream = kwargs.pop("stream", None)
            verify = kwargs.pop("verify", not self._skip_ssl)
            cert = kwargs.pop("cert", None)

            request = requests.Request(method=method,
                                       url=url,
                                       *args,
                                       **kwargs)
            prep = session.prepare_request(request)
            self.sign(prep)

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
            self.logger.debug("%s Request: \n"
                              "\tURL: %s\n"
                              "\tMethod: %s\n"
                              "\tHeaders: %s\n"
                              "\tBody: %s\n", self.__class__.__name__, prep.url, prep.method, prep.headers, prep.body)
            resp = session.send(prep, **send_kwargs)
            self.logger.debug("%s Response: \n"
                              "\tHttpStatus: %s\n"
                              "\tHeaders: %s\n"
                              "\tBody: %s\n", self.__class__.__name__,
                              resp.status_code,
                              resp.headers,
                              resp if response else resp.text)
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
