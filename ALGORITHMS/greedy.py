import sys
from library import *
from argparse import ArgumentParser, RawTextHelpFormatter

nLocations, nCities, nTypes, p, posCities, posLocations, d_city, cap, cost, d_center, name2location, name2city, name2type = parse_input("../INPUTS/project.1.dat")

city2centres            = {}    # Dictionary that relates each city with primary and secondary centre                       -> city2centres[City] = (primary, secondary)
centre2cities_primary   = {}    # Dictionary relating each centre with the cities where it serves as a primary centre       -> centre2cities_primary[Centre]   = [city1, city2, ...]
centre2cities_secondary = {}    # Dictionary relating each centre with the cities where it serves as a secondary centre     -> centre2cities_secondary[Centre] = [city1, city2, ...]



# for city in posCities:
#     print(city)
#     for location in posLocations:
#         print("\t{}".format(location))
#         print("\t\t{}".format(distance(city, location)))