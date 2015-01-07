import argparse
import json
import os

import marl.fileutils as futil

from dl4mir.common import util
import dl4mir.chords.evaluate as EVAL


METRICS = EVAL.COMPARISONS.keys()
METRICS_ENUM = dict([(k, i) for i, k in enumerate(METRICS)])


def main(args):
    ref_jamset = util.load_jamset(args.ref_jamset)
    est_jamset = util.load_jamset(args.est_jamset)
    keys = est_jamset.keys()
    keys.sort()

    ref_annots = [ref_jamset[k].chord[0] for k in keys]
    est_annots = [est_jamset[k].chord[0] for k in keys]

    results = EVAL.tally_scores(
        ref_annots, est_annots, args.min_support, METRICS)

    output_dir = os.path.split(args.output_file)[0]
    futil.create_directory(output_dir)

    with open(args.output_file, 'w') as fp:
        json.dump(results, fp, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")

    # Inputs
    parser.add_argument("ref_jamset",
                        metavar="ref_jamset", type=str,
                        help="Path to a JAMSet to use as a reference.")
    parser.add_argument("est_jamset",
                        metavar="est_jamset", type=str,
                        help="Path to a JAMSet to use as an estimation.")
    # Outputs
    parser.add_argument("output_file",
                        metavar="output_file", type=str,
                        help="Path for saving the results as JSON.")
    parser.add_argument("--min_support",
                        metavar="--min_support", type=float, default=60.0,
                        help="Minimum label duration for macro-quality stats.")
    main(parser.parse_args())
