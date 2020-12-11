import sys, random
from library import *
from argparse import ArgumentParser, RawTextHelpFormatter
from itertools import combinations

nLocations, nCities, nTypes, p, posCities, posLocations, d_city, cap, cost, d_center, name2location, name2city, name2type = parse_input("INPUTS/project.1.dat")

unserved_c = set()  # Set of cities without primary, secondary or both centers
for c in name2city.keys():
    unserved_c.add(c)

unoccupied_l = set() # Unoccupied locations
for l in name2location.keys():
    unoccupied_l.add(name2location[l].coord)

occupied_l = set()

location2sumdist = {}   # Sum of distances for each location to each city

centre2cities_primary   = {}    # Dictionary relating each centre with the cities where it serves as a primary centre       -> centre2cities_primary[Centre]   = [city1, city2, ...]
centre2cities_secondary = {}    # Dictionary relating each centre with the cities where it serves as a secondary centre     -> centre2cities_secondary[Centre] = [city1, city2, ...]



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


def selectLocation(unoccupied_l = unoccupied_l, unserved_c = unserved_c):
    global location2sumdist

    min_location = (None, 99999)
    for location in unoccupied_l:
        location2sumdist[location] = 0
        # print(location)

        for city in unserved_c:
            city = name2city[city].coord
            # print("\t{}".format(city))
            # print("\t\t{}".format(distance(city, location)))
            location2sumdist[location] += distance(city, location)
        if location2sumdist[location] < min_location[1]:
            min_location = (location, location2sumdist[location])
    
    return min_location[0]


def assign_type2location(l, unserved_c = unserved_c, name2type = name2type, name2city = name2city, p = p):
    '''
    Returns:
        [0]: Tupple (type, cost_per_city)
        [1]: Tupple (primary_cities, secondary_cities)
    '''   
    type_citycost = (None, 99999) # (c_type, costCity) Tupple where the 1st element is type of the center and 2nd is the cost per city
    cities_served = (set(), set())
    for t in name2type.keys():
        filled_cap = 0
        primary, possible_secondary, secondary = set(), set(), set()
        for c in unserved_c:
            if distance( l , name2city[c].coord) <= name2type[t].d_city and name2city[c].pc <= name2type[t].cap - filled_cap and name2city[c].primary_l is None:
                filled_cap += name2city[c].pc
                primary.add(c)
            elif distance( l, name2city[c].coord) <= 3 * name2type[t].d_city and name2city[c].secondary_l is None:
                possible_secondary.add(c)
        
        if name2type[t].cap > filled_cap:
            for c in possible_secondary:
                if name2city[c].pc * 0.1 <= name2type[t].cap - filled_cap:
                    secondary.add(c)
                    filled_cap += name2city[c].pc * 0.1

        cost_type = name2type[t].cost / filled_cap
        print("Type: {} | cost_type: {} | primary: {} | secondary: {}".format(t, cost_type, primary, secondary))
        if cost_type < type_citycost[1]:
            type_citycost = (t, cost_type)
            cities_served = (primary, secondary)
    return type_citycost, cities_served





if __name__ == "__main__":
    min_location = selectLocation(unoccupied_l, unserved_c)

    while len(unserved_c) > 0:
        while len(unoccupied_l) > 0:
            type_citycost, cities_served = assign_type2location(min_location)
            unoccupied_l.remove(min_location)
            occupied_l.add(min_location)
            if len(cities_served[0]) > 0:
                for c in cities_served[0]:
                    name2city[c].primary_l = min_location
            if len(cities_served[1]) > 0:
                for c in cities_served[1]:
                    name2city[c].secondary_l = min_location
            for c in name2city.keys():
                if c in unserved_c:
                    if name2city[c].primary_l is not None and name2city[c].secondary_l is not None:
                        unserved_c.remove(c)

            f0 = False
            new_location = selectLocation(unoccupied_l, unserved_c)

            while not f0:
                for l in occupied_l:
                    if new_location is not None and distance(new_location, l) < d_center:
                        unoccupied_l.remove(new_location)
                        new_location = selectLocation(unoccupied_l, unserved_c)
                        break
                else:
                    f0 = True
                    min_location = new_location


