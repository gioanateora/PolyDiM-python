#ifndef __GEDIM_MACRO_H
#define __GEDIM_MACRO_H

/// Enable MKL
/// - 0 false
/// - 1 true
#define ENABLE_MKL 0

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
#define VERBOSE 3

/// Logging Levels
/// - 0 None
/// - 1 Only Console
/// - 2 Only Files
/// - 3 Console and Files
#define LOGGING 3

// the configured options and settings for Tutorial
#define GEDIM_VERSION_MAJOR 1
#define GEDIM_VERSION_MINOR 0

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
