# coding: utf-8

import datetime
from ._base import BaseAppPaths, Path, APP


class AppConfigPaths(BaseAppPaths):
    # documents: http[s]://YOUR-DOMAIN/next/developers/providers-v2/appconfig?group=appconfig&debugger-expand=0

    appconfig_list = Path("/api/v1/appconfig", desc="Get application configuration list")
    appconfig_keys = Path("/api/v1/appconfig/keys", desc="Get configuration keys")
    appconfig_values = Path("/api/v1/appconfig/values", desc="Get configuration values")
    publish_appconfig = Path("/api/v1/appconfig/values", method="POST", desc="Publishing environment configuration")
    modify_appconfig_values = Path("/api/v1/appconfig/values", method="PATCH", desc="Modifying the Configuration value")
    appconfig_detail = Path("/api/v1/appconfig/detail", desc="Get the Detail of the specified level configuration")
    appconfig_summary = Path("/api/v1/appconfig/summary", desc="Get an overview of app configuration", method="POST")
    appconfig_publish = Path(appconfig_list.path, method="POST", desc="Publishing environment configuration")
    appconfig_render = Path("/api/v1/appconfig/render", method="POST", desc="Rendering configuration")
    appconfig_diff = Path("/api/v1/appconfig/diff", method="GET", desc="Gets the applied configuration differences")
    appconfig_instance_diff = Path("/api/v1/appconfig/instance/diff",
                                   method="POST",
                                   desc="Gets the applied instance difference")
    appconfig_instance_file_diff = Path("/api/v1/appconfig/instance/filediff",
                                        method="POST",
                                        desc="Gets the difference in the applied profile")

    appconfig_version_list = Path("/api/v1/appconfig/version", method="GET",
                                  desc="Gets a list of application configuration versions")
    appconfig_version_diff = Path("/api/v1/appconfig/version/diff", method="GET",
                                  desc="Gets the applied configuration version differences")

    templates_diff = Path("/api/v1/templates/diff", method="POST", desc="Gets the template key difference")
    templates_key = Path("/api/v1/templates/key", method="GET", desc="Gets the template key")
    templates_validate = Path("/api/v1/templates/validate", method="POST", desc="Verify the template key")

    def __init__(self, app_name="appconfig"):
        super(AppConfigPaths, self).__init__(app_name, relative=False)


class AppConfig(APP):
    """
    e.g.
        openapi = OpenApi("http://192.168.234.143", "xxxxxxx", "xxxxxxxxxxxxxx")
        appconfig = AppConfig(openapi)

        appconfig_list = appconfig.get_appconfig_list(app_id="5e13c2c9fdff5")
        or:
        # Make a request using the API name
        # The parameters of the following request methods are the same as those used by the requests library,
        # except for the `url_params` parameter, which is mainly used to fill the parameters in the url,
        # such as: https://example.cn/{instance_id} => url_params={“instance_id”: "5e13c2c9fdff5"}

        appconfig_list = appconfig.appconfig_list(params={"appId": "5e13c2c9fdff5"})

        # Get all API names and details
        appconfig.paths.get_all_paths()
        => {
            'appconfig_instance_diff':
            <Path path='/appconfig/api/v1/appconfig/instance/diff',desc='Gets the applied instance difference'>
        }

    """
    paths = AppConfigPaths("appconfig")
    name_service = "logic.appconfig"

    def get_appconfig_list(self, app_id, **query):
        """
        Get APP configuration list
        :param app_id:
        :param query:
        :return:
        """
        return self.client.get(self.paths.appconfig_list, params=dict(appId=app_id, **query))

    def get_appconfig_values(self, app_id, env, version=None, **query):
        """
        Get configuration values
        :param app_id:
        :param env: develop|test|prerelease|production
        :param version:
        :param query:
        :return:
        """
        return self.client.get(self.paths.appconfig_values, params=dict(appId=app_id,
                                                                        env=env,
                                                                        version=version,
                                                                        **query))

    def get_appconfig_keys(self, app_id, env=None, version=None, **query):
        """
        Get configuration keys
        :param app_id:
        :param env: develop|test|prerelease|production
        :param version:
        :param query:
        :return:
        """

        return self.client.get(self.paths.appconfig_keys, params=dict(appId=app_id,
                                                                      env=env,
                                                                      version=version,
                                                                      **query))

    def get_appconfig_detail(self, app_id, env, cluster_id=None, host_instance_id=None, version_id=None, **query):
        """
        Get the Detail of the specified level configuration
        :param app_id:
        :param env: develop|test|prerelease|production
        :param cluster_id:
        :param host_instance_id:
        :param version_id:
        :param query:
        :return:
        """

        return self.client.get(self.paths.appconfig_detail, params=dict(
            appId=app_id,
            env=env,
            clusterId=cluster_id,
            hostInstanceId=host_instance_id,
            versionId=version_id,
            **query
        ))

    def get_appconfig_summary(self, app_id, env=None, namespaces=None, **body):
        """
        Gets an overview of the application configuration
        :param app_id:
        :param env:
        :param namespaces:
        :return:
        """
        return self.client.post(self.paths.appconfig_summary, json=dict(
            appId=app_id,
            env=env,
            namespaces=namespaces,
            **body
        ))

    def render(self, app_id, env, clusters=None, packages=None, version_id=None, **body):
        """
        render configuration
        :param app_id:
        :param env:
        :param clusters:
        :param packages:
        :param version_id:
        :param body:
        :return:
        """
        return self.client.posts(self.paths.appconfig_render, json=dict(
            appId=app_id,
            env=env,
            clusters=clusters,
            packages=packages,
            versionId=version_id,
            **body
        ))

    def modify_appconfig_values(self, action, app_id, env, keys):
        return self.client.patch(self.paths.modify_appconfig_values, json={
            "action": action,
            "appId": app_id,
            "env": env,
            "keys": keys
        })

    def publish_appconfig(self, app_id, env, release=None, message="", **kwargs):
        """
        publish appconfig
        :param app_id:
        :param env:
        :param release:
        :param message:
        :return:
        """

        release = release or datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        body = {
            "appId": app_id,
            "env": env,
            "message": message,
            "release": release,
        }
        body.update(kwargs)
        return self.client.post(self.paths.publish_appconfig, json=body)
