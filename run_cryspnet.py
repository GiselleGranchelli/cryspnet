from random_crystal import generate_crystals
from predict import make_predictions
from cryspnet.utils import topkacc
from pathlib import Path

# required parameters ; only change these and/or the optional params
ipt = "output/all_input.csv"
output = 'output'
run_version = "V1"
predictions = True
crystals = True

# Parameters for structure predictions
# required params ; don't change

pred_input = ipt
pred_output = output

# optional parameters
# parameters that are not included will use default values set in CRYSPNet
# model options: 'whole', 'metal' or 'oxide'
if predictions is True:
    pred_params = {}
    pred_params['which'] = 'oxide'  # which model: 'whole', 'metal' or 'oxide'
    pred_params['topn_bravais'] = 1
    pred_params['topn_spacegroup'] = 1
    pred_params['n_ensembler'] = 14  # max 14 models provided
    pred_params['cpu'] = True

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
    crystal_params['topn_bravais'] = 1
    crystal_params['topn_spacegroup'] = 1
    crystal_params['n_workers'] = 4  # number of concurrent processes
    crystal_params['n_trails'] = 10  # number of lattices to generate per composition
    crystal_params['timeout'] = 300  # seconds before timing out of a process
    crystal_params['formula_only'] = False
    crystal_params['space_group_only'] = True
    crystal_params['max_atoms'] = 500

    generate_crystals(input=crys_input, output=crys_output, **crystal_params, run_version=run_version)