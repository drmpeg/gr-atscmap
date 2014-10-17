/* -*- c++ -*- */

#define ATSCMAP_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "atscmap_swig_doc.i"

%{
#include "atscmap/atscmap_bc.h"
%}


%include "atscmap/atscmap_bc.h"
GR_SWIG_BLOCK_MAGIC2(atscmap, atscmap_bc);
