## About ##
This library was coded to reduce the amount of manual computation work (and mistakes made) when performing calculations for Physics labs. Namely, this library is all about handling the calculation of "uncertainties" (or "standard errors" for Biologists/everyone else) when calculating the result to data collected during a lab session.

There are two main types provided here:
**1. A numerical type which represents a tuple of (value +/- uncertainty) + units, which can participate in standard algebraic operations
  1. A unit type (used for 1) providing information for unit conversions**

The numeric type allows the uncertainty associated with a value to be propagated and automatically calculated through the process of evaluating more complicated expressions. Meanwhile, unit conversions can also take place, whilst preserving the integrity of the data too.

## Usage ##
Firstly, import the library...
```
from phystools import *
P = PhysNum # get shorthand ref for the class
```

Get instances of the units to use...
```
mmDim= MillimetreLengthUnit();
mDim= MetreLengthUnit();

gDim= GramMassUnit();
kgDim= KilogramMassUnit();

sDim= SecondTimeUnit()
```

Define some data (note the use of the 'P' shorthand defined earlier)...
```
exp_data = [\
  [P(612, 1, mmDim), 	P(67.72, 0.05, sDim), P(67.62, 0.05, sDim), P(67.80, 0.05, sDim)],
  [P(481, 1, mmDim), 	P(60.28, 0.05, sDim), P(60.21, 0.05, sDim), P(60.28, 0.05, sDim)],
  # etc.
]
```

Perform calculations on the data as if they were regular numbers, except that we can retrieve the data at any point