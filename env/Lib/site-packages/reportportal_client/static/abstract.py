"""This module provides base abstract class for RP request objects.

Copyright (c) 2018 http://reportportal.io .

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from abc import ABCMeta as _ABCMeta, abstractmethod

__all__ = ["AbstractBaseClass", "abstractmethod"]


class AbstractBaseClass(_ABCMeta):
    """Metaclass fot pure Interfacing.

    Being set as __metaclass__, forbids direct object creation from this
    class, allowing only inheritance. I.e.

    class Interface(object):
        __metaclass__ = AbstractBaseClass
    i = Interface() -> will raise TypeError

    meanwhile,

    class Implementation(Interface):
        pass
    i = Implementation() -> success
    """

    _abc_registry = []

    def __call__(cls, *args, **kwargs):
        """Disable instantiation for the interface classes."""
        if cls.__name__ in AbstractBaseClass._abc_registry:
            raise TypeError("No instantiation allowed for Interface-Class"
                            " '{}'. Please inherit.".format(cls.__name__))

        result = super(AbstractBaseClass, cls).__call__(*args, **kwargs)
        return result

    def __new__(mcs, name, bases, namespace):
        """Register instance of the implementation class."""
        class_ = super(AbstractBaseClass, mcs).__new__(mcs, name,
                                                       bases, namespace)
        if namespace.get("__metaclass__") is AbstractBaseClass:
            mcs._abc_registry.append(name)
        return class_
