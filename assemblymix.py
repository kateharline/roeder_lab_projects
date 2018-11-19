import numpy as np
# calculation parameters
# rxn specific
insert_concs = [215.1, 178.6]
insert_sizes = [1.6, 2.5]
vector_conc = 92
vector_size = 14

# NEB set
insert_vector_ratio = 2
max_vectors_mix = 10
pmol_range = [0.03, .2]
max_vector_vol = 10

# calculate ng from ul and conc ng/ul
def ng(conc, ul):
    return conc * ul


# calculate ul from ng and conc ng/ul
def ul(conc, ng):
    return ng / conc

# calc insert vols from ngs
def get_insert_vols(insert_ngs, insert_concs):
    return [ ul(insert_concs[i], insert_ngs[i]) for i in range(0, len(insert_ngs))]

# calc pmols from ng and bp
def pmols(ng, bp):
    return ng / (bp *650)

# calc ng from pmols and bp
def ng_desired(pmols, bp):
    return pmols * bp * 650

# ng needed for each insert based on vector pmols
def get_ng_desired(vector_pmols, insert_vector_ratio, insert_sizes):

    return [ ng_desired(vector_pmols*insert_vector_ratio, size) for size in insert_sizes ]

def optimize_vols(insert_concs, vector_conc, insert_vector_ratio, total_mix, pmol_range):

    for vector_vol in np.arange(0, max_vector_vol, .1):
        vector_ng = ng(vector_conc, vector_vol)
        vector_pmols = pmols(vector_ng, vector_size)

        if pmol_range[0]<=vector_pmols<=pmol_range[1]:
            insert_ngs = get_ng_desired(vector_pmols, insert_vector_ratio, insert_sizes)

            insert_vols = get_insert_vols(insert_ngs, insert_concs)

            total_mix = vector_vol + sum(insert_vols)

            if total_mix <= max_vectors_mix:
                return vector_vol, vector_pmols, insert_vols
            else:
                continue

        else:
            continue



vols = optimize_vols(insert_concs, vector_conc, insert_vector_ratio, total_mix, pmol_range)

print(vols)
