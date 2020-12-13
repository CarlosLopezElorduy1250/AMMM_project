#!/opt/miniconda3/envs/ammm/bin/python

### Created: Dec, 2020
### Authors: Paula Iborra, Carlos López 

import sys, os, yaml, time
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
    config = read_yaml(args.config)
    if config["verbose"]==True: sys.stderr.write("Read configuration file\n")
    d_center, name2location, name2city, name2type = parse_input(config["inputDataFile"])

    if config["verbose"]==True: sys.stderr.write("Solver method: {}\n".format(config["solver"])) 
    
    if config["solver"]=="Greedy":
        startTime = time.time()
        greedy = Solver_Greedy().solve(d_center, name2location, name2city, name2type)
        finalTime = round(time.time() - startTime, 5)
        if greedy == 0:
            if config["verbose"]==True: sys.stderr.write("Solution not found\n")
            with open(config["solutionFile"], 'w+') as output:
                output.write("Data from: %s\n" %(config["inputDataFile"]))
                output.write("Solution not found.")

        else:
            if config["verbose"]==True: sys.stderr.write("Solution found. Written to: %s\n" %(config["solutionFile"]))
            with open(config["solutionFile"], 'w+') as output:
                output.write("Data from: %s\n" %(config["inputDataFile"]))
                output.write("Execution time: {}".format(finalTime))
                output.write("\n"+"#"*98+"\n\n")
                output.write("Solution with cost: %s \n\n"%(greedy[2]))
                for city in greedy[0].keys():
                    output.write(greedy[0][city].print_class())
                output.write("\n")
                for loc in greedy[1].keys(): 
                    output.write(greedy[1][loc].print_class())
                output.write("\n"+"#"*98+"\n\n")


    if config["verbose"]==True: sys.stderr.write("Execution time: {}".format(finalTime)+"\nDONE!\n")
    sys.exit(0)



