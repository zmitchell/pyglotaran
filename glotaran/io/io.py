from __future__ import annotations

import xarray as xr

from glotaran.model import Model
from glotaran.parameter import ParameterGroup
from glotaran.project import Result
from glotaran.project import SavingOptions
from glotaran.project import Scheme


class Io:
    def read_model(self, fmt: str, file_name: str) -> Model:
        raise NotImplementedError

    def write_model(self, fmt: str, file_name: str, model: Model):
        raise NotImplementedError

    def read_parameters(self, fmt: str, file_name: str) -> ParameterGroup:
        raise NotImplementedError

    def write_parameters(self, fmt: str, file_name: str, parameters: ParameterGroup):
        raise NotImplementedError

    def read_scheme(self, fmt: str, file_name: str) -> Scheme:
        raise NotImplementedError

    def write_scheme(self, fmt: str, file_name: str, scheme: Scheme):
        raise NotImplementedError

    def read_dataset(self, fmt: str, file_name: str) -> xr.DataSet | xr.DataArray:
        raise NotImplementedError

    def write_dataset(
        self, fmt: str, file_name: str, saving_options: SavingOptions, dataset: xr.DataSet
    ):
        raise NotImplementedError

    def read_result(self, fmt: str, file_name: str) -> Result:
        raise NotImplementedError

    def write_result(
        self, fmt: str, file_name: str, saving_options: SavingOptions, result: Result
    ):
        raise NotImplementedError
