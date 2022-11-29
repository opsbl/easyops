# -*- coding: utf-8 -*-
#

"""
@Project: 易方达
@File:    easy_flow
@Author:  boli
@Data:    2022/11/28 20:26
@Describe: 
    EasyFlow Application
"""

from ._base import BaseAppPaths, Path, APP


class EasyFlowPaths(BaseAppPaths):
    create_deploy_strategy = Path("/deployStrategy", method="POST", desc="Create a new deployment policy")
    list_deploy_strategy = Path("/deployStrategy", method="GET", desc="Gets a list of deployment policies")
    modify_deploy_strategy = Path("/deployStrategy/{strategy_id}", method="PUT", desc="Modify the deployment policy")
    delete_deploy_strategy = Path("/deployStrategy/{strategy_id}", method="DELETE", desc="Delete the deployment policy")
    exec_deploy_strategy = Path("/deployStrategy/exec/{strategy_id}", method="POST", desc="Policy one-click deployment")
    get_deploy_params = Path("/deployStrategy/{strategy_id}", method="GET",
                             desc="Gets the deployment policy parameters")


class EasyFlow(APP):
    name_service = "logic.easyflow"
    paths = EasyFlowPaths()
