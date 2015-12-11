# coding: utf-8
from binascii import hexlify
from uuid import uuid4

from fields import Field, StringField
from ..helpers.helpers import Helpers
from itertools import chain


class FieldProperty(object):
    def __init__(self, field, name=None):
        self.field = field
        self.name = name or field.name

    def __get__(self, instance, owner):
        if instance is None:
            return owner._fields[self.name]
        try:
            return instance._values[self.name]
        except KeyError as e:
            raise AttributeError(*e.args)

    def __set__(self, instance, value):
        instance._values[self.name] = value

    def __delete__(self, instance):
        del instance._values[self.name]


class TOMeta(type):
    def __new__(mcs, name, bases, attrs):

        def get_base_attr(attrname, rev=False):
            for base in (bases if not rev else reversed(bases)):
                try:
                    yield getattr(base, attrname)
                except AttributeError:
                    pass

        # Overriding fields in subclasses might lead to problems!!

        fields = {}
        for base_fields in get_base_attr("_fields", True):
            fields.update(base_fields)

        defaults = {}
        for base_defaults in get_base_attr("_defaults", True):
            defaults.update(base_defaults)

        pks = list(chain.from_iterable(get_base_attr("_pks")))
        indexes = set(chain.from_iterable(get_base_attr("_indexes")))

        if "_NUM_PKS" in attrs:
            num_pks = attrs["_NUM_PKS"]
        else:
            num_pks = next(get_base_attr("_NUM_PKS"))

        for attrname, attrvalue in attrs.iteritems():
            if isinstance(attrvalue, Field):
                attrvalue.name = attrname
                fields[attrname] = attrvalue
                if attrvalue.pk:
                    pks.append(attrname)
                if attrvalue.index:
                    indexes.add(attrname)
                if attrvalue.null:
                    defaults[attrname] = None

        # allow empty TO declarations otherwise it must have a PK
        if fields:
            if isinstance(num_pks, (tuple, list)):
                if not num_pks[0] <= len(pks) <= num_pks[1]:
                    raise ValueError("%s expected to have from %d to %d pks" % (name, num_pks[0], num_pks[1]))
            elif len(pks) != num_pks:
                raise ValueError("%s expected to have %d pks" % (name, num_pks))

        if len(pks) >= 2:
            # If pk is an integer sort pks list accordingly, otherwise they won't have deterministic order!
            pk_fields_pks = [fields[pk_name].pk for pk_name in pks]
            if not all(isinstance(pk, (int, long)) for pk in pk_fields_pks) or\
                    len(set(pk_fields_pks)) != len(pk_fields_pks):
                raise ValueError("When using multiple pks all field.pk values must be unique integers")
            pks.sort(key=lambda k: fields[k].pk)

        for key, field in fields.iteritems():
            attrs[key] = FieldProperty(field)
        attrs["_fields"] = fields
        attrs["_pks"] = pks
        attrs["_indexes"] = indexes
        attrs["_defaults"] = defaults

        return super(TOMeta, mcs).__new__(mcs, name, bases, attrs)


class TO(object):
    __metaclass__ = TOMeta
    _NUM_PKS = 1

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self._values)

    __repr__ = __str__

    def __init__(self, **kwargs):
        self._values = self._defaults.copy()
        self.populate(**kwargs)

    def populate(self, **kwargs):
        values = self._values
        for key, value in kwargs.iteritems():
            if key in self._fields:
                values[key] = value

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        values = instance._values
        fields = instance._fields
        for key, value in data.iteritems():
            if key in fields:
                values[key] = fields[key].deserialize(value)

        return instance

    @classmethod
    def get_field(cls, name):
        return cls._fields[name]

    def _before_serialize(self):
        pass

    def _serialize(self, fields_to_ignore=None):
        values = self._values
        fields = self._fields
        data = {}
        for name, field in fields.iteritems():
            if fields_to_ignore and name in fields_to_ignore:
                continue
            value = values.get(name)
            field.validate(value)
            s_value = field.serialize(value)
            if field.store and (s_value is not None or field.store_null):
                data[name] = s_value
        return data

    def serialize(self):
        self._before_serialize()
        return self._serialize()

    @property
    def pk(self):
        return getattr(self, self._pks[0])

    @property
    def _internal_pk(self):
        # THIS IS A GIGANTIC HACK
        # returns the original or internal pk representation, useful if any pks are store=False
        # it might be available when you deserialize data coming from the DB
        # aerospike implementation
        return hexlify(self._key_tuple[3])
        # possibly add other db variants


class PKConcatTO(TO):
    _NUM_PKS = (2, 10)

    @property
    def pk(self):
        return Helpers.concat([getattr(self, name) for name in self._pks])


class PKUUIDTO(TO):
    # Important Note:
    # The _id field might NOT be stored in the body of the record,
    # so it might NOT be present after deserialization!
    # This is useful in TOs that will only be queried by secondary indexes.
    # If you possibly need the TO pk afterwards use a plain TO with a pk field instead.
    _id = StringField(pk=True, store=False)

    def _before_serialize(self):
        if not hasattr(self, "_id"):
            self._id = str(uuid4())
