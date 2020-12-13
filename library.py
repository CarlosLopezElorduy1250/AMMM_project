import sys
import numpy as np

# ===============
# === CLASSES ===
# ===============

class Type:
    def __init__(self, cap, d_city, cost):
        self.cap = cap
        self.d_city = d_city
        self.cost = cost

class City:
    def __init__(self,pc, coord):
        self.coord = coord
        self.pc = pc
        self.primary_l = None
        self.secondary_l = None
    
    def print_class(self):
        return "City %s is served by: Primary center in location %s || Secondary center in location %s \n" %(self.coord, self.primary_l, self.secondary_l)

class Location:
    def __init__(self, coord):
        self.type = None
        self.coord = coord
    
    def print_class(self):
        if self.type is not None:
            return "Location %s has a center of type %s. \n" %(self.coord, self.type)
        else: return ""

# class Centre:
#     def __init__(self, ctype, clocation, ccities):
#         self.type = ctype           # Class Type
#         self.location = clocation   # Class Location
#         self.cities = ccities       # List of the cities it serves (class Cities)
    
#     def canPrimary(self, city):
#         return distance((city.cx, city.cy),(self.location)) <= self.type.d_city

#     def canSecondary(self, city):
#         return distance((city.cx, city.cy),(self.location)) <= self.type.d_city * 3

#     def exceedsCapacity(self):
#         global centre2cities_primary, centre2cities_secondary

#         result = 0
#         result += centre2cities_primary[self].pc + (centre2cities_secondary[self].pc)*0.1

#         return self.type.cap >= result

# =================
# === FUNCTIONS ===
# =================

def parse_input(dat):
    '''
    Input:
        *.dat   (following the format of "project.template.mod")

    Returns:
        [0] d_center
        [1] name2location
        [2] name2city
        [3] name2type
    '''

    nLocations  = 0
    nCities     = 0
    nTypes      = 0

    d_center    = 0.0   # Minimum distance between centres

    p           = []
    posCities   = []
    posLocations= []

    d_city_input= []
    cap_input   = []
    cost_input  = []

    name2city       = {}
    name2type       = {}
    name2location   = {}

    with open(dat, "r") as data:
        for line in data.readlines():
            line = line.split()
            if line!=[]:
                if line[0][:2] != '//':
                    if line[0] == "nLocations":
                        nLocations = int(line[2][:-1])
                    elif line[0] == "nCities":
                        nCities = int(line[2][:-1])
                    elif line[0] == "nTypes":
                        nTypes = int(line[2][:-1])
                    elif line[0] == "p":
                        start = False
                        for chunk in line:
                            if chunk == "];":
                                start = False

                            if start:
                                p.append(int(chunk))
                                
                            if chunk == "[":
                                start = True
                    elif line[0] == "posCities":
                        start = False
                        a, b = None, None
                        for chunk in line:
                            if chunk == "];":
                                start = False

                            if start:
                                if chunk[0] == "[":
                                    a = chunk[1:]
                                elif chunk[1] == "]":
                                    b = chunk[:-1]
                                if a is not None and b is not None:
                                    posCities.append((int(a),int(b)))
                                    a, b = None, None
                                
                            if chunk == "[":
                                start = True
                    elif line[0] == "posLocations":
                        start = False
                        a, b = None, None
                        for chunk in line:
                            if chunk == "];":
                                start = False

                            if start:
                                if chunk[0] == "[":
                                    a = chunk[1:]
                                elif chunk[1] == "]":
                                    b = chunk[:-1]
                                if a is not None and b is not None:
                                    posLocations.append((int(a),int(b)))
                                    name2location[(int(a), int(b))]=Location((int(a),int(b)))
                                    a, b = None, None
                                
                            if chunk == "[":
                                start = True
                    elif line[0] == "d_city":
                        start = False
                        for chunk in line:
                            if chunk[0] == "[":
                                start = True
                            if start:
                                if chunk[0] == "[":
                                    if len(chunk) > 1:
                                        d_city_input.append(int(chunk[1:]))
                                elif chunk[-1] == ";":
                                    d_city_input.append(int(chunk[:-2]))
                                else:
                                    d_city_input.append(int(chunk))
                    elif line[0] == "cap":
                        start = False
                        for chunk in line:
                            if chunk[0] == "[":
                                start = True
                            if start:
                                if chunk[0] == "[":
                                    if len(chunk) > 1:
                                        cap_input.append(int(chunk[1:]))
                                elif chunk[-1] == ";":
                                    cap_input.append(int(chunk[:-2]))
                                else:
                                    cap_input.append(int(chunk))
                            

                    elif line[0] == "cost":
                        start = False
                        for chunk in line:
                            if chunk[0] == "[":
                                start = True
                            if start:
                                if chunk[0] == "[":
                                    if len(chunk) > 1:
                                        cost_input.append(int(chunk[1:]))
                                elif chunk[-1] == ";":
                                    cost_input.append(int(chunk[:-2]))
                                else:
                                    cost_input.append(int(chunk))
                    elif line[0] == "d_center":
                        d_center = float(line[2][:-1])

    ind_cities = 0
    for c in posCities:
        name2city[c] = City(p[ind_cities], c)
        ind_cities += 1

    for t in range(nTypes):
        name2type[t] = Type(cap_input[t], d_city_input[t], cost_input[t])

    return (d_center, name2location, name2city, name2type)

def distance(a, b):
    '''
    Euclidean distance between two points ->  a = (a_x, a_y) | b = (b_x, b_y)
    '''
    return np.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )

