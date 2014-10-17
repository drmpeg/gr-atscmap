#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Atsc Blade Fpga
# Generated: Fri Oct 17 16:14:06 2014
##################################################

from gnuradio import atsc
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import atscmap
import osmosdr
import wx

class atsc_blade_fpga(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Atsc Blade Fpga")

        ##################################################
        # Variables
        ##################################################
        self.vga2_gain = vga2_gain = 20
        self.vga1_gain = vga1_gain = -8
        self.symbol_rate = symbol_rate = (4500000.0 / 286 * 684) * 3

        ##################################################
        # Blocks
        ##################################################
        _vga2_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._vga2_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_vga2_gain_sizer,
        	value=self.vga2_gain,
        	callback=self.set_vga2_gain,
        	label="VGA2 Gain",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._vga2_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_vga2_gain_sizer,
        	value=self.vga2_gain,
        	callback=self.set_vga2_gain,
        	minimum=0,
        	maximum=25,
        	num_steps=25,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_vga2_gain_sizer)
        _vga1_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._vga1_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_vga1_gain_sizer,
        	value=self.vga1_gain,
        	callback=self.set_vga1_gain,
        	label="VGA1 Gain",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._vga1_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_vga1_gain_sizer,
        	value=self.vga1_gain,
        	callback=self.set_vga1_gain,
        	minimum=-35,
        	maximum=-4,
        	num_steps=31,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_vga1_gain_sizer)
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(symbol_rate )
        self.osmosdr_sink_0.set_center_freq(429000000, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(vga2_gain, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(vga1_gain, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(6000000, 0)
          
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_char*1, 1024)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_char, 832, 1024, 4)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "/home/re/xfer/glitchatsc.ts", True)
        self.atscmap_atscmap_bc_0 = atscmap.atscmap_bc()
        self.atsc_trellis_encoder_0 = atsc.trellis_encoder()
        self.atsc_rs_encoder_0 = atsc.rs_encoder()
        self.atsc_random_0 = atsc.randomizer()
        self.atsc_pad_0 = atsc.pad()
        self.atsc_interleaver_0 = atsc.interleaver()
        self.atsc_field_sync_mux_0 = atsc.field_sync_mux()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.atsc_pad_0, 0))
        self.connect((self.atsc_pad_0, 0), (self.atsc_random_0, 0))
        self.connect((self.atsc_random_0, 0), (self.atsc_rs_encoder_0, 0))
        self.connect((self.atsc_rs_encoder_0, 0), (self.atsc_interleaver_0, 0))
        self.connect((self.atsc_interleaver_0, 0), (self.atsc_trellis_encoder_0, 0))
        self.connect((self.atsc_trellis_encoder_0, 0), (self.atsc_field_sync_mux_0, 0))
        self.connect((self.atsc_field_sync_mux_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.blocks_keep_m_in_n_0, 0))
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.atscmap_atscmap_bc_0, 0))
        self.connect((self.atscmap_atscmap_bc_0, 0), (self.osmosdr_sink_0, 0))



    def get_vga2_gain(self):
        return self.vga2_gain

    def set_vga2_gain(self, vga2_gain):
        self.vga2_gain = vga2_gain
        self.osmosdr_sink_0.set_gain(self.vga2_gain, 0)
        self._vga2_gain_slider.set_value(self.vga2_gain)
        self._vga2_gain_text_box.set_value(self.vga2_gain)

    def get_vga1_gain(self):
        return self.vga1_gain

    def set_vga1_gain(self, vga1_gain):
        self.vga1_gain = vga1_gain
        self._vga1_gain_slider.set_value(self.vga1_gain)
        self._vga1_gain_text_box.set_value(self.vga1_gain)
        self.osmosdr_sink_0.set_bb_gain(self.vga1_gain, 0)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.osmosdr_sink_0.set_sample_rate(self.symbol_rate )

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = atsc_blade_fpga()
    tb.Start(True)
    tb.Wait()
