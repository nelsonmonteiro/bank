import string
import random
import inspect
import os
import re
from collections import namedtuple
from django.db import models


# -----------------------------------------------------------------------------
# ABSTRACT MODELS
# -----------------------------------------------------------------------------
class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class BigIDModel(models.Model):
    class Meta:
        abstract = True

    id = models.BigAutoField(primary_key=True)


class BigIDBaseModel(BaseModel):
    class Meta:
        abstract = True

    id = models.BigAutoField(primary_key=True)


# -----------------------------------------------------------------------------
# MODEL HELPERS
# -----------------------------------------------------------------------------
def camelcase_to_underscore(str):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str).lower().strip('_')


def get_namedtuple_choices(name, choices_tuple):
    class Choices(namedtuple(name, [name for val, name, desc in choices_tuple])):
        __slots__ = ()
        _choices = tuple([desc for val, name, desc in choices_tuple])

        def get_choices(self):
            return zip(tuple(self), self._choices)
    return Choices._make([val for val, name, desc in choices_tuple])


def upload_to(instance, filename):
    name, ext = os.path.splitext(filename)
    name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(random.randrange(20, 31)))
    new_filename = '%s%s' % (name, ext.lower())
    path = '%s/%s' % (inspect.getfile(instance.__class__).split('/')[-2], instance.__class__.__name__.lower())
    return os.path.join(path, new_filename)
