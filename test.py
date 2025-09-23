import polydim
import numpy as np

a = polydim.gedim.StringsUtilities.parse_float("6")
print(a)

b = polydim.gedim.GeometryUtilitiesConfig()
c = polydim.gedim.GeometryUtilities(b)

origin = np.matrix([[1.0], [2.0], [3.0]], dtype=np.float64)
print(origin)

mat = c.create_ellipse(2.0, 2.0, 3)


print(mat)