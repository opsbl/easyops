# -*- coding: utf-8 -*-
#

"""
@Project: easyops
@File:    examples
@Author:  boli
@Data:    2022/11/22 10:21
@Describe: 
    examples
"""

from easyops import apps
from easyops.client import OpenApi

if __name__ == '__main__':
    openapi = OpenApi("http://192.168.110.17/", access_key="c7aad600e83d811bf7dabdc7",
                      secret_key="75614859414c616e6f4654626f4d664144536e594e48574d59734a6558545361",
                      debug=True)
    cmdb = apps.CMDB(openapi)
    print(cmdb.instance_search("HOST", fields={"ip": 1}))

    print(cmdb.generate_openapi_configs("logic.cmdb.service"))
