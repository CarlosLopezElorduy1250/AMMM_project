# Algorithmic Methods for Mathematical Models 
## COURSE PROJECT

An Internet retail company wants to build several logistic centers in order to operate in a new country. Its goal is to spend the minimum amount of money, but making sure that customers receive their products quickly enough.

The company has a set of locations L where logistic centers could be installed, and a set of cities C that need to be served. For each location l ∈ L we know its coordinates (lx,ly), and for every city c ∈ C we know its coordinates (cx,cy) and its population pc. We have available a set T of logistic center types. Each type t ∈ T represents a logistic center with capacity capt, working distance d cityt, and installation cost cost_t.

Each city must be served by exactly one primary and one secondary center, which of course must be different. Logistic centers should be placed so that the distance1 between any two of them is at least d center. The capacity of a center of type t requires that the sum of the populations of the cities it serves as a primary center plus 10% the sum of the populations of the cities it serves as a secondary center cannot exceed capt. With respect to its working distance, a center of type t cannot be the primary center of any city at distance more than d cityt, or the secondary center of any city at distance more than 3 ∗ d cityt.

The goal of this project is to decide where to install the logistic centers, determine of which type each center should be and to which primary and secondary center each city should be connected to in order to minimize the total installation cost.

## Installation

### Cloning the repository

Traverse to the desired directory/folder on your file system, then clone/get the 
repository and move into the respective directory with:

```bash
git clone https://github.com/CarlosLopezElorduy1250/AMMM_project.git
cd AMMM_project
```

### Installing Conda and dependencies

Dependencies can be conveniently installed with the [Conda][conda]
package manager. We recommend that you install
[Miniconda][miniconda-installation] for your system. Be sure to select
Python 3 option. The workflow was built and tested with `conda 4.8.5`.

After installing conda or miniconda, install the remaining dependencies with:

```bash
conda env create -f environment.yml
```
### Activate environment

Activate the Conda environment with:

```bash
conda activate ammm
```

## Running the workflow

1. Populate the `INPUT/config.yml` file with required parameters.

2. Assuming that your current directory is the repository's root directory, start your workflow run:
```bash
./main_solver.py
```




[conda]: <https://docs.conda.io/projects/conda/en/latest/index.html>
[miniconda-installation]: <https://docs.conda.io/en/latest/miniconda.html>


