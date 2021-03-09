from cryspnet.utils import FeatureGenerator, load_input, dump_output, group_outputs, descriptionfile, topkacc
from cryspnet.models import load_Bravais_models, load_Lattice_models, load_SpaceGroup_models
from cryspnet.config import *
from random_crystal import make_stoi

import argparse

featurizer = FeatureGenerator()

def make_predictions(input:str, output:str, which:str='whole', topn_bravais:int=TOPN_BRAVAIS,
                     topn_spacegroup:int=TOPN_SPACEGROUP, n_ensembler:int=N_ESMBLER,
                     batch_size:bool=BATCHSIZE, cpu:bool=False, run_version:str=None):
    args = {key: value for key, value in locals().items() if key not in 'self'}
    output = Path(output)
    if output.suffix != ".csv":
        file_path = output.joinpath(f"predictions{run_version}.csv")
    else:
        file_path = output
        output = output.parent

    output.mkdir(exist_ok=True)

    BE = load_Bravais_models(
        n_ensembler=n_ensembler,
        which=which,
        batch_size=batch_size,
        cpu=cpu)
    LPB = load_Lattice_models(batch_size=batch_size, cpu=cpu)
    SGB = load_SpaceGroup_models(batch_size=batch_size, cpu=cpu)

    formula = load_input(input)
    formula['formula'] = formula['formula'].map(make_stoi)
    ext_magpie = featurizer.generate(formula)

    bravais_probs, bravais = BE.predicts(ext_magpie, topn_bravais=topn_bravais)

    lattices = []
    spacegroups = []
    spacegroups_probs = []

    for i in range(topn_bravais):
        ext_magpie["Bravais"] = bravais[:, i]
        lattices.append(LPB.predicts(ext_magpie))
        sg_prob, sg = SGB.predicts(ext_magpie, topn_spacegroup=topn_spacegroup)
        spacegroups.append(sg)
        spacegroups_probs.append(sg_prob)

    out = group_outputs(bravais, bravais_probs, spacegroups, spacegroups_probs, lattices, formula)
    out = out.drop_duplicates()
    dump_output(out, file_path, index=False)
    descriptionfile("prediction", **args)

def main():

    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("-i", "--input", default=None, type=str, required=True,
                        help="The input data path. The program accept .csv, .xlsx file.")
    parser.add_argument("-o", "--output", default=None, type=str, required=True,
                        help="The output directory where predictions for \
                            Bravais Lattice, Space Group, and Lattice  will be written.")
    parser.add_argument("--use_metal", action='store_true',
                        help="Whether to run prediction on the Bravais Lattice model that trained on metal subset.")
    parser.add_argument("--use_oxide", action='store_true',
                        help="Whether to run prediction on the Bravais Lattice model that trained on oxide subset.")
    parser.add_argument("--n_ensembler", default=N_ESMBLER, type=int,
                        help="number of ensembler for Bravais Lattice Prediction.")
    parser.add_argument("--topn_bravais", default=TOPN_BRAVAIS, type=int,
                        help="The top-n Bravais Lattice the user want to pre \
                        serve. The space group and lattice parameter would \
                        be predicted for each top-n Bravais Lattice"
            )
    parser.add_argument("--topn_spacegroup", default=TOPN_SPACEGROUP, type=int,
                        help="The top-n Space Group the user want to pre \
                        serve."
            )
    parser.add_argument("--batch_size", default=BATCHSIZE, type=int,
                        help="Batch size per GPU/CPU for prediction.")
    parser.add_argument("--no_cuda", action='store_true',
                        help="Avoid using CUDA when available")
    parser.add_argument("--run_version", default=None, type=str,
                        help="Any descriptor that the user may want to add to characterize the run. \
                            Will be appended to the end of the descriptor file name."
                        )

    args = parser.parse_args()

    if args.no_cuda:
        cpu = True
    else:
        cpu = False
    if args.use_metal and args.use_oxide:
        raise Exception("Could only select --use_metal or --use_oxide")
    elif args.use_metal:
        which = "metal"
    elif args.use_oxide:
        which = "oxide"
    else:
        which = "whole"

    make_predictions(args.input, args.output, which, args.topn_bravais,
                        args.topn_spacegroup, args.n_esembler,
                        args.batch_size, cpu)

if __name__ == "__main__":
    main()
