import numpy as np
import pypolydim


a = pypolydim.gedim.StringsUtilities.parse_float("6")
print(a)

b = pypolydim.gedim.GeometryUtilitiesConfig()
c = pypolydim.gedim.GeometryUtilities(b)

origin = np.matrix([[1.0], [2.0], [3.0]], dtype=np.float64)
print(origin)

mat = c.create_ellipse(2.0, 2.0, 3)


print(mat)

