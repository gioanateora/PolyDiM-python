#ifndef __GEDIM_MACRO_H
#define __GEDIM_MACRO_H

/// Enable Triangle
/// - 0 false
/// - 1 true
#define ENABLE_TRIANGLE 0

/// Enable Tetgen
/// - 0 false
/// - 1 true
#define ENABLE_TETGEN 0

/// Enable VTK
/// - 0 false
/// - 1 true
#define ENABLE_VTK 0

/// Enable MKL
/// - 0 false
/// - 1 true
#define ENABLE_MKL 0

/// Enable Metis
/// - 0 false
/// - 1 true
#define ENABLE_METIS 0

/// Enable VORO++
/// - 0 false
/// - 1 true
#define ENABLE_VORO 0

/// Enable SUITESPARSE
/// - 0 false
/// - 1 true
#define ENABLE_SUITESPARSE 0

/// Enable PETSc
/// - 0 false
/// - 1 true
#define ENABLE_PETSC 0

/// Adapt for PYBIND11
/// - 0 false
/// - 1 true
#define PYBIND 0

/// Use MPI
/// - 0 false
/// - 1 true
#define USE_MPI 0

/// Verbose Levels
/// - 0 None
/// - 1 Error
/// - 2 Warning
/// - 3 Info
/// - 4 Debug
/* #undef VERBOSE */

/// Logging Levels
/// - 0 None
/// - 1 Only Console
/// - 2 Only Files
/// - 3 Console and Files
/* #undef LOGGING */

// the configured options and settings for Tutorial
#define GEDIM_VERSION_MAJOR 
#define GEDIM_VERSION_MINOR 

/// @name Code Simplifications
///@{
#ifndef MIN
#define MIN(a,b) (a < b) ? a : b
#endif

#ifndef MAX
#define MAX(a,b) (a > b) ? a : b
#endif

///@}

#endif
