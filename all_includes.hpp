#include <chrono>
#include <iostream>
#include <limits>
#include <set>
#include <sstream>
#include <string>
#include <vector>

#include "Eigen/Eigen"

// GeDiM - Algebra
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/Eigen_Array.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/Eigen_BiCGSTABSolver.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/Eigen_LUSolver.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/Eigen_PCGSolver.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/Eigen_SparseArray.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/Eigen_Utilities.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/IArray.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/ILinearSolver.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/ISparseArray.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/LAPACK_Utilities.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/Paradiso_CholeskySolver.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/Paradiso_LUSolver.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/PETSc_Array.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/PETSc_KSPSolver.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/PETSc_SparseArray.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/Algebra/SutieSparse_Utilties.hpp"

// GeDiM - IO
// #include "./PolyDiM/gedim/GeDiM/src/IO/IOUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM/src/IO/StringsUtilities.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/IO/TimeUtilities.hpp"

// GeDiM - Mesh
#include "./PolyDiM/gedim/GeDiM/src/Geometry/GeometryUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Geometry/MapHexahedron.hpp"
