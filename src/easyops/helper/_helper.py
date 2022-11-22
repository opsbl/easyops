# coding: utf-8
import importlib

from io import BytesIO
from . import _apps as apps

import yaml

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


class Path(object):
    """
    该类实现url path拼接, 以及参数填充(参数填充仅支持format方式), 完整url拼接
    example:
        单Path使用
        p1 = Path("/a/b/")
        p2 = p1 / "tom" # => <Path path='/a/b/tom',desc=''>

        p3 = Path("/a/b/{id}")
        url = "https://domain.cn" + p3.fill_params(id=1)    # url = https://domain.cn/a/b/1

        以类的方式获取简化URL管理
        class Urls(object):
            a = Path("/a")
            b = Path("/b")
            c = a / b
            def __init__(self):
                self.base_url = "https://domain.cn"

        urls = Urls()
        urls.a  # => <Path path='https://domain.cn/a',desc='full url'>
        urls.b  # => <Path path='https://domain.cn/b',desc='full url'>
        urls.c  # => <Path path='https://domain.cn/a/b',desc='full url'>

    """

    def __init__(self, path, desc="", method=None):
        self.desc = desc
        self.method = method or "GET"
        self.__path = path.strip()
        self._frequency = 120
        self.raw = None

    @property
    def path(self):  # type: ()->str
        return self.__path

    def full_url(self, base, *args, **kwargs):
        """
        完整的URL
        :param base: url前缀. example: https://domain.cn
        :param args: url位置参数
        :param kwargs: url具名参数
        :return:
        """
        return base + self.fill_params(*args, **kwargs)

    def get_params(self):
        """
        Get path parameters
        :return:
        """

    def fill_params(self, *args, **kwargs):
        """
        填充路径参数
        :param args:
        :param kwargs:
        :return:
        """
        if not args and not kwargs:
            return self.__class__(self.__path, method=self.method, desc=self.desc)
        path = self.__path.format(*args, **kwargs)
        return self.__class__(path, method=self.method, desc=self.desc)

    def __div__(self, other):
        if isinstance(other, (str, self.__class__)):
            path = self.path + "/" if not self.path.endswith("/") else self.path
            return self.__class__(path + str(other).lstrip("/"))
        else:
            raise ValueError("can only be of type 'str' or type '%s'" % self.__class__.__name__)

    def __truediv__(self, other):
        return self.__div__(other)

    def __radd__(self, other):
        return other + self.__str__()

    def __repr__(self):
        return "<Path path='%s',desc='%s'>" % (self.path, self.desc)

    def __str__(self):
        return self.path

    def __get__(self, instance, owner):
        if hasattr(instance, "base_url"):
            url = self.__class__(instance.base_url) / self
            url.desc = self.desc
            url.method = self.method
            url.raw = self
            return url
        else:
            return self

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        assert isinstance(value, int)
        self._frequency = value

    @property
    def info(self):
        path = self.raw if self.raw else self
        return {
            "method": path.method,
            "frequency": path.frequency,
            "uri": path.__path
        }

    def generate_openapi_config(self, frequency=None):
        """
        Generate openapi configuration。
            api_list:
                - frequency: 120
                  method: POST
                  uri: a/b/c/
        :return:
        """
        frequency = self.frequency if frequency is None else int(frequency)
        info = self.info
        info.update(frequency=frequency)
        with BytesIO() as buf:
            buf.write(b"# {} \n".format(self.desc.encode("utf-8")))
            yaml.dump([info], buf, Dumper, default_flow_style=False)
            return buf.getvalue()


class BaseUrls(object):
    def __init__(self, host, port=None, tls=False):
        schemas = "https" if tls else "http"
        port = (443 if tls else 80) if port is None else port
        self.base_url = "{schemas}://{host}:{port}".format(host=host, port=port, schemas=schemas)

    def __str__(self):
        return "{}.{}(url=\"{}\")".format(self.__class__.__module__, self.__class__.__name__, self.base_url)

    __repr__ = __str__


def get_application_by_name(name):
    """
    Get the APP class
    :param name:
    :return:
    """
    if not hasattr(apps, name):
        raise ValueError("App '%s' does not exist" % name)
    full = getattr(apps, name)
    pkg, cls = full.rsplit(".", 1)
    module = importlib.import_module(pkg)

    return getattr(module, cls)
