#!/opt/miniconda3/envs/ammm/bin/python

### Created: Dec, 2020
### Authors: Paula Iborra, Carlos Lópex 

import sys, os, yaml
from argparse import ArgumentParser

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
                 "inputs","config.yml"),
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
    config = read_yaml(args.config)

    if args.verbose: 
        sys.stderr.write("Solution completed successfully.\n")
    sys.exit(0)


