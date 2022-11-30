psr_catalogs = ["Fermi", "ATNF"]
plottable_columns = {
    "P0": "$P$",
    "P1": "$\\dot{P}$",
    "Dist": "$D$",
    "Edot": "$\\dot{E}$",
    "Bsurf": "$B_*$",
}

plottable_columns_r = {v: k for k, v in plottable_columns.items()}