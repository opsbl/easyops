EasyOps动态库使用说明
=====================

客户端类型
==========

   EasyOps平台目前访问有两种方式, 分别是\ ``org``\ 和\ ``openapi``.

``OrgClient``
-------------

.. code:: python

   from easyops.org_client import OrgClient

   org_client = OrgClient("http://DOMAIN/", host="", org=8888888, user="easyops", valid=True, debug=True)

============ ==== =====================================
参数         必须 备注
============ ==== =====================================
``server``   Y    服务地址
``host``     Y    请求头中的\ ``Host``\ 参数
``org``      Y    ORG
``user``     Y    用户名
``valid``    N    默认: True, 验证接口返回code是否等于0
``debug``    N    Debug模式
``skip_ssl`` N    默认: False, 忽略SSL
============ ==== =====================================

``OpenApi``
-----------

.. code:: python

   from easyops.openapi import OpenApi

   openapi = OpenApi("http://DOMAIN/", access_key="6d9e55d2d4d8223ba6545", secret_key="66536b6352536c6747764567555265586e62755979546d4e6f74635a4f66")

============== ==== =====================================
参数           必须 备注
============== ==== =====================================
``server``     Y    服务地址
``access_key`` Y    Access Key
``secret_key`` Y    Secret Key
``debug``      N    Debug模式
``valid``      N    默认: True, 验证接口返回code是否等于0
============== ==== =====================================

Application
===========

   ``application``\ 代表平台的一个组件, 该组件有对应的访问方式, 如:
   ``cmdb,appconfig``\ 等. easyops库实现了两种不同客户端的通用.

.. code:: python

   from easyops import apps
   from easyops.openapi import OpenApi
   from easyops.org_client import OrgClient

   # 以OpenAPI方式调用APP
   openapi = OpenApi("http://DOMAIN/", access_key="6d9e55d2d4d70f82a6545", secret_key="66536b6352567477645675552655662686e62755979546d4e6f74635a4f66")
   cmdb = apps.CMDB(openapi)	# cmdb = apps.CMDB(openapi, APP_NAME) 默认: app_name="cmdbservice"

   data = cmdb.instance_search("HOST", page=1, page_size=1, fields={"ip": 1, "hostname": 1})


   # 以OrgClient方式调用APP
   org_client = OrgClient("http://DOMAIN/", host="", org=8888888, user="easyops")
   cmdb = apps.CMDB(org_client)
   # 搜索实例
   data = cmdb.instance_search("HOST", page=1, page_size=1, fields={"ip": 1, "hostname": 1})
   # 追加关系
   cmdb.instance_relation_append("HOST",relation_key="users",instance_ids=["x", "x"], related_instance_ids=["y", "y"])
   # 关系自动发现
   cmdb.instance_relation_autodiscovery("HOST_users_hosts_USER", 
                                        left_match=["instanceId"],
                                        right_match=["instanceId"], 
                                        data=[ {"left_instance": {"key": "value"}, "right_instance": {"key": "value"}}, {...}, ... ], 
                                        operation="set")

   # 生成openapi配置信息
   # 如: cmdb
   cmdb = apps.CMDB(openapi)
   # 为当前APP生成openapi配置信息
   print(cmdb.generate_openapi_configs("logic.cmdb_service"))	# py2 => str, py3 => bytes
   # api_list:
   # - frequency: 120
   #   method: GET
   #   uri: /cmdbservice/object_relation/{relation_id}/relation_instance/_count_relation_instance
   # - frequency: 120
   #   method: DELETE
   #   uri: /cmdbservice/object/{object_id}/instance/{instance_id}
   # - frequency: 120
   #   method: GET
   #   uri: /cmdbservice/object_all
   # app_name: cmdbservice
   # host: cmdb_resource.easyops-only.com
   # service_name: logic.cmdb_service
   # 为单一API接口生成配置信息
   print(cmdb.paths.instance_search_v3.generate_openapi_config(frequency=500))
   # - frequency: 500
   #   method: POST
   #   uri: /cmdbservice/v3/object/{object_id}/instance/_search

其中内置了\ ``CMDB,AppConfig，Tool``\ 等\ ``APP``, 以及常见的方法.
如方法不存在, 但是存在\ ``Path``\ 对象, 那么可以直接调用该\ ``Path``

.. code:: python

   # Path的调用方法
   appconfig = apps.AppConfigPaths(org_client)

   # appconfig 存在 templates_key path, 那么该接口是可以被调用的
   print appconfig.paths.templates_key
   # 调用方法如下:
   # 参数和requests类似, 多了一个url_params用于填充path的具名参数
   data = appconfig.templates_key()
   data = appconfig.appconfig_list(params={"appId": "xcds"})

   # 获取所有的path
   print appconfig.paths.get_all_paths()

   # 扩展path，用于处理业务逻辑
   appconfig.paths.extend_paths([
       {
           "name": "test",
           "path": "/a/b/c/{id}",
           "desc": "test",
           "method": "GET"
       }
   ])
   print type(appconfig.paths.test), appconfig.paths.test
   print appconfig.test()

自定义Application
-----------------

   由于内置\ ``Application``\ 覆盖率较低,
   很多情况下可能需要自定义\ ``Application``

.. code:: python

   from easyops.openapi import OpenApi

   from easyops.apps import BaseApp
   from easyops.apps import BaseAppPaths, Path


   class DeployPaths(BaseAppPaths):
       # 定义当前APP存在的Path以及请求方法
       test = Path("/a/b/c", method="GET", desc="test")


   class Deploy(BaseApp):
       # host 用于OrgClient
       host = "deploy.easyops-only.com"
       # DeployPaths("APP名字") 用于OpenAPI
       paths = DeployPaths("deploy")

       def test_method(self, **query):
           # 自定义方法
           return self.client.get(self.paths.test, params=query)

   openapi = OpenApi("http://DOMAIN/", access_key="6d9e55d2d4d70f8223ba6545", secret_key="66536b6352536c67477645675552655662686e62755979546d4e6f74635a4f66")
   deploy = Deploy(openapi)

   deploy.test_method() 
   # or 
   deploy.test()
