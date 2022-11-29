# -*- coding: utf-8 -*-
from collections import namedtuple

import io
import yaml
from ..helper import types

from ._base import BaseAppPaths, APP, Path

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class ArtifactPaths(BaseAppPaths):
    default_app_name = "artifact"

    package_search = Path("/package/search", method="GET", desc="search package")

    package_download = Path("/archive/{package_id}/{version_id}", method="GET", desc="download package")

    version_list = Path("/version/list", method="GET", desc="version list")
    version_detail = Path("/version/version/{version_id}", method="GET", desc="version detail")

    packages_bind = Path("/api/artifact/v1/apps/{app_id}/packages/{package_id}/bind", method="POST",
                         desc="Quickly bind packages and configuration packages")


class PackageVersion(object):
    ENV_DEVELOP = 1
    ENV_TEST = 3
    ENV_PRE_RELEASE = 7
    ENV_PRODUCTION = 15

    ENVS = {
        1: "DEVELOP",
        3: "TEST",
        7: "PRE_RELEASE",
        15: "PRODUCTION",
    }

    def __init__(self, attr, client=None):
        self._attrs = attr
        self._client = client  # type: Artifact

    @property
    def attrs(self):
        return self._attrs

    @property
    def name(self):
        return self._attrs["name"]

    def __getattr__(self, name):
        return self._attrs[name]

    @property
    def version_id(self):
        return self._attrs["versionId"]

    @property
    def package_id(self):
        return self._attrs["packageId"]

    @property
    def memo(self):
        return self._attrs["memo"]

    @property
    def info(self):
        return self._client.get_version_detail(self.version_id)

    @property
    def conf(self):
        conf = self._attrs["conf"]
        return yaml.load(conf, Loader)

    def download(self, filename, chunk_size=512, hook=None, **opts):
        return self._client.download(self.package_id, self.version_id, filename, chunk_size=chunk_size, hook=hook,
                                     **opts)

    def env_display(self):
        env = int(self._attrs["env_type"])
        if env in self.ENVS:
            return self.ENVS[env]
        return "Unknown"

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.name)

    __str__ = __repr__


class Package(object):
    def __init__(self, attrs, client=None):
        self._attrs = attrs
        self._client = client  # type: Artifact

    @property
    def attrs(self):
        return self._attrs

    def __getattr__(self, name):
        return self._attrs[name]

    @property
    def name(self):
        return self._attrs["name"]

    @property
    def package_id(self):
        return self._attrs["packageId"]

    @property
    def install_path(self):
        return self._attrs["installPath"]

    @property
    def platform(self):
        return self._attrs["platform"]

    @property
    def user(self):
        return self._attrs["user"]

    @property
    def latest_version(self):
        info = self._attrs["lastVersionInfo"]
        if info:
            info["packageId"] = self.package_id
        return PackageVersion(info, self._client)

    def get_versions(self, page=1, page_size=20, order=None, env_type=None, **query):
        return self._client.get_package_versions(self.package_id, page=page, page_size=page_size, order=order,
                                                 env_type=env_type, **query)

    def get_latest_version(self, env_type=None):  # type: (int)->PackageVersion|None
        """
        获取最新版本
        :param env_type:
        :return:
        """
        resp = self._client.get_package_versions(self.package_id, env_type=env_type, order="ctime desc")
        if resp.total == 0:
            return None
        return resp.list[0]

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.name)

    __str__ = __repr__


class Artifact(APP):
    ENV_DEVELOP = 1
    ENV_TEST = 3
    ENV_PRE_RELEASE = 7
    ENV_PRODUCTION = 15

    PKG_APP = 1  # 应用包
    PKG_CONF = 2  # 配置包
    PKG_FILE = 4  # 文件包

    host = "deploy.easyops-only.com"
    paths = ArtifactPaths()
    name_service = "logic.artifact"

    def fast_bind_packages(self, app_id, package_id, **options):
        """
        为APP快速绑定制品包
        :param app_id:
        :param package_id:
        :param options:
        :return:
        """
        return self.client.post(self.paths.packages_bind.fill_params(app_id=app_id, package_id=package_id),
                                json=options)

    def search_packages(self, name=None, exact=False, creator=None, page=1, page_size=20, order=None, **query):
        """
        搜索包
        :param name:
        :param exact:
        :param creator:
        :param page:
        :param page_size:
        :param order:
        :param query:
        :return:
        """
        result = namedtuple("SearchResult", ("total", "list", "page", "page_size"))
        query.update({
            "name": name,
            "exact": exact,
            "creator": creator or "",
            "order": order or "",
            "page": page,
            "pageSize": page_size,
        })
        resp = self.client.call(self.paths.package_search.method, self.paths.package_search, params=query)
        resp["list"] = [Package(i, self) for i in resp["list"]]
        return result(**resp)

    def get_package_versions(self, pkg_id, page=1, page_size=20, order=None, env_type=None, **query):
        """
        获取文件包版本信息
        :param pkg_id:
        :param page:
        :param page_size:
        :param order:
        :param env_type:
        :param query:
        :return:
        """
        result = namedtuple("VersionResult", ("total", "list", "page", "page_size"))
        query.update({
            "packageId": pkg_id,
            "start": 0,
            "order": order or "ctime desc",
            "page": page,
            "env_type": env_type,
            "pageSize": page_size,
        })

        resp = self.client.call(self.paths.version_list.method, self.paths.version_list, params=query)
        resp["list"] = [PackageVersion(i, self) for i in resp["list"]]
        return result(**resp)

    def get_version_detail(self, vid):
        """
        获取版本详细信息
        :param
        vid:
        :return:
        """
        return PackageVersion(self._call(self.paths.version_detail.fill_params(version_id=vid)))

    def get_package_by_name(self, name, type=None):  # type: (str, int)->Package|None
        """
        根据包名获取包
        :param name:
        :param type: 包类型
        :return:
        """
        ret = self.search_packages(name, exact=True, type=type)
        if ret.total == 0:
            return None
        return ret.list[0]

    def download(self, pid, vid, filename, deploy_repo_app_name=None, **opts):
        repo = DeployRepo(self.client, app_name=deploy_repo_app_name)
        return repo.download(pid, vid, filename, **opts)


class DeployRepoPaths(BaseAppPaths):
    default_app_name = "deploy_repo"
    download = Path("/archive/{package_id}/{version_id}", method="GET", desc="Download package")

    archive = Path("/v2/archive")


class DeployRepo(APP):
    host = "deployrepo.easyops-only.com"
    paths = DeployRepoPaths()

    def download(self, pid, vid, filename, encoding=None, path=None, redirect=False, with_package_conf=True,
                 chunk_size=512, hook=None):
        """
        下载版本, 如果filename是IO对象时, 下载完成后会seek(0)
        :param pid: 包ID
        :param vid: 版本ID
        :param filename: 保持文件
        :param encoding: 参数path的编码格式
        :param path: 单独下载指定的文件
        :param redirect: 是否重定向，默认为false
        :param with_package_conf:整包下载的时候，是否带 package.conf.yaml 文件
        :param chunk_size: 块大小
        :param hook: 钩子
        :return:
        """
        _headers_repo = {
            "Host": "deployrepo.easyops-only.com"
        }
        params = {
            "encoding": encoding,
            "path": path,
            "redirect": redirect,
            "withPackageConf": with_package_conf,
        }
        path = self.paths.download.fill_params(package_id=pid, version_id=vid)

        if isinstance(filename, (io.IOBase, types.file)):
            target = filename
            close = False
        elif isinstance(filename, (str, types.bytes)):
            target = open(filename, "wb+")
            close = True
        else:
            raise TypeError("wrong file type: %s" % type(filename))
        try:
            resp = self.client.call(path.method, path, stream=True, response=True, params=params)
            total = float(resp.headers.get("content-length", 0))
            downloaded = 0.0
            for block in resp.iter_content(chunk_size=chunk_size):
                target.write(block)
                downloaded += len(block)
                if hook:
                    hook(resp, total, downloaded)
        finally:
            if close:
                target.close()
            else:
                target.seek(0)
