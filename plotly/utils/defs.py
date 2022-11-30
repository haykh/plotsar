from num2tex import num2tex
from num2tex import configure as num2tex_configure

num2tex_configure(exp_format="cdot", help_text=False, display_singleton=False)


def exp_tex(float_number):
    ret = "{:.2g}".format(num2tex(float_number))
    if ret.startswith("\cdot"):
        ret = ret.replace("\cdot", "")
    return ret


def to_label(label, unit):
    return f"{label} [{unit}]" if unit else label


psr_catalogs = ["Fermi", "ATNF"]
plottable_columns = {
    "P0": "Period",
    "P1": "Spindown rate",
    "Dist": "Distance",
    "Edot": "Spindown power",
    "Bsurf": "Surface magnetic field",
}

plottable_columns_r = {v: k for k, v in plottable_columns.items()}

categorical_columns = {"Catalog": "Catalog", **plottable_columns}
categorical_columns_r = {v: k for k, v in categorical_columns.items()}
