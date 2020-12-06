import sys
import numpy as np
from argparse import ArgumentParser, RawTextHelpFormatter

# =================
# === VARIABLES ===
# =================
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

L  = set()  # Set of possible locations where a centre could be installed
C  = set()  # Set of cities
T  = set()  # Set of possible centre types
CT = set()  # Set of all centres created    (not given by the statement)

city2centres            = {}    # Dictionary that relates each city with primary and secondary centre                       -> city2centres[City] = (primary, secondary)
centre2cities_primary   = {}    # Dictionary relating each centre with the cities where it serves as a primary centre       -> centre2cities_primary[Centre]   = [city1, city2, ...]
centre2cities_secondary = {}    # Dictionary relating each centre with the cities where it serves as a secondary centre     -> centre2cities_secondary[Centre] = [city1, city2, ...]


# =================
# === FUNCTIONS ===
# =================
def distance(a, b): # Euclidean distance between two points ->  a = (a_x, a_y) | b = (b_x, b_y)
    return np.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )


# ===============
# === CLASSES ===
# ===============
class Type:
    def __init__(self, cap, d_city, cost):
        self.cap = cap
        self.d_city = d_city
        self.cost = cost

class City:
    def __init__(self, cx, cy, pc):
        self.cx = cx
        self.cy = cy
        self.pc = pc

class Location:
    def __init__(self, lx, ly):
        self.lx = lx
        self.ly = ly

class Centre:
    def __init__(self, ctype, clocation, ccities):
        self.type = ctype           # Class Type
        self.location = clocation   # Class Location
        self.cities = ccities       # List of the cities it serves (class Cities)
    
    def canPrimary(self, city):
        return distance((city.cx, city.cy),(self.location)) <= self.type.d_city

    def canSecondary(self, city):
        return distance((city.cx, city.cy),(self.location)) <= self.type.d_city * 3

    def exceedsCapacity(self):
        global centre2cities_primary, centre2cities_secondary

        result = 0
        result += centre2cities_primary[self].pc + (centre2cities_secondary[self].pc)*0.1

        return self.type.cap >= result


# ============
# === MAIN ===
# ============
if __name__ == "__main__":
    data_path = sys.argv[1]

    with open(data_path, "r") as data:
        for line in data.readlines():
            line = line.split()
            if line!=[]:
                if line[0][:2] != '//':
                    if line[0] == "nLocations":
                        nLocations = line[2][:-1]
                    elif line[0] == "nCities":
                        nCities = line[2][:-1]
                    elif line[0] == "nTypes":
                        nTypes = line[2][:-1]
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
                                    a, b = None, None
                                
                            if chunk == "[":
                                start = True
                    elif line[0] == "d_city":
                        start = False
                        for chunk in line:
                            if len(chunk)!=1:
                                if chunk[-1]==";":
                                    d_city_input.append(int(chunk[:-2]))
                                start = False

                            if start:
                                d_city_input.append(int(chunk))
                                
                            if chunk == "[":
                                start = True
                    elif line[0] == "cap":
                        start = False
                        for chunk in line:
                            if chunk[0] == "[":
                                start = True
                            if start:
                                if chunk[0] == "[":
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
                                    cost_input.append(int(chunk[1:]))
                                elif chunk[-1] == ";":
                                    cost_input.append(int(chunk[:-2]))
                                else:
                                    cost_input.append(int(chunk))
                    elif line[0] == "d_center":
                        d_center = float(line[2][:-1])
