# coding: utf-8
from datetime import datetime, timedelta
import re
import uuid


class Field(object):
    def __init__(self, **kwargs):
        self._available_options = kwargs.get('options', None)
        if self._available_options:
            if not isinstance(self._available_options, list) or len(self._available_options) == 0:
                raise ValueError("Options must be a non empty list")

        self.name = self.__class__.__name__

        self.pk = kwargs.get('pk', False)
        self.null = kwargs.get('null', False)
        self.store_null = kwargs.get('store_null', False)

        if not isinstance(self.pk, (bool, int, long)):
            raise ValueError('%s pk attribute must be either bool or int type, not %s'
                             % (self.name, self.pk.__class__.__name__))

        if self.pk and self.null:
            raise ValueError('%s can not be PK and null' % self.name)

        if self.store_null and not self.null:
            raise ValueError("%s can not use store_null if not nullable" % self.name)

        self.index = kwargs.get('index', False)
        self.store = kwargs.get('store', True)
        self.default = kwargs.get('default', None)
        self.default_cast = kwargs.get('default_cast', None)
        self.default_args = kwargs.get('default_args', None)
        self.default_kwargs = kwargs.get('default_kwargs', None)

    def _get_default_value(self):
        if callable(self.default):
            if self.default_args:
                if self.default_kwargs:
                    result = self.default(*self.default_args, **self.default_kwargs)
                else:
                    result = self.default(**self.default_kwargs)
            elif self.default_kwargs:
                result = self.default(**self.default_kwargs)
            else:
                result = self.default()
        else:
            result = self.default
        return self.default_cast(result) if self.default_cast else result

    def validate(self, value):
        if value is None and self.default:
            value = self._get_default_value()
        if value is None and not self.null:
            raise ValueError("%s can't be None" % self.name)
        if self._available_options and not value in self._available_options:
            raise ValueError('%s value is not present in options %s ' % (
                self.name, self._available_options))
        return value

    @classmethod
    def serialize(cls, value):
        """ Convert a native python into a primitive type """
        return value

    @classmethod
    def deserialize(cls, value):
        """ Convert a primitive type into a native python type """
        return value


class StringField(Field):
    def __init__(self, **kwargs):
        super(StringField, self).__init__(**kwargs)
        self.max_length = kwargs.get('max_length', None)

    def validate(self, value, **kwargs):
        value = super(StringField, self).validate(value)
        if value is None:
            return

        if not isinstance(value, (str, unicode)):
            raise ValueError('%s is from type %s and not (str, unicode) ' % (
                self.name, value.__class__.__name__))

        if self.max_length and len(value) > self.max_length:
            raise ValueError('%s has length %s which is bigger than %s' % (
                self.name, len(value), self.max_length))
        return value


class UUIDField(Field):
    def __init__(self, **kwargs):
        super(UUIDField, self).__init__(**kwargs)

    def validate(self, value, name=None, **kwargs):
        value = super(UUIDField, self).validate(value)
        if value is None:
            return
        if not isinstance(value, (uuid.UUID)):
            raise ValueError('%s is from type %s and not (uuid) ' % (
                self.name, value.__class__.__name__))
        return value

    def serialize(self, value):
        return str(value)


class IntegerField(Field):
    def __init__(self, **kwargs):
        super(IntegerField, self).__init__(**kwargs)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)

    def validate(self, value, name=None, **kwargs):
        value = super(IntegerField, self).validate(value)
        if value is None:
            return

        if not isinstance(value, (int, long)):
            raise ValueError('%s is from type %s and not (int, long) ' % (
                self.name, value.__class__.__name__))

        if self.min:
            if self.min > value:
                raise ValueError(
                    'the assigned value %s for %s is less than the minimum allowed, min: %s' % (
                        value, self.name, self.min))

        if self.max:
            if self.max < value:
                raise ValueError(
                    "the value %s assigned to %s is greater than the maximum allowed, max: %s" % (
                        value, self.name, self.max))
        return value


class FloatField(Field):
    def __init__(self, **kwargs):
        super(FloatField, self).__init__(**kwargs)

    def validate(self, value, name=None, **kwargs):
        value = super(FloatField, self).validate(value)
        if value is None:
            return

        if not isinstance(value, (float)):
            raise ValueError('%s is from type %s and not (float) ' % (
                self.name, value.__class__.__name__))
        return value


class BooleanField(Field):
    def __init__(self, **kwargs):
        super(BooleanField, self).__init__(**kwargs)

    def validate(self, value, name=None, **kwargs):
        value = super(BooleanField, self).validate(value)
        if value is None:
            return

        if not isinstance(value, (bool)):
            raise ValueError('%s is from type %s and not (bool) ' % (
                self.name, value.__class__.__name__))
        return value


class ListField(Field):
    def __init__(self, **kwargs):
        super(ListField, self).__init__(**kwargs)

    def validate(self, value, **kwargs):
        value = super(ListField, self).validate(value)
        if value is None:
            return

        if not isinstance(value, (list)):
            raise ValueError('%s is from type %s and not (list) ' % (
                self.name, value.__class__.__name__))
        return value


class SetField(Field):
    def __init__(self, **kwargs):
        super(SetField, self).__init__(**kwargs)

    def validate(self, value, **kwargs):
        value = super(SetField, self).validate(value)
        if value is None:
            return

        if not isinstance(value, (set, frozenset)):
            raise ValueError('%s is from type %s and not (set, frozenset) ' % (
                self.name, value.__class__.__name__))
        return value

    @classmethod
    def serialize(cls, value):
        if value is None:
            return value
        return list(value)

    @classmethod
    def deserialize(cls, value):
        return set(value)


class DictField(Field):
    def __init__(self, **kwargs):
        super(DictField, self).__init__(**kwargs)

    def validate(self, value, name=None, **kwargs):
        value = super(DictField, self).validate(value)
        if value is None:
            return

        if not isinstance(value, dict):
            raise ValueError('%s is from type %s and not (dict) ' % (
                self.name, value.__class__.__name__))
        return value


class DateTimeField(Field):
    RESOLUTION = timedelta(milliseconds=1)
    DEFAULT_FORMAT = "%Y-%m-%dT%H:%M:%S"
    REGEXP = re.compile(
        r"^(?P<year>\d{4})-?(?P<month>\d{2})-?(?P<day>\d{2})(( |T)?"
        r"(?P<hour>\d{2}):?(?P<min>\d{2}):?(?P<sec>\d{2})\.?(?P<us>\d+)?)?$")

    def __init__(self, **kwargs):
        super(DateTimeField, self).__init__(**kwargs)

    def validate(self, value, **kwargs):
        value = super(DateTimeField, self).validate(value)
        if value is None:
            return

        if not isinstance(value, datetime):
            raise ValueError('%s is from type %s and not (datetime) ' % (
                self.name, value.__class__.__name__))
        return value

    @classmethod
    def serialize(cls, value):
        if value is None:
            return
        return value.strftime(cls.DEFAULT_FORMAT)

    @classmethod
    def deserialize(cls, value):
        if isinstance(value, basestring):
            return datetime.strptime(value, cls.DEFAULT_FORMAT)
        elif isinstance(value, datetime):
            return value
        else:
            raise ValueError("Unknown %s type to deserialize" % value.__class__.__name__)

    def now(self):
        return datetime.utcnow().isoformat()


class GeoPointField(Field):

    def __init__(self, **kwargs):
        super(GeoPointField, self).__init__(**kwargs)

    def validate(self, value, **kwargs):
        value = super(GeoPointField, self).validate(value)
        if value is None:
            return

        if isinstance(value, dict):
            keys = value.keys()
            if not "lat" in keys or not "lon" in keys:
                raise ValueError('%s must contain "lat" and "lon" keys when is a dict' % (
                    self.name))
        else:
            if not isinstance(value, tuple) and not isinstance(value, list):
                raise ValueError('%s must be a tuple, dict or list not %s' % (
                    self.name, value.__class__.__name__))

            if len(value) != 2:
                raise ValueError('%s must be a tuple/list with two entries (lat, lon)' % (
                    self.name))
        return value

    @classmethod
    def serialize(cls, value):
        if value is None:
            return value

        if isinstance(value, dict):
            return dict(lat=value["lat"], lon=value["lon"])
        else:
            return dict(lat=value[0], lon=value[1])

    @classmethod
    def deserialize(cls, value):
        if value is None:
            return value
        elif isinstance(value, dict):
            return value["lat"], value["lon"]
        elif isinstance(value, list):
            return value[0], value[1]
        elif isinstance(value, tuple):
            return value[0], value[1]
        else:
            raise ValueError('Unknown type %s to deserialize ' % (
                value.__class__.__name__))

if __name__ == '__main__':
    print DateTimeField.deserialize("2015-04-01 13:25:22")
    print DateTimeField.deserialize("2015-04-01")
    print DateTimeField.deserialize("2015-05-25T10:43:03.485141")
    print DateTimeField.deserialize("2015-05-25 10:43:03.485141")
    print DateTimeField.deserialize("20150601131522")
    print DateTimeField.deserialize("20150601131522000")
    print DateTimeField.deserialize("20150601131522")
    print DateTimeField.deserialize(20150601131522000)
