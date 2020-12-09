import sys, random
from library import *
from argparse import ArgumentParser, RawTextHelpFormatter

nLocations, nCities, nTypes, p, posCities, posLocations, d_city, cap, cost, d_center, name2location, name2city, name2type = parse_input("INPUTS/project.1.dat")

unserved_c = set()  # Set of cities with out primary, secondary or both centers
for c in name2city.keys():
    unserved_c.add(c)

unocupied_l = set() # Unoccupied locations
for l in name2location.keys():
    unocupied_l.add(l)

# city2centres            = {}    # Dictionary that relates each city with primary and secondary centre                       -> city2centres[City] = (primary, secondary)
# centre2cities_primary   = {}    # Dictionary relating each centre with the cities where it serves as a primary centre       -> centre2cities_primary[Centre]   = [city1, city2, ...]
# centre2cities_secondary = {}    # Dictionary relating each centre with the cities where it serves as a secondary centre     -> centre2cities_secondary[Centre] = [city1, city2, ...]

# city2isComplete         = {}    # Dictionary relating each city to a boolean. True -> has both primary and secondary | False -> otherwise
# for c in name2city.keys():
#     city2isComplete[c] = False

def sort_type_cost(name2type = name2type):
    '''
    Returns a list of the center types sorted from the lowest cost to the highest
    '''

    cost_order = []

    while len(cost_order) < len(name2type.keys()):
        min_cost = 9999999999
        for t in name2type.keys():
            if t not in cost_order:
                if name2type[t].cost < min_cost:
                    min_cost = name2type[t].cost
                    type_mincost = t
        cost_order.append(type_mincost)
    
    return cost_order

def add_cType2location(c_type, location):
    '''
    Adds the type of center to the location
    '''

    global name2location
    name2location[location].type = c_type

if __name__ == "__main__":
    index_minCost = 0     # Index that tells us which type are we currently trying to introduce in locations
    cost_order = sort_type_cost()

    while len(unserved_c)>0:
        current_location = random.sample(unocupied_l, 1)[0]
        add_cType2location(cost_order[index_minCost], current_location)
        for c in name2city.keys():
            if c in unserved_c:
                dist_c2l = distance( (name2city[c].cx, name2city[c].cy) , (name2location[current_location].lx, name2location[current_location].ly) )
                if  dist_c2l< d_city[index_minCost]:
                    if name2city[c].primary_l is not None and name2city[c].secondary_l is None:
                        name2city[c].secondary_l = current_location
                    elif name2city[c].primary_l is None:
                        name2city[c].primary_l = current_location
                elif dist_c2l < 3*d_city[index_minCost]:
                    if name2city[c].secondary_l is None:
                        name2city[c].secondary_l = current_location
            
                if name2city[c].primary_l is not None and name2city[c].secondary_l is not None:
                    unserved_c.remove(c)
        unocupied_l.remove(current_location)

    

# location2cities_primary   = {}
# location2cities_secondary = {}

# for location in name2location.keys():
#     location2cities_primary[location] = []
#     for city in name2city.keys():
#         if distance( (name2location[location].lx, name2location[location].ly), (name2city[city].cx, name2city[city].cy)) < 

# for city in posCities:
#     print(city)
#     for location in posLocations:
#         print("\t{}".format(location))
#         print("\t\t{}".format(distance(city, location)))