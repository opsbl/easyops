# coding=utf-8

from ._base import BaseAppPaths, Path, APP


class CMDBPaths(BaseAppPaths):
    # documents: http[s]://YOUR-DOMAIN/next/developers/providers-v2/cmdb?group=business-instance&debugger-expand=0

    instance_search = Path("/object/{object_id}/instance/_search", method="POST", desc="Search for an instance")
    instance_search_v2 = Path("/v2/object/{object_id}/instance/_search", method="POST",
                              desc="Search for instance v2(supports multi-attribute sorting)")
    instance_search_v3 = Path("/v3/object/{object_id}/instance/_search", method="POST",
                              desc="Search for instance v2(supports multi-attribute sorting)")

    instance_search_total = Path("/object/{object_id}/instance/_search_total", method="POST",
                                 desc="Total number of searches")

    instance_detail = Path("/object/{object_id}/instance/{instance_id}", method="GET", desc="Gets the instance details")

    instance_create = Path("/v2/object/{object_id}/instance", method="POST", desc="Create an instance")
    instance_batch_create = Path("/mix/object/instance/create", method="POST", desc="Create instances in batches")

    instance_update = Path("/object/{object_id}/instance/{instance_id}", method="PUT", desc="Update the instance")
    instance_update_v2 = Path("/v2/object/{object_id}/instance/{instance_id}", method="PUT",
                              desc="Update the instance V2 (support update)")
    instance_batch_update = Path("/mix/object/instance/update", method="POST", desc="Batch update instance")

    instance_delete = Path("/object/{object_id}/instance/{instance_id}", method="DELETE", desc="Delete an instance")
    instance_batch_delete = Path("/object/{object_id}/instance/_batch", method="DELETE", desc="Batch delete instances")

    instance_export_to_csv = Path("/object/{object_id}/instance/export", method="POST", desc="Instance export to CSV")
    instance_export_to_excel = Path("/export/object/{object_id}/instance/excel", method="POST",
                                    desc="Instance export to Excel")

    instance_import = Path("/object/{object_id}/instance/_import", method="POST", desc="Batch edit/add instances")
    # file
    instance_import_from_csv = Path("/import/object/{object_id}/instance/csv", method="POST",
                                    desc="Use the CSV file import instance")
    instance_import_from_excel = Path("/import/object/{object_id}/instance/excel", method="POST",
                                      desc="Use the Excel file import instance")
    instance_import_from_json = Path("/import/object/{object_id}/instance/json", method="POST",
                                     desc="Use the JSON file import instance")

    instance_aggregation = Path("/object/{object_id}/instance/group", method="POST",
                                desc="Instance aggregation interface")
    instance_aggregation_v2 = Path("/v2/object/{object_id}/instance/group", method="POST",
                                   desc="Instance aggregation interface V3")
    instance_aggregation_v3 = Path("/v3/object/{object_id}/instance/group", method="POST",
                                   desc="Instance aggregation interface V3")

    instance_strategy_create = Path("/object/{object_id}/query/strategy", method="POST",
                                    desc="Create an instance query policy")
    instance_strategy_detail = Path("/object/{object_id}/query/strategy/{strategy_id}", method="GET",
                                    desc="Gets the instance query policy")
    instance_strategy_delete = Path("/object/{object_id}/query/strategy/{strategy_id}", method="DELETE",
                                    desc="Delete the instance query policy")
    instance_strategy_list = Path("/object/{object_id}/query/strategy", method="GET",
                                  desc="Gets a list of instance query policies")

    instance_update_by_query = Path("/object/{object_id}/instance/update_by_query", method="POST",
                                    desc="Updates the instance based on the query criteria")

    instance_batch_modify_permissions = Path("/permission/{object_id}/instances/_batch", method="PUT",
                                             desc="Modify instance permissions in bulk")

    instance_validate = Path("/object/{object_id}/instances/_validate", method="POST", desc="Instance validation")

    relation_append = Path("/object/{object_id}/relation/{relation_id}/append", method="POST",
                           desc="Batch add relationships")

    relation_remove = Path("/object/{object_id}/relation/{relation_id}/remove", method="POST",
                           desc="Batch remove relationships")

    relation_set = Path("/object/{object_id}/relation/{relation_id}/set", method="POST",
                        desc="Batch set relationships")

    relation_instance_count = Path("/object_relation/{relation_id}/relation_instance/_count_relation_instance",
                                   method="GET", desc="Number of statistical relationship instance")

    relation_autodiscovery = Path("/object_relation/{relation_id}/_autodiscovery/multi",
                                  method="POST", desc="Instance Relationship Discovery")

    relation_autodiscovery_v2 = Path("/v2/object_relation/{relation_id}/_autodiscovery/multi",
                                     method="POST", desc="Instance Relationship Discovery(v2)")
    relation_instance_snapshot = Path("/history/object_relation/{relation_id}/relation_instance/{relation_instance_id}",
                                      method="GET", desc="Query a snapshot of the historical instance relationship")

    object_all = Path("/object_all", method="GET", desc="Gets all the models")
    object_list = Path("/object", method="GET", desc="To obtain a list model")
    object_create = Path("/object", method="POST", desc="Create model")
    object_detail = Path("/object/{object_id}", method="GET", desc="Get model detail")
    object_update = Path("/v2/object/{object_id}", method="PUT", desc="Update model")
    object_update_batch = Path("/batch/object", method="PUT", desc="Batch update model")
    object_delete = Path("/object/{object_id}", method="DELETE", desc="Delete model")

    object_import = Path("/object_import", method="POST", desc="Bulk import models")
    object_import_v2 = Path("/v2/object_import", method="POST", desc="Bulk import models(V2)")

    object_import_check = Path("/object_import_check", method="POST", desc="import objects check")
    object_import_check_v2 = Path("/v2/object_import_check", method="POST", desc="Batch import model check(v2)")
    object_import_conflict_check = Path("/object_conflict_check", method="POST", desc="Model conflict checking")

    object_attr = Path("/object/{object_id}/attr/{attr_id}", method="GET", desc="Gets the model properties")
    object_attr_update = Path("/object/{object_id}/attr/{attr_id}", method="PUT", desc="Update model properties")
    object_attr_delete = Path("/object/{object_id}/attr/{attr_id}", method="PUT", desc="Delete model properties")

    def __init__(self, app_name="cmdbservice"):
        super(CMDBPaths, self).__init__(app_name, relative=False)


class CMDB(APP):
    paths = CMDBPaths("cmdbservice")
    # cmdb.easyops-only.com
    # cmdb_resource.easyops-only.com
    host = "cmdb_resource.easyops-only.com"

    name_service = "logic.cmdb.service"

    def instance_search(self, object_id, **body):
        return self.client.post(self.paths.instance_search,
                                url_params={
                                    "object_id": object_id,
                                },
                                json=body)

    def instance_search_v3(self, object_id, **body):
        return self.client.post(self.paths.instance_search_v3,
                                url_params={
                                    "object_id": object_id,
                                },
                                json=body)

    def instance_search_first(self, object_id, **body):
        lst = self.instance_search(object_id, **body)["list"]
        if len(lst) > 0:
            return lst[0]
        return None

    def instance_import(self, object_id, **body):
        return self.client.post(self.paths.instance_import,
                                url_params={
                                    "object_id": object_id,
                                },
                                json=body)

    def instance_create(self, object_id, **body):
        return self.client.post(self.paths.instance_create,
                                url_params={
                                    "object_id": object_id,
                                },
                                json=body)

    def instance_update(self, object_id, instance_id, **body):
        return self.client.put(self.paths.instance_update,
                               url_params={
                                   "object_id": object_id,
                                   "instance_id": instance_id,
                               },
                               json=body)

    def instance_delete(self, object_id, instance_id):
        return self.client.delete(self.paths.instance_delete,
                                  url_params={
                                      "object_id": object_id,
                                      "instance_id": instance_id,
                                  })

    def instance_detail(self, object_id, instance_id):
        return self.client.get(self.paths.instance_detail, url_params={
            "object_id": object_id,
            "instance_id": instance_id,
        })

    def instance_batch_delete(self, object_id, *instance_ids):
        """
        Delete instances in batches
        :param object_id:
        :param instance_ids:
        :return:
        """
        return self.client.delete(self.paths.instance_batch_delete,
                                  url_params={
                                      "object_id": object_id,
                                  },
                                  params={
                                      "instanceIds": ";".join(instance_ids)
                                  })

    def instance_relation_autodiscovery(self, relation_id, left_match, right_match, data, operation,
                                        strict=False, main_side_id=None):
        """
        relationship auto-discovery
        document:
        http[s]://DOMAIN/next/developers/providers-v2/cmdb?group=instance-relation&api-name=discovery-v2&debugger-expand=0
        :param relation_id:
        :param left_match:
        :param right_match:
        :param right_match:
        :param data: [ {"left_instance": {"key": "value"}, "right_instance": {"key": "value"}}, {...}, ... ]
        :param operation:
        :param strict:
        :param main_side_id:
        :return:
        """
        body = {
            "match": {
                "left_match": left_match,
                "right_match": right_match,
            },
            "strict": strict,
            "data": data,
            "operation": operation,
        }
        if main_side_id:
            body.update({"mainSideId": main_side_id})

        return self.client.post(self.paths.relation_autodiscovery,
                                url_params={"relation_id": relation_id},
                                json=body)

    def _multi_relation_handle(self, path, object_id, relation_key, instance_ids, related_instance_ids):
        """
        batch relationships
        :param path:
        :param object_id:
        :param relation_key: relation key
        :param instance_ids: Instance ID of the current model
        :param related_instance_ids: the id of the associated instance
        :return:
        """
        return self.client.post(path, url_params={
            "object_id": object_id,
            "relation_id": relation_key,
        }, json={
            "related_instance_ids": related_instance_ids,
            "instance_ids": instance_ids
        })

    def instance_relation_append(self, object_id, relation_key, instance_ids, related_instance_ids):
        return self._multi_relation_handle(self.paths.relation_append, object_id, relation_key, instance_ids,
                                           related_instance_ids)

    def instance_relation_remove(self, object_id, relation_key, instance_ids, related_instance_ids):
        return self._multi_relation_handle(self.paths.relation_remove, object_id, relation_key, instance_ids,
                                           related_instance_ids)

    def instance_relation_set(self, object_id, relation_key, instance_ids, related_instance_ids):
        return self._multi_relation_handle(self.paths.relation_set, object_id, relation_key, instance_ids,
                                           related_instance_ids)

    def object_create(self, **body):
        return self.client.post(self.paths.object_create, json=body)

    def object_all(self, **query):
        return self.client.get(self.paths.object_all, params=query)

    def object_list(self, **query):
        return self.client.get(self.paths.object_list, params=query)

    def object_update(self, object_id, **body):
        return self.client.put(self.paths.object_update, body=body, url_params={
            "object_id": object_id,
        })

    def object_delete(self, object_id):
        return self.client.delete(self.paths.object_delete, url_params={
            "object_id": object_id,
        })

    def object_attr(self, object_id, attr_id):
        return self.client.get(self.paths.object_attr, url_params={
            "object_id": object_id,
            "attr_id": attr_id,
        })

    def object_attr_update(self, object_id, attr_id, **body):
        return self.client.put(self.paths.object_attr_update, url_params={
            "object_id": object_id,
            "attr_id": attr_id,
        }, json=body)

    def object_attr_delete(self, object_id, attr_id, **body):
        return self.client.delete(self.paths.object_attr_delete, url_params={
            "object_id": object_id,
            "attr_id": attr_id,
        }, json=body)
