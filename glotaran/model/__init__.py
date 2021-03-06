"""Glotaran Model Package

This package contains the Glotaran's base model object, the model decorators and
common model items.
"""

from .attribute import model_attribute
from .attribute import model_attribute_typed
from .base_model import Model
from .dataset_descriptor import DatasetDescriptor
from .decorator import model
from .register import get_model
from .register import known_model
from .register import known_model_names
from .weight import Weight
