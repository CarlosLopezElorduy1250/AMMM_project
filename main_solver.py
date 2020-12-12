#!/opt/miniconda3/envs/ammm/bin/python

### Created: Dec, 2020
### Authors: Paula Iborra, Carlos Lópex 

import sys, os, yaml
from argparse import ArgumentParser
from library import *
from ALGORITHMS.greedy import Solver_Greedy

def parse_args():
    ''' 
    Get arguments
    '''

    __doc__ = "  "
    parser = ArgumentParser(
        description=__doc__
        )
    parser.add_argument(
        '-v','--version', 
        action='version', 
        version='%(prog)s 1.0',
        help="Show program's version number and exit"
        )
    parser.add_argument(
        "-c","--config",
       # required=True,
        default=os.path.join(
                os.path.dirname(__file__),
                 "INPUTS","config.yml"),
        help="Input configuration file. (default: %(default)s)",
        metavar="FILE"
        )     
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print log messages to STDERR",
        )
       
    try:
        args = parser.parse_args()
    except(Exception):
        parser.print_help()

    if args.config is None:
        parser.print_help() 
        sys.exit("ERROR! Configuration file required.")

    return args

def read_yaml(config_file):
    ''' 
    Read parameters from configuration file
    '''
    with open(config_file, 'r') as config:
        config = yaml.safe_load(config)
        return(config)

if __name__ == '__main__':
    
    args=parse_args()
    if args.verbose: sys.stderr.write("Reading configuration file...\n")
    config = read_yaml(args.config)
    d_center, name2location, name2city, name2type = parse_input(config["inputDataFile"])

    if args.verbose: sys.stderr.write("Solver method: {}\n".format(config["solver"])) 
    
    if config["solver"]=="Greedy":
        greedy = Solver_Greedy().solve(d_center, name2location, name2city, name2type)
        if greedy == 0:
            sys.stderr.write("Solution not found\n")
        else:
            sys.stderr.write("Solution found!!!\n")
    # if args.verbose: sys.stderr.write("Solution completed successfully!\n")
    sys.exit(0)



