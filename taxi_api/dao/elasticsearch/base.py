__author__ = 'luiz'

from ..base import BaseDao
from elasticsearch.exceptions import ElasticsearchException, NotFoundError
import logging
from taxi_api.to.fields import *
from taxi_api.helpers.helpers import Helpers


def add_defaults(properties, defaults):
    if properties is None:
        properties = {}
    if defaults:
        for k, v in defaults.iteritems():
            properties.setdefault(k, v)
    return properties


class DBBaseDao(BaseDao):

    _EXCEPTION_IGNORE_ON_QUERY = []
    _EXCEPTION_IGNORE_ON_READ = [NotFoundError]
    _EXCEPTION_IGNORE_ON_WRITE = []
    _EXCEPTION_IGNORE_ON_DELETE = [2]  # 2 = AEROSPIKE_ERR_RECORD_NOT_FOUND
    _UPDATE_ARGS_LABEL = "update_args"
    _WRITE_ARGS_LABEL = "index_args"
    _READ_ARGS_LABEL = "read_args"
    _default_write_args = {}
    _default_update_args = {"retry_on_conflict": 10}
    _default_read_args = {}

    def save(self, to_obj, **kwargs):
        update_args = add_defaults(kwargs.get(self._UPDATE_ARGS_LABEL, {}), self._default_update_args)

        # call serialize BEFORE _build_pk
        _serialized = to_obj.serialize()
        # active upsert
        doc_body = dict(doc=_serialized, upsert=_serialized)

        rec_id = kwargs.get("rec_id")
        if rec_id is None:
            rec_id = self._build_pk(to_obj)
        try:
            self.data_source.connection.update(
                index=self.data_source.index,
                doc_type=self._get_table_name(),
                body=doc_body,
                id=rec_id,
                params=update_args
            )
            return to_obj
        except ElasticsearchException as e:
            if e.__class__ in self._EXCEPTION_IGNORE_ON_WRITE:
                self._log_exception(*e.args)
                return None
            raise

    def save_if_up_to_date(self, to_obj, **kwargs):
        if "version" in kwargs.keys():
            if self._UPDATE_ARGS_LABEL not in kwargs:
                kwargs[self._UPDATE_ARGS_LABEL] = {}
            kwargs[self._UPDATE_ARGS_LABEL]["version"] = kwargs["version"]
            if "version_type" in kwargs.keys():
                kwargs[self._UPDATE_ARGS_LABEL]["version_type"] = kwargs["version_type"]
        return self.save(to_obj, **kwargs)

    def _index(self, to_obj, **kwargs):
        write_args = add_defaults(kwargs.get(self._WRITE_ARGS_LABEL, {}), self._default_write_args)

        # call serialize BEFORE _build_pk
        doc_body = to_obj.serialize()

        rec_id = kwargs.get("rec_id")
        if rec_id is None:
            rec_id = self._build_pk(to_obj)
        try:
            self.data_source.connection.index(
                index=self.data_source.index,
                doc_type=self._get_table_name(),
                body=doc_body,
                id=rec_id,
                params=write_args)
            return to_obj
        except ElasticsearchException as e:
            if e.__class__ in self._EXCEPTION_IGNORE_ON_WRITE:
                self._log_exception(*e.args)
                return None
            raise

    def replace(self, to_obj, **kwargs):
        if self._WRITE_ARGS_LABEL not in kwargs:
            kwargs[self._WRITE_ARGS_LABEL] = {}
        kwargs[self._WRITE_ARGS_LABEL]["op_type"] = "index"
        return self._index(to_obj, **kwargs)

    def create(self, to_obj, **kwargs):
        if self._WRITE_ARGS_LABEL not in kwargs:
            kwargs[self._WRITE_ARGS_LABEL] = {}
        kwargs[self._WRITE_ARGS_LABEL]["op_type"] = "create"
        return self._index(to_obj, **kwargs)

    def delete(self, to_obj, **kwargs):
        # call serialize BEFORE _build_pk
        to_obj.serialize()

        rec_id = kwargs.get("rec_id")
        if rec_id is None:
            rec_id = self._build_pk(to_obj)
        try:
            self.data_source.connection.delete(
                index=self.data_source.index,
                doc_type=self._get_table_name(),
                id=rec_id
            )
            return True
        except ElasticsearchException as e:
            if e.__class__ in self._EXCEPTION_IGNORE_ON_DELETE:
                self._log_exception(*e.args)
                return
            raise

    def exists(self, pk):
        return self.data_source.connection.exists(
            index=self.data_source.index,
            doc_type=self._get_table_name(),
            id=pk
        )

    def _record_to_to(self, record):
        _source = record.pop("_source", {})
        to_obj = self._to_class.deserialize(_source)
        for k, v in record.iteritems():
            if not hasattr(to_obj, k):
                setattr(to_obj, k, v)
        return to_obj

    def get_by_pk(self, pk, *fields, **kwargs):
        read_args = add_defaults(kwargs.get(self._READ_ARGS_LABEL, {}), self._default_read_args)
        if fields:
            read_args["_source"] = Helpers.concat(fields, ",")

        try:
            record = self.data_source.connection.get(
                index=self.data_source.index,
                doc_type=self._get_table_name(),
                id=pk,
                params=read_args
            )
            if record is not None:
                return self._record_to_to(record)
        except ElasticsearchException as e:
            if e.__class__ in self._EXCEPTION_IGNORE_ON_READ:
                self._log_exception(*e.args)
                return None
            raise

    def get_by_pks(self, pks, *fields, **kwargs):
        read_args = add_defaults(kwargs.get(self._READ_ARGS_LABEL, {}), self._default_read_args)
        if fields:
            read_args["_source"] = Helpers.concat(fields, ",")

        try:
            records = self.data_source.connection.mget(
                index=self.data_source.index,
                doc_type=self._get_table_name(),
                body=dict(ids=list(pks)),
                params=read_args
            )
            return {record["_id"]: self._record_to_to(record) if record["found"] else None
                    for record in records["docs"]}
        except ElasticsearchException as e:
            if e.__class__ in self._EXCEPTION_IGNORE_ON_READ:
                self._log_exception(*e.args)
                return None
            raise

    def get_all(self, table_name=None, **kwargs):
        raise NotImplementedError("get_all disabled")

    def search_by_field_value(self, field_to_search, value_to_search, *fields, **kwargs):
        query = {
            "query": {
                "filtered": {
                    "filter": {
                        "term": {
                            field_to_search: value_to_search
                        }
                    }
                }
            }
        }
        return self._run_query(query, *fields, **kwargs)

    def search_by_field_range(self, field_to_search, initial_range, final_range, *fields, **kwargs):
        query = {
            "query": {
                "filtered": {
                    "filter": {
                        "range": {
                            field_to_search: {
                                "from": initial_range,
                                "to": final_range
                            }
                        },
                    }
                }
            }
        }
        return self._run_query(query, *fields, **kwargs)

    def _get_table_name(self, table_name=None):
        if not table_name:
            table_name = self._default_table
        if not table_name or table_name == self._UNDEFINED_TABLE:
            raise Exception("Undefined table_name to perform operation")
        return table_name

    def _build_pk(self, to_obj):
        pk = to_obj.pk
        if pk is None:
            raise Exception("Could not build PK for service %s" % self.__class__.__name__)
        return pk

    def _log_exception(self, *args):
        logging.warning("{0} - {1} [{2}]".format(args[0], args[1], args[2]))

    def _run_query(self, query, *fields, **kwargs):
        read_args = add_defaults(kwargs.get(self._READ_ARGS_LABEL, {}), self._default_read_args)
        if fields:
            read_args["_source"] = Helpers.concat(fields, ",")

        try:
            records = self.data_source.connection.search(
                index=self.data_source.index,
                doc_type=self._get_table_name(),
                body=query,
                params=read_args
            )
            for record in records["hits"]["hits"]:
                yield self._record_to_to(record)
        except ElasticsearchException as e:
            if e.__class__ in self._EXCEPTION_IGNORE_ON_QUERY:
                self._log_exception(*e.args)
            raise

    def create_db(self, **kwargs):
        conn = self.data_source.connection
        if not conn.indices.exists(self.data_source.index):
            conn.indices.create(self.data_source.index)

    def create_table(self, **kwargs):
        conn = self.data_source.connection
        properties = {}
        mappings = dict(properties=properties)

        for field in self._to_class._fields.itervalues():
            if isinstance(field, Field):
                properties[field.name] = self._get_field_mapping(field)

        conn.indices.put_mapping(
            doc_type=self._get_table_name(),
            body=mappings,
            index=self.data_source.index)

    def _get_field_mapping(self, field):
        if isinstance(field, StringField) or isinstance(field, UUIDField):
            return dict(type="string", index="not_analyzed")
        elif isinstance(field, BooleanField):
            return dict(type="boolean")
        elif isinstance(field, GeoPointField):
            return dict(type="geo_point")
        elif isinstance(field, IntegerField):
            return dict(type="integer")
        elif isinstance(field, FloatField):
            return dict(type="float")
        elif isinstance(field, ListField) or isinstance(field, SetField) or isinstance(field, DictField):
            return dict(dynamic=True, enabled=True)
        elif isinstance(field, DateTimeField):
            return dict(type="date")
        else:
            raise Exception("Unkown mapping type for field %s" % field.name)