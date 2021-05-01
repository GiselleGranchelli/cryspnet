from random_crystal import generate_crystals
from predict import make_predictions
from cryspnet.utils import topkacc
from cryspnet.compare_structures import compare
from pathlib import Path

# required parameters ; only change these and/or the optional params
ipt = "generate_structures/oxide_input.csv"
output = 'generate_structures/test'
run_version = "V6(oxides)"
predictions = True
crystals = True

# Parameters for structure predictions
# required params ; don't change

pred_input = ipt
pred_output = output

# optional parameters
# unincluded parameters will use default values set in CRYSPNet
#model options: 'whole', 'metal' or 'oxide'
if predictions is True:
    pred_params = {}
    with pred_params as pp:
        pp['which'] = 'oxide'  # which model: 'whole', 'metal' or 'oxide'
        pp['topn_bravais'] = 1
        pp['topn_spacegroup'] = 1
        pp['n_ensembler'] = 14  # max 14 models provided
        pp['batch_size'] = 256 #default
        pp['cpu'] = True

    make_predictions(input=pred_input, output=pred_output, **pred_params, run_version=run_version)

# Parameters for crystal generation
# required parameters ; dont change
if crystals is True:
    if pred_output[-3:] != ".csv":
        crys_input = f"{pred_output}/predictions{run_version}.csv"
        crys_output = f"{pred_output}/structures"
    else:
        crys_input = pred_output
        crys_output = pred_output[:pred_output.rfind("//")]

    # optional parameters
    crystal_params = {}
    with crystal_params as cp:
        cp['topn_bravais'] = 1
        cp['topn_spacegroup'] = 1
        cp['n_workers'] = 4  # number of concurrent processes
        cp['n_trails'] = 10  # number of lattices to generate per composition
        cp['timeout'] = 300  # seconds before timing out of a process
        cp['formula_only'] = False
        cp['space_group_only'] = True
        cp['max_atoms'] = 500

    generate_crystals(input=crys_input, output=crys_output, **crystal_params, run_version=run_version)