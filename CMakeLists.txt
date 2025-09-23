cmake_minimum_required(VERSION 3.4)
project(polypython)

# Find required packages
find_package(pybind11 REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(Eigen3 REQUIRED)

# Create a static library with the C++ sources (excluding main)
add_subdirectory(PolyDiM)

## Configura Gedim_Macro.hpp
set(GEDIM_LIBRARY_ADDITIONAL_INCLUDE_PATH ${CMAKE_CURRENT_BINARY_DIR}/GeDiM_additional_include)
set(header "PolyDiM/gedim/GeDiM/src/Common/Gedim_Macro.in")

get_filename_component(headerDirectory ${header} DIRECTORY)
get_filename_component(headerFileName ${header} NAME_WE)
get_filename_component(headerExtension ${header} EXT)

set(headerExtension ".hpp")
set(headerDirectory ${GEDIM_LIBRARY_ADDITIONAL_INCLUDE_PATH})
configure_file(${header} ${headerDirectory}/${headerFileName}${headerExtension} @ONLY)



# Define our library with all sources from PolyDiM
file(GLOB_RECURSE POLYDIM_SOURCES 
     "PolyDiM/PolyDiM/src/*.cpp"
)

add_library(polypy_lib STATIC ${POLYDIM_SOURCES})
target_include_directories(polypy_lib PUBLIC 
    ${GEDIM_LIBRARY_ADDITIONAL_INCLUDE_PATH}
    ${EIGEN3_INCLUDE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/AgglomeratedConcaveMesh
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/AgglomeratedConcaveMesh/M1
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/AgglomeratedConcaveMesh/M2
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/AgglomeratedConcaveMesh/M3
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CircleTriangularMesh
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CircleTriangularMesh/CircleTriangularMesh_R1
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CircleTriangularMesh/CircleTriangularMesh_R2
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CircleTriangularMesh/CircleTriangularMesh_R3
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CircleTriangularMesh/CircleTriangularMesh_R4
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/ConvexConcave
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/ConvexConcave/ConvexConcave_16x16
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/ConvexConcave/ConvexConcave_32x32
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/ConvexConcave/ConvexConcave_4x4
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/ConvexConcave/ConvexConcave_8x8
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CooksMembrane
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CooksMembrane/cooks_voro_2
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CooksMembrane/cooks_voro_4
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/CooksMembrane/cooks_voro_5
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/DarcyStokesMesh
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/DarcyStokesMesh/Square_0_01
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/DarcyStokesMesh/Square_1_32
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/DarcyStokesMesh/Square_1_8
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/DarcyStokesMesh/TriMesh_0_001
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/DarcyStokesMesh/TriMesh_0_01
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/DarcyStokesMesh/TriMesh_0_025
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/2D/GenericPolyMesh
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/3D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/3D/Conformed
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/3D/Hexaedron_1e_01
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/3D/Hexaedron_1e_02
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/3D/Hexaedron_1e_03
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/Mesh/3D/Tetra200
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Brinkman_DF_PCC_2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Brinkman_DF_PCC_2D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elastic_PCC_2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elastic_PCC_2D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_MCC_2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_MCC_2D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_MCC_3D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_MCC_3D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_PCC_1D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_PCC_1D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_PCC_2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_PCC_2D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_PCC_3D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Elliptic_PCC_3D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/NavierStokes_DF_PCC_2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/NavierStokes_DF_PCC_2D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Stokes_DF_PCC_3D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/examples/Stokes_DF_PCC_3D/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/Common
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/FEM
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/FEM/PCC
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/FEM/PCC/1D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/FEM/PCC/2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/FEM/PCC/3D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/Interpolation
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/PDETools
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/PDETools/Assembler
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/PDETools/DOFs
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/PDETools/Equations
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/PDETools/Mesh
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/DF_PCC
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/DF_PCC/2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/DF_PCC/3D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/MCC
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/MCC/2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/MCC/3D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/PCC
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/PCC/2D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/PCC/3D
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/Quadrature
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/src/VEM/Utilities
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test/FEM
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test/FEM/PCC
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test/PDETools
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test/PDETools/DOFs
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test/VEM
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test/VEM/DF_PCC
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test/VEM/MCC
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/PolyDiM/test/VEM/PCC
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/3rd_party_libraries
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/3rd_party_libraries/cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/src
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/src/Algebra
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/src/Common
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/src/Geometry
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/src/IO
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/src/Mesh
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/src/MpiTools
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/src/Quadrature
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/test
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/test/Algebra
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/test/Geometry
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/test/IO
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/test/Mesh
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/test/MpiTools
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/test/Quadrature
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/GeDiM/test/cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/PolyDiM/gedim/cmake
)

# Create the pybind11 module
pybind11_add_module(polypy bindings.cpp)

# Link the library to the pybind11 module
target_link_libraries(polypy_lib PRIVATE PolyDiM::PolyDiM GeDiM::GeDiM)
target_link_libraries(polypy PRIVATE polypy_lib)

# Set properties for the module
target_compile_definitions(polypy PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

# Ensure C++17 standard is used
set_target_properties(polypy PROPERTIES 
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
)

set_target_properties(polypy_lib PROPERTIES 
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
)

# Set the output directory to the parent directory for easier Python import
set_target_properties(polypy PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/..
)

