from random_crystal import generate_crystals
from predict import make_predictions
from cryspnet.utils import topkacc
from cryspnet.compare_structures import compare
from pathlib import Path

# required parameters ; only change these or the optional params
ipt = "generate_structures/non-oxides.csv"
output = 'generate_structures/version6/6-1/non-oxides/'
run_version = "V6(non-oxides)"
predictions = True
crystals = True

# Parameters for structure predictions
# required params ; don't change
pred_input = ipt
pred_output = output

# optional parameters
# commented parameters will use defaults
which_model = 'whole'  # 'whole', 'metal' or 'oxide'
topn_bravais = 1
topn_spacegroup = 1
n_ensembler = 14  # max 14 models provided
# batch_size =
cpu = True
if predictions is True:
    make_predictions(input=pred_input, output=pred_output,
                     which=which_model,
                     topn_bravais=topn_bravais,
                     topn_spacegroup=topn_spacegroup,
                     n_ensembler=n_ensembler,
                     # batch_size=batch_size,
                     cpu=cpu,
                     run_version=run_version)

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
    # commented parameters will use defaults
    topn_bravais = 1
    topn_spacegroup = 1
    n_workers = 4  # number of concurrent processes
    n_trails = 10  # number of lattices to generate per composition
    timeout = 300  # seconds before timing out of a process
    formula_only = False
    space_group_only = True
    max_atoms = 500

    generate_crystals(input=crys_input, output=crys_output,
                      # error=error,
                      topn_bravais=topn_bravais,
                      topn_spacegroup=topn_spacegroup,
                      n_workers=n_workers,
                      n_trails=n_trails,
                      timeout=timeout,
                      formula_only=formula_only,
                      space_group_only=space_group_only,
                      max_atoms=max_atoms,
                      run_version=run_version
                      )