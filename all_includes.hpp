#include <fstream>
#include <limits>

// GeDiM-core - Geometry
#include "./PolyDiM/gedim/GeDiM-core/src/Geometry/GeometryUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapHexahedron.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapParallelepiped.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapParallelogram.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapQuadrilateral.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapTetrahedron.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Geometry/MapTriangle.hpp"

// GeDiM-core - IO
#include "./PolyDiM/gedim/GeDiM-core/src/IO/IOStream.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/IO/IOUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/IO/MEDIT_Utilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/IO/StringsUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/IO/UCDUtilities.hpp"

// GeDiM-core - Mesh
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/ConformerMeshPolygon.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/ConformerMeshSegment.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/ConformMeshUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/IMeshDAO.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/IntersectorMesh2DSegment.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/IntersectorMesh3DSegment.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshDAOExporterToCsv.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshDAOImporterFromCsv.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshFromCsvUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshMatrices.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshMatricesDAO.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/MeshUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/ObjectFileFormatInterface.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/OpenVolumeMeshInterface.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/PlatonicSolid.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/RefinementUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/SphereMeshUtilities.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/UnionMeshSegment.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Mesh/WavefrontOBJInterface.hpp"

// GeDiM-core MpiTools
#include "./PolyDiM/gedim/GeDiM-core/src/MpiTools/GraphUtilities.hpp"

// GeDiM-core Quadrature
#include "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss1D.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss2D_Square.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss2D_Triangle.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss3D_Hexahedron.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss3D_Tetrahedron_PositiveWeights.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_Gauss3D_Tetrahedron.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Quadrature/Quadrature_GaussLobatto1D.hpp"
#include "./PolyDiM/gedim/GeDiM-core/src/Quadrature/QuadratureData.hpp"

// 3rd_party_libraries MetisInterface
#include "./PolyDiM/gedim/3rd_party_libraries/src/MetisInterface/MetisUtilities.hpp"

// 3rd_party_libraries TetgenInterface
#include "./PolyDiM/gedim/3rd_party_libraries/src/TetgenInterface/TetgenInterface.hpp"
#include "./PolyDiM/gedim/3rd_party_libraries/src/TetgenInterface/CreateMeshWithHoles.hpp"

// 3rd_party_libraries TriangleInterface
#include "./PolyDiM/gedim/3rd_party_libraries/src/TriangleInterface/TriangleInterface.hpp"

// 3rd_party_libraries VoroInterface
#include "./PolyDiM/gedim/3rd_party_libraries/src/VoroInterface/VoroInterface.hpp"

// GeDiM-core FEM
#include "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_MCC_2D_LocalSpace_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_MCC_2D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_MCC_2D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_Triangle_RT_MCC_2D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/MCC/2D/FEM_Triangle_RT_MCC_2D_ReferenceElement.hpp"

#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/1D/FEM_PCC_1D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/1D/FEM_PCC_1D_ReferenceElement.hpp"

#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_PCC_2D_LocalSpace_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_PCC_2D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_PCC_2D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_Quadrilateral_PCC_2D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_Quadrilateral_PCC_2D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_Triangle_PCC_2D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/2D/FEM_Triangle_PCC_2D_ReferenceElement.hpp"

#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_Hexahedron_PCC_3D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_Hexahedron_PCC_3D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_PCC_3D_LocalSpace_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_PCC_3D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_PCC_3D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_Tetrahedron_PCC_3D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/FEM/PCC/3D/FEM_Tetrahedron_PCC_3D_ReferenceElement.hpp"

// GeDiM-core Interpolation
#include "./PolyDiM/PolyDiM-core/src/Interpolation/lagrange_1D.hpp"

// GeDiM-core PDETools
#include "./PolyDiM/PolyDiM-core/src/PDETools/Assembler/assembler_PCC_2D_functions_data.hpp"
#include "./PolyDiM/PolyDiM-core/src/PDETools/Assembler/assembler_PCC_2D_functions_utilities.hpp"
#include "./PolyDiM/PolyDiM-core/src/PDETools/Assembler/assembler_PCC_2D_functions.hpp"
#include "./PolyDiM/PolyDiM-core/src/PDETools/Assembler/Assembler_Utilities.hpp"

#include "./PolyDiM/PolyDiM-core/src/PDETools/DOFs/DOFsManager.hpp"

#include "./PolyDiM/PolyDiM-core/src/PDETools/Equations/EllipticEquation.hpp"

#include "./PolyDiM/PolyDiM-core/src/PDETools/LocalSpace/LocalSpace_DF_PCC_2D.hpp"
#include "./PolyDiM/PolyDiM-core/src/PDETools/LocalSpace/LocalSpace_MCC_2D.hpp"
#include "./PolyDiM/PolyDiM-core/src/PDETools/LocalSpace/LocalSpace_PCC_2D.hpp"
#include "./PolyDiM/PolyDiM-core/src/PDETools/LocalSpace/LocalSpace_PCC_3D.hpp"

#include "./PolyDiM/PolyDiM-core/src/PDETools/Mesh/MeshMatricesDAO_mesh_connectivity_data.hpp"
#include "./PolyDiM/PolyDiM-core/src/PDETools/Mesh/PDE_Mesh_Utilities.hpp"

// GeDiM-core Utilities
#include "./PolyDiM/PolyDiM-core/src/Utilities/GBasis_2D.hpp"
#include "./PolyDiM/PolyDiM-core/src/Utilities/GBasis_3D.hpp"
#include "./PolyDiM/PolyDiM-core/src/Utilities/GBasis_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/Utilities/Inertia_Utilities.hpp"
#include "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_1D.hpp"
#include "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_2D.hpp"
#include "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_3D.hpp"
#include "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/Utilities/Monomials_Utilities.hpp"

// GeDiM-core VEM
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Creator.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_LocalSpace_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Pressure_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Reduced_Pressure_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Reduced_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Reduced_Velocity_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/2D/VEM_DF_PCC_2D_Velocity_LocalSpace.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Creator.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_LocalSpace_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Pressure_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Reduced_Pressure_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Reduced_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Reduced_Velocity_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/3D/VEM_DF_PCC_3D_Velocity_LocalSpace.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/DF_PCC/VEM_DF_PCC_Utilities.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Creator.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_EdgeOrtho_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_EdgeOrtho_Velocity_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_LocalSpace_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Ortho_EdgeOrtho_Velocity_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Ortho_Velocity_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Partial_Velocity_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Pressure_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/2D/VEM_MCC_2D_Velocity_LocalSpace.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_Creator.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_LocalSpace_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_Pressure_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/3D/VEM_MCC_3D_Velocity_LocalSpace.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/MCC/VEM_MCC_Utilities.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_Creator.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_Inertia_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_Ortho_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/I_VEM_PCC_2D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/2D/VEM_PCC_2D_LocalSpace_Data.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_Creator.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_Inertia_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_Ortho_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/3D/VEM_PCC_3D_LocalSpace_Data.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/PCC/VEM_PCC_Utilities.hpp"

#include "./PolyDiM/PolyDiM-core/src/VEM/Quadrature/VEM_Quadrature_2D.hpp"
#include "./PolyDiM/PolyDiM-core/src/VEM/Quadrature/VEM_Quadrature_3D.hpp"

// GeDiM-core Z-FEM
#include "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_Creator.hpp"
#include "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_ReferenceElement.hpp"
#include "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_LocalSpace_Data.hpp"
#include "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_LocalSpace.hpp"
#include "./PolyDiM/PolyDiM-core/src/ZFEM/PCC/2D/ZFEM_PCC_2D_LocalSpace.cpp"

