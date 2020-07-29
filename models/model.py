# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
import util


class Model(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None):  # noqa: E501
        """Model - a model defined in OpenAPI

        :param id: The id of this Model.  # noqa: E501
        :type id: int
        :param name: The name of this Model.  # noqa: E501
        :type name: str
        """
        self.openapi_types = {
            'id': int,
            'name': str
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name'
        }

        self._id = id
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'Model':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Model of this Model.  # noqa: E501
        :rtype: Model
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Model.


        :return: The id of this Model.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Model.


        :param id: The id of this Model.
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Model.

        Name of simulation model  # noqa: E501

        :return: The name of this Model.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Model.

        Name of simulation model  # noqa: E501

        :param name: The name of this Model.
        :type name: str
        """

        self._name = name

