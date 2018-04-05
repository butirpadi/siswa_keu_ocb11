# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class biaya_ta_jenjang(models.Model):
    _name = 'siswa_keu_ocb11.biaya_ta_jenjang'

    tahunajaran_jenjang_id = fields.Many2one('siswa_ocb11.tahunajaran_jenjang', string='Tahun Ajaran', required=True, ondelete='cascade')
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya', required=True)
    harga = fields.Float('Harga', required=True)