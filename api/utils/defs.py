from num2tex import num2tex
from num2tex import configure as num2tex_configure
from .physics import *

num2tex_configure(exp_format="cdot", help_text=False, display_singleton=False)


def exp_tex(float_number):
    ret = "{:.2g}".format(num2tex(float_number))
    if ret.startswith("\cdot"):
        ret = ret.replace("\cdot", "")
    return ret


def to_label(label, unit):
    return f"{label} [{unit}]" if unit else label


additional_quantities = {
    "Bsurf": ("Surface magnetic field", "G", ComputeBsurf),
    "BLC": ("Magnetic field at LC", "G", ComputeBLC),
    "RLC": ("Light cylinder", "km", ComputeRLC),
    "gmax": ("Polar cap voltage", "m_e c^2", ComputeGmax),
    "gradLC": ("Burnoff limit at LC", "m_e c^2", ComputeGammaradLC),
}

psr_catalogs = ["Fermi", "ATNF"]
plottable_columns = {
    "P0": "Period",
    "P1": "Spindown rate",
    "Dist": "Distance",
    "Edot": "Spindown power",
    **{k: v[0] for k, v in additional_quantities.items()},
}

plottable_columns_r = {v: k for k, v in plottable_columns.items()}

categorical_columns = {"Catalog": "Catalog", **plottable_columns}
categorical_columns_r = {v: k for k, v in categorical_columns.items()}
