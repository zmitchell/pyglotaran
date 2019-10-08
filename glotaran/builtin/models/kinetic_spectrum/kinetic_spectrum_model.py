import typing
import numpy as np
import xarray as xr

from glotaran.model import model
from glotaran.parameter import ParameterGroup

from glotaran.builtin.models.kinetic_image.kinetic_image_megacomplex \
    import KineticImageMegacomplex
from glotaran.builtin.models.kinetic_image.kinetic_image_model import KineticImageModel

from .kinetic_spectrum_dataset_descriptor import KineticSpectrumDatasetDescriptor
from .kinetic_spectrum_matrix import kinetic_spectrum_matrix
from .kinetic_spectrum_result import finalize_kinetic_spectrum_result
from .spectral_constraints import SpectralConstraint, OnlyConstraint, ZeroConstraint
from .spectral_irf import IrfSpectralGaussian
from .spectral_matrix import spectral_matrix
from .spectral_penalties import EqualAreaPenalty
from .spectral_relations import SpectralRelation, apply_spectral_relations
from .spectral_shape import SpectralShape


def apply_spectral_constraints(
        model: typing.Type['KineticModel'],
        clp_labels: typing.List[str],
        matrix: np.ndarray,
        index: float) -> typing.Tuple[typing.List[str], np.ndarray]:
    for constraint in model.spectral_constraints:
        if isinstance(constraint, (OnlyConstraint, ZeroConstraint)) and constraint.applies(index):
            idx = [not label == constraint.compartment for label in clp_labels]
            clp_labels = [label for label in clp_labels if not label == constraint.compartment]
            matrix = matrix[:, idx]
    return (clp_labels, matrix)


def spectral_constraint_penalty(
        model: typing.Type['KineticModel'],
        datasets: typing.Dict[str, xr.Dataset],
        parameter: ParameterGroup,
        clp_labels: typing.List[str],
        clp: np.ndarray,
        matrix: any) -> np.ndarray:
    residual = []
    #  for equal_area_penalty in model.equal_area_penalties:
    #      equal_area_penalty = equal_area_penalty.fill(model, parameter)
    #      source_idx = clp_labels.index(constraint.compartment)
    #      target_idx = clp_labels.index(constraint.target)
    #      residual.append(
    #          (clp[source_idx] - constraint.parameter * clp[target_idx]) * constraint.weight
    #      )
    return residual


def apply_kinetic_model_constraints(
        model: typing.Type['KineticModel'],
        parameter: ParameterGroup,
        clp_labels: typing.List[str],
        matrix: np.ndarray,
        index: float):
    clp_labels, matrix = apply_spectral_relations(model, parameter, clp_labels, matrix, index)
    clp_labels, matrix = apply_spectral_constraints(model, clp_labels, matrix, index)
    return clp_labels, matrix


def index_dependend(model: typing.Type['KineticModel']):
    if any([
        isinstance(irf, IrfSpectralGaussian) and irf.dispersion_center is not None
        for irf in model.irf.values()
    ]):
        return True
    if len(model.spectral_relations) != 0:
        return True
    if len(model.spectral_constraints) != 0:
        return True
    return False


def grouped(model: typing.Type['KineticModel']):
    return len(model.dataset) != 1


@model(
    'kinetic-spectrum',
    attributes={
        'equal_area_penalties': EqualAreaPenalty,
        'shape': SpectralShape,
        'spectral_constraints': SpectralConstraint,
        'spectral_relations': SpectralRelation,
    },
    dataset_type=KineticSpectrumDatasetDescriptor,
    megacomplex_type=KineticImageMegacomplex,
    matrix=kinetic_spectrum_matrix,
    matrix_dimension='time',
    global_matrix=spectral_matrix,
    global_dimension='spectral',
    constrain_matrix_function=apply_kinetic_model_constraints,
    additional_penalty_function=spectral_constraint_penalty,
    grouped=grouped,
    index_dependend=index_dependend,
    finalize_data_function=finalize_kinetic_spectrum_result,
)
class KineticSpectrumModel(KineticImageModel):
    pass
