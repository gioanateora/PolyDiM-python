cmake_minimum_required(VERSION 3.28)
project(pypolydim LANGUAGES CXX C)

set(USE_MPI OFF CACHE BOOL "Enable MPI support")
set(ENABLE_TRIANGLE OFF CACHE BOOL "Enable Triangle extension")
set(ENABLE_TETGEN OFF CACHE BOOL "Enable Tetgen extension")
set(ENABLE_METIS OFF CACHE BOOL "Enable Metis extension")
set(ENABLE_VTK OFF CACHE BOOL "Enable VTK extension")
set(ENABLE_MKL OFF CACHE BOOL "Enable MKL extension")
set(ENABLE_VORO OFF CACHE BOOL "Enable VORO extension")
set(ENABLE_SUITESPARSE OFF CACHE BOOL "Enable SuiteSparse extension")
set(ENABLE_PETSC OFF CACHE BOOL "Enable PETSc extension")


# Add dependencies
###########################################################################################

## PyBind11
# Use Python from venv if one is active
if(DEFINED ENV{VIRTUAL_ENV})
    set(Python3_EXECUTABLE $ENV{VIRTUAL_ENV}/bin/python)
    message(STATUS "Using Python from: $ENV{VIRTUAL_ENV}")
endif()

# Find required packages
find_package(Python3 3.12 REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 REQUIRED)

add_compile_definitions(PYBIND11_DETAILED_ERROR_MESSAGES)

## Eigen3
find_package(Eigen3 CONFIG REQUIRED)
list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES PUBLIC Eigen3::Eigen)

## Blas
find_package(BLAS REQUIRED)
list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES PUBLIC BLAS::BLAS)

## Lapack
find_package(LAPACK REQUIRED)
list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES PUBLIC LAPACK::LAPACK)

## MPI
if(${USE_MPI})
    find_package(MPI REQUIRED)
    list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES PUBLIC MPI::MPI_CXX)
endif()

## MKL
if(${ENABLE_MKL})
    set(MKL_INTERFACE lp64) # Eigen requires lp64 interface
    find_package(MKL CONFIG REQUIRED)
    list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES MKL::MKL)
endif()

## triangle
if(${ENABLE_TRIANGLE})
    find_package(triangle CONFIG REQUIRED)
    list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES PUBLIC triangle::triangle)
endif()

## tetgen
if(${ENABLE_TETGEN})
    find_package(tetgen CONFIG REQUIRED)
    list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES PUBLIC tetgen::tetgen)
endif()

## VORO
if(${ENABLE_VORO})
    find_package(VORO CONFIG REQUIRED)
    list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES PUBLIC VORO::voro++)
endif()

## VTK
if(${ENABLE_VTK})
    find_package(VTK CONFIG REQUIRED)
    list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES PUBLIC ${VTK_LIBRARIES})
endif()

## METIS
if(${ENABLE_METIS})
    find_package(metis CONFIG REQUIRED)
    list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES METIS::metis)
endif()

## SuiteSparse
if(${ENABLE_SUITESPARSE})
    find_package(SuiteSparse CONFIG REQUIRED)
    message("Found SuiteSparse: ${SUITESPARSE_LIBRARIES}")
    list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES ${SUITESPARSE_LIBRARIES})
    list(APPEND GEDIM_LIBRARY_INCLUDE ${SUITESPARSE_INCLUDE_DIRS})
endif()

if(${ENABLE_PETSC})
    # PkgConfig
    find_package(PkgConfig)

    # PETSc
    if (PKG_CONFIG_FOUND)
        pkg_check_modules(PETSC PETSc)
    endif()

    if (PETSC_FOUND)
        message("Found PETSc: ${PETSC_LINK_LIBRARIES}")
        list(APPEND COMPILE_OPTIONS ${PETSC_CFLAGS})
        list(APPEND GEDIM_LIBRARY_INCLUDE ${PETSC_INCLUDE_DIRS})
        list(APPEND PYPOLYDIM_LIBRARY_LINKED_LIBRARIES ${PETSC_LINK_LIBRARIES})
        set(LINK_FLAGS "${LINK_FLAGS} ${PETSC_LDFLAGS}")
        set(CMAKE_REQUIRED_FLAGS ${PETSC_CFLAGS})
        set(CMAKE_REQUIRED_INCLUDES "${PETSC_INCLUDE_DIRS}")
    endif()
endif()

# Insert Sources
#############################################################################################
add_subdirectory(PolyDiM/PolyDiM/src)

list(APPEND pypolydim_sources ${polydim_src_sources})
list(APPEND pypolydim_headers ${polydim_src_headers})
list(APPEND pypolydim_includes ${polydim_src_includes})


add_subdirectory(PolyDiM/gedim/GeDiM/src)

list(APPEND pypolydim_sources ${gedim_src_sources})
list(APPEND pypolydim_headers ${gedim_src_headers})
list(APPEND pypolydim_includes ${gedim_src_includes})

# Create public headers
###############################################################################################
set(GEDIM_LIBRARY_ADDITIONAL_INCLUDE_PATH ${CMAKE_CURRENT_BINARY_DIR}/GeDiM_additional_include)

foreach(header ${pypolydim_headers})
    get_filename_component(headerDirectory ${header} DIRECTORY)
    get_filename_component(headerFileName ${header} NAME_WE)
    get_filename_component(headerExtension ${header} EXT)

    if(${headerExtension} MATCHES ".in")
        set(headerExtension ".hpp")
        set(headerDirectory ${GEDIM_LIBRARY_ADDITIONAL_INCLUDE_PATH})

        configure_file(${header} ${headerDirectory}/${headerFileName}${headerExtension} @ONLY)
    elseif(NOT ${headerExtension} MATCHES ".hpp" AND NOT ${headerExtension} MATCHES ".h")
        message(SEND_ERROR "Header extension not recognized for file ${headerFileName}${headerExtension}")
    endif()

    list(APPEND pypolydim_headers ${headerDirectory}/${headerFileName}${headerExtension})
endforeach()

list(APPEND pypolydim_includes ${GEDIM_LIBRARY_ADDITIONAL_INCLUDE_PATH})

############################################################################################
# Create a static library with the C++ sources (excluding main)

add_library(polydim_lib STATIC ${pypolydim_sources} ${pypolydim_headers})
target_include_directories(polydim_lib PUBLIC  ${pypolydim_includes}) #  rimosso ${CMAKE_CURRENT_SOURCE_DIR}

set_target_properties(polydim_lib PROPERTIES
    LINKER_LANGUAGE CXX
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

target_compile_options(polydim_lib PUBLIC -fPIC -w)

# Create the pybind11 module
pybind11_add_module(pypolydim bindings.cpp)

# Link the library to the pybind11 module
target_link_libraries(polydim_lib ${PYPOLYDIM_LIBRARY_LINKED_LIBRARIES})
target_link_libraries(pypolydim PRIVATE polydim_lib ${PYPOLYDIM_LIBRARY_LINKED_LIBRARIES})
target_include_directories(pypolydim PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${pypolydim_includes})

# Set properties for the module
target_compile_definitions(pypolydim PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

# Set the output directory to the parent directory for easier Python import
set_target_properties(pypolydim PROPERTIES
    LINKER_LANGUAGE CXX
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)


install(TARGETS pypolydim DESTINATION pypolydim)
install(FILES __init__.py DESTINATION pypolydim)
install(FILES pypolydim.pyi DESTINATION pypolydim)
install(FILES assembler_utilities.py DESTINATION pypolydim)
install(FILES vtk_utilities.py DESTINATION pypolydim)
install(FILES export_vtk_utilities.py DESTINATION pypolydim)



