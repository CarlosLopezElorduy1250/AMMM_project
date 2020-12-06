 int nLocations = ...;
 int nCities = ...;
 int nTypes = ...;
		   
 range L = 1..nLocations;
 range C = 1..nCities;
 range T = 1..nTypes;

 int posCities[C][1..2] = ...;
 int posLocations[L][1..2] = ...;
 int p[C] = ...;

 float d_city[T] = ...;
 int cap [T] = ...;
 int cost [T] = ...;

 float d_center = ...;
			  
// Define your decision variables and any other auxiliary data here.
// You can run an execute block if needed.

 minimize // ... Write the objective function.

 subject to {

  // Write the constraints.
      
 }

// You can run an execute block if needed.
