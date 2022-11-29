from .cmdb import CMDB
from .tool import Tool
from .easy_flow import EasyFlow
from .easy_plugin import Plugin
from .appconfig import AppConfig
from .scheduler import Scheduler
from .artifact import Artifact, DeployRepo
from ._base import BaseAppPaths, Path, APP

BaseApp = APP

applications = {
    "appconfig": AppConfig,
    "cmdb": CMDB,
    "tool": Tool,
    "artifact": Artifact,
    "deploy_repo": DeployRepo,
    "deployrepo": DeployRepo,
    "plugin": Plugin,
    "easy_plugin": Plugin,
    "scheduler": Scheduler,
    "easy_flow": EasyFlow,
}

__all__ = [
    "APP",
    "Path",
    "Artifact",
    "BaseAppPaths",
    "BaseApp",
    "AppConfig",
    "DeployRepo",
    "Plugin",
    "CMDB",
    "applications",
    "Scheduler",
    "EasyFlow",
]
