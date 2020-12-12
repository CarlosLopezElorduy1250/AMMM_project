import sys, random
from library import *
from argparse import ArgumentParser, RawTextHelpFormatter
from itertools import combinations

class Solver_Greedy:

    def sort_type_cost(self, name2type):
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


    def selectLocation(self, unoccupied_l, unserved_c, name2city):
        '''
        Selects location with minim sum of distances to all cities. Returns location coordiantes
        '''

        # location2sumdist = {} # location2sumdist[location] = sumdist 

        # min_location = (None, 99999)
        # for location in unoccupied_l:
        #     location2sumdist[location] = 0
        #     for city in unserved_c:
        #         location2sumdist[location] += distance(city, location)
        #     if location2sumdist[location] < min_location[1]:
        #         min_location = (location, location2sumdist[location])
        
        # return min_location[0]

        return random.sample(unoccupied_l,1)[0]


    def assign_type2location(self, l, unserved_c, name2type, name2city):
        '''
        Assign type of center to location minimizing the cost function.
            Cost function: for each type calculates the ratio total_cost/population_served
        Returns:
            [0]: Type with minimum ratio cost
            [1]: Tupple (primary_cities, secondary_cities)
        '''
        type_citycost = (None, 99999) # (c_type, costCity) Tupple where the 1st element is type of the center and 2nd is the cost per city
        cities_served = (set(), set())
        for t in name2type.keys():
            filled_cap = 0
            primary, possible_secondary, secondary = set(), set(), set()
            for c in unserved_c:
                if distance(l, c) <= name2type[t].d_city and name2city[c].pc <= name2type[t].cap - filled_cap and name2city[c].primary_l is None:
                    filled_cap += name2city[c].pc
                    primary.add(c)
                elif distance(l, c) <= 3 * name2type[t].d_city and name2city[c].secondary_l is None:
                    possible_secondary.add(c)
            
            if name2type[t].cap > filled_cap:
                for c in possible_secondary:
                    if name2city[c].pc * 0.1 <= name2type[t].cap - filled_cap:
                        secondary.add(c)
                        filled_cap += name2city[c].pc * 0.1

            cost_type = name2type[t].cost / filled_cap
            if cost_type < type_citycost[1]:
                type_citycost = (t, cost_type)
                cities_served = (primary, secondary)
        
        if cities_served != (set(),set()):
            return type_citycost[0], cities_served, name2type[type_citycost[0]].cap - filled_cap
        else:
            return 0


    def solve(self, d_center, name2location, name2city, name2type):

        # Set of cities without primary, secondary or both centers
        unserved_c = set()  
        for c in name2city.keys():
            unserved_c.add(c)

        # Unoccupied locations
        unoccupied_l = set() 
        for l in name2location.keys():
            unoccupied_l.add(l)

        # Initialize occupied locations
        occupied_l = set()

        # Initialize total cost
        total_cost = 0
        
        min_location = self.selectLocation(unoccupied_l, unserved_c, name2city)

        while len(unserved_c) > 0:
            if len(unoccupied_l) > 0:
                isLocValid = False
                try:
                    type_loc, cities_served, remaining_cap = self.assign_type2location(min_location,unserved_c, name2type, name2city)
                    isLocValid = True

                except:
                    unoccupied_l.remove(min_location)
                    if len(unoccupied_l) > 0:
                        min_location = self.selectLocation(unoccupied_l, unserved_c, name2city)

                if isLocValid:
                    unoccupied_l.remove(min_location)
                    occupied_l.add(min_location)
                    name2location[min_location].type = type_loc
                    total_cost += name2type[type_loc].cost
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

                    if len(unoccupied_l) > 0:
                        f0 = False      # True if a new location is valid
                        new_location = self.selectLocation(unoccupied_l, unserved_c, name2city)

                        while not f0 and len(unoccupied_l) > 0:
                            for l in occupied_l:
                                if distance(new_location, l) < d_center:
                                    unoccupied_l.remove(new_location)

                                    if len(unoccupied_l) > 0:
                                        new_location = self.selectLocation(unoccupied_l, unserved_c, name2city)
                                    break
                            else:
                                f0 = True   
                                min_location = new_location
            else:
                return 0

        return name2city, name2location, total_cost
