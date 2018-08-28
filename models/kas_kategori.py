# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.addons import decimal_precision as dp
from datetime import datetime

class kas_kategori(models.Model):
    _name = 'siswa_keu_ocb11.kas_kategori'

    name = fields.Char(string='Nama', requred=True)
    tipe = fields.Selection([('in', 'Pendapatan'), ('out', 'Pengeluaran')], string='Tipe', required=True, default='in')
    is_biaya_account = fields.Boolean('Is Account Biaya ?', default=False)
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string="Biaya", ondelete="cascade")