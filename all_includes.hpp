#include <vector>
#include <set>
#include <iostream>

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

// GeDiM - Geometry
#include "./PolyDiM/gedim/GeDiM/src/Geometry/GeometryUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Geometry/MapHexahedron.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Geometry/MapParallelepiped.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Geometry/MapParallelogram.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Geometry/MapQuadrilateral.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Geometry/MapTetrahedron.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Geometry/MapTriangle.hpp"

// GeDiM - IO
// #include "./PolyDiM/gedim/GeDiM/src/IO/IOUtilities.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/IO/StringsUtilities.hpp"
// #include "./PolyDiM/gedim/GeDiM/src/IO/TimeUtilities.hpp"

// GeDiM - Mesh
#include "./PolyDiM/gedim/GeDiM/src/Mesh/ConformerMeshPolygon.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/ConformerMeshSegment.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/ConformerMeshUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/IMeshDAO.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/IntersectorMesh2DSegment.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/IntersectorMesh3DSegment.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/MeshDAOExporterToCsv.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/MeshDAOImporterFromCsv.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/MeshFromCsvUtilties.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/MeshMatrices.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/MeshMatricesDAO.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/MeshUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/ObjectFileFormatInterface.hpp"
#include "./PolyDiM/gedim/GeDiM/src/Mesh/OpenVolumeMeshInterface.hpp"