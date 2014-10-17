INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_ATSCMAP atscmap)

FIND_PATH(
    ATSCMAP_INCLUDE_DIRS
    NAMES atscmap/api.h
    HINTS $ENV{ATSCMAP_DIR}/include
        ${PC_ATSCMAP_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    ATSCMAP_LIBRARIES
    NAMES gnuradio-atscmap
    HINTS $ENV{ATSCMAP_DIR}/lib
        ${PC_ATSCMAP_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ATSCMAP DEFAULT_MSG ATSCMAP_LIBRARIES ATSCMAP_INCLUDE_DIRS)
MARK_AS_ADVANCED(ATSCMAP_LIBRARIES ATSCMAP_INCLUDE_DIRS)

