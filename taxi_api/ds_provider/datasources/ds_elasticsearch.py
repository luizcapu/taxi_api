# coding: utf-8

__author__ = 'luiz'

from ds_interface import DSInterface
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan as es_scan
import functools


class DSElasticSearch(DSInterface):

    def __init__(self, ds_name, environment, config):
        self.ds_name = ds_name
        self.environment = environment
        self.config = config or {}
        self.connected = False
        self.client = None
        self.connection = None
        self._parse_config()
        self._scan = None

    @property
    def scan(self):
        if not self.connected:
            raise Exception("Driver must be connected before perform scan")
        if self._scan is None:
            self._scan = functools.partial(es_scan, self.connection, index=self.index)
        return self._scan

    def _reload_config(self):
        pass

    def _parse_config(self):
        """
            config (dict) –
            the client’s configuration.
            hosts a list of (address, port) tuples identifying the cluster
            policies a dict of policies
            timeout default timeout in milliseconds
            key default key policy for this client
            exists default exists policy for this client
            gen default generation policy for this client
            retry default retry policy for this client
            consistency_level default consistency level policy for this client
            replica default replica policy for this client
            commit_level default commit level policy for this client
        """
        self.conn_args = self.config.get("conn_args") or {}
        self.hosts = self.config["hosts"]
        if not isinstance(self.hosts, list):
            self.hosts = [self.hosts]
        self.index = self.config.get("index")

    def validate(self):
        still_valid = True
        # TODO check still_valid comparing current config with _reload_config result
        if self.connected:
            if not still_valid:
                self._connect()

    def _connect(self):
        try:
            self.client = self._get_client()
            self._get_connection()
            self.connected = True
        except:
            self.connected = False
            raise

    def connect(self):
        if self.connected:
            self.validate()
        else:
            self._connect()

    def _get_client(self):
        self.client = Elasticsearch(self.hosts, **self.conn_args)
        return self.client

    def get_client(self):
        self.connect()
        return self.client

    def _get_connection(self):
        self.connection = self.client
        return self.connection

    def get_connection(self):
        self.connect()
        return self.connection
