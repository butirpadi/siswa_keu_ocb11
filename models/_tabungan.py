# -*- coding: utf-8 -*-

from flectra import models, fields, api, _
from pprint import pprint
from datetime import datetime, date


class tabungan(models.Model):
    _inherit = 'siswa_tab_ocb11.tabungan'

    pembayaran_siswa_id = fields.One2many('siswa_keu_oacb11.pembayaran', inverse_name="tabungan_id", string="Pembayaran Tagihan Siswa", ondelete="cascade") 