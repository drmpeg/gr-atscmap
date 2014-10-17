/* -*- c++ -*- */
/* 
 * Copyright 2014 Ron Economos.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "atscmap_bc_impl.h"

namespace gr {
  namespace atscmap {

    atscmap_bc::sptr
    atscmap_bc::make()
    {
      return gnuradio::get_initial_sptr
        (new atscmap_bc_impl());
    }

    /*
     * The private constructor
     */
    atscmap_bc_impl::atscmap_bc_impl()
      : gr::block("atscmap_bc",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
        set_output_multiple(8);
    }

    /*
     * Our virtual destructor.
     */
    atscmap_bc_impl::~atscmap_bc_impl()
    {
    }

    void
    atscmap_bc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = noutput_items * 8;
    }

    int
    atscmap_bc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const unsigned char *in = (const unsigned char *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];
        short symbols;
        gr_complex mapped_symbols[1];
        const float scaling = 1.0f / 2000.0f;

        for (int i = 0; i < noutput_items; i++)  {
            symbols = 0;
            for (int j = 0; j < 4; j++)
            {
                symbols |= *in++ << (j * 4);
            }
            mapped_symbols[0].real() = (float)symbols * scaling;
            symbols = 0;
            for (int j = 0; j < 4; j++)
            {
                symbols |= *in++ << (j * 4);
            }
            mapped_symbols[0].imag() = (float)symbols * scaling;
            *out++ = mapped_symbols[0];
        }

        // Tell runtime system how many input items we consumed on
        // each input stream.
        consume_each (noutput_items * 8);

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace atscmap */
} /* namespace gr */

