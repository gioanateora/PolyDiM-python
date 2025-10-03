import numpy as np
from pypolydim import gedim

b = gedim.GeometryUtilitiesConfig()
c = gedim.GeometryUtilities(b)

origin = np.matrix([[1.0], [2.0], [3.0]], dtype=np.float64)
print(origin)

mat = c.create_ellipse(2.0, 2.0, 3)


print(mat)

