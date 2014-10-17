#!/usr/bin/env /usr/bin/python

# Copyright 2014 Ron Economos (w6rz@comcast.net)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from gnuradio import gr, atsc, blocks, analog, digital
from grc_gnuradio import blks2 as grc_blks2
import sys, os
import atscmap, osmosdr

def main(args):
    nargs = len(args)
    if nargs == 1:
        infile = args[0]
        outfile = None
    elif nargs == 2:
        infile = args[0]
        outfile = args[1]
    else:
        sys.stderr.write("Usage: atsc-blade-fpga.py input_file [output_file]\n");
        sys.exit(1)

    symbol_rate = (4500000.0 / 286 * 684) * 3
    center_freq = 429000000
    txvga1_gain = -6
    txvga2_gain = 20

    tb = gr.top_block()

    src = blocks.file_source(gr.sizeof_char, infile, True)

    pad = atsc.pad()
    rand = atsc.randomizer()
    rs_enc = atsc.rs_encoder()
    inter = atsc.interleaver()
    trell = atsc.trellis_encoder()
    fsm = atsc.field_sync_mux()

    v2s = blocks.vector_to_stream(gr.sizeof_char, 1024)
    minn = blocks.keep_m_in_n(gr.sizeof_char, 832, 1024, 4)
    symmap = atscmap.atscmap_bc()

    out = osmosdr.sink(args="bladerf=0")
    out.set_sample_rate(symbol_rate)
    out.set_center_freq(center_freq, 0)
    out.set_freq_corr(0, 0)
    out.set_gain(txvga2_gain, 0)
    out.set_bb_gain(txvga1_gain, 0)
    out.set_bandwidth(6000000, 0)

    tb.connect(src, pad, rand, rs_enc, inter, trell, fsm, v2s, minn, symmap)
    tb.connect(symmap, out)

    if outfile:
        dst = blocks.file_sink(gr.sizeof_gr_complex, outfile)
        tb.connect(symmap, dst)

    tb.run()


if __name__ == '__main__':
    main(sys.argv[1:])
