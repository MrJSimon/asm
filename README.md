# viscoprony
**viscoprony** is a Python package for viscoelastic material modeling. It generates Prony-series coefficients from dynamic mechanical analysis (DMA) data to describe time-dependent behavior of polymers and other viscoelastic materials.

# Purpose
This tool streamlines the process of polymer and material characterization for FEA implementations (e.g., ABAQUS, ANSYS)

1. Building master curves using Time-Temperature Superposition (TTS)
2. Fitting Prony-series parameters (relaxation moduli and times) from DMA data
3. Visualizing shift factors, storage/loss moduli, and fitted curves

# Installation
Install **viscoprony** by cloning the repository onto your local machine using the following command

    git clone https://github.com/yourusername/viscoprony.git

**Dependencies**

Required Python packages are listed in `requirements.txt`. Install them with:  

    pip install -r requirements.txt

# Getting started
This package is intended to be run through a Python IDE (PyCharm, VSCode, Spyder, etc.).  

**Data Placement**

Place your DMA data file (e.g., yourfile.txt) in the Data/ folder of the repository.

**Data file and structure**

The data file must be comma-separated and contain the following columns:

| Frequency [Hz] | Storage [MPa] | Loss [MPa] | Temperature [°C] |
|---------------:|--------------:|-----------:|------------------|
| 0.100          | 2257.56        | 123.72     | -40          |
| 0.126          | 2279.13        | 130.06     | -40          |
| 0.158          | 2297.55        | 133.45     | -40          |
| ⋮              | ⋮              | ⋮          |               |
| 0.100          | 1683.27        | 154.40     | -30          |
| 0.126          | 1679.55        | 149.65     | -30          |
| 0.158          | 1689.89        | 147.20     | -30          |
| ⋮              | ⋮              | ⋮          |               |
| 0.100          | 985.37         | 144.47     | -20          |
| 0.126          | 999.41         | 143.66     | -20          |
| 0.158          | 1018.68        | 143.01     | -20          |
| ⋮              | ⋮              | ⋮          |               |

**Example Workflow in `__main__.py`**

You can edit parameters directly in the main script.  

```python
## Load in packages
import numpy as np
from PythonFunctions.Mastercurves.mastercurve import mastercurve_tanh
from PythonFunctions.PronySeries.prony_series import prony_1
from PythonFunctions.PlottingFunctions.plotting_functions import plot_storageloss_curves
from PythonFunctions.PlottingFunctions.plotting_functions import plot_mastercurve
from PythonFunctions.PlottingFunctions.plotting_functions import plot_pronyseries
from PythonFunctions.PlottingFunctions.plotting_functions import plot_shiftfactorsVStemperatures
from PythonFunctions.OutputFunctions.output_functions import numpysavetxt

## Load in values
values = np.loadtxt('Data/<yourfile>.txt', delimiter=',')

## Set X, Y1, Y2, Z
X  = values[:, 0] # Frequencies [rad/s] (converted from Hz later)
Ys = values[:, 1] # Storage modulus [MPa]
Yl = values[:, 2] # Loss modulus [MPa]
Z  = values[:, 3] # Temperature [°C] 

## Set temperature threshold values
T1, T2 = -30, 20  # Temperatures between -30°C and 20°C

## Set frequency threshold values
f1, f2 = 10**(-24), 10**24  # Frequencies between 10⁻²⁴ and 10²⁴ [1/s]
```

# Visualizations

**Storage and Loss Moduli**: Raw DMA curves showing $E'$ (storage modulus) and $E''$  (loss modulus).
<p align="center">
  <img src="./docs/images/StorageLossCurves.png" alt="Storage and loss moduli curves from DMA data" width="70%">
</p>

**Shift Factors vs Temperature**: Logarithmic shift factors $a_T$ calculated from DMA data. 
<p align="center">
  <img src="./docs/images/ShiftfactorVsTemperatures.png" alt="Shift Factors" width="70%">
</p>

**Master Curve**: Constructed master curve showing the material’s behavior over a wide frequency range.
<p align="center">
  <img src="./docs/images/MasterCurve.png" alt="Master curve of viscoelastic material" width="70%">
</p>

**Prony-Series Fit**: Fitted Prony-series overlaying the master curve for validation.
<p align="center">
  <img src="./docs/images/PronyseriesFit.png" alt="Prony-series fit on master curve" width="70%">
</p>

# Output Files

| File Name                               | Description                                |
|-----------------------------------------|--------------------------------------------|
| PronySeriesCoefficientsDMTA.txt         | Fitted Prony-series parameters            |
| ShiftFactorsDMTA.txt                    | Temperature shift factors (a_T)           |
| ShiftedDataDMTA.txt                     | Shifted DMA data for master curve         |
| StorageLossCurves.png                   | Plot of raw storage and loss moduli       |
| MasterCurve.png                         | Constructed master curve                  |
| ShiftfactorVsTemperatures.png           | Shift factors vs. temperatures plot       |
| PronyseriesFit.png                      | Fitted Prony-series over master curve     |


# Documentation
For more details, visit the [Wiki](https://github.com/MrJSimon/viscoprony/wiki).
