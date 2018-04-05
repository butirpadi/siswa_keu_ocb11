# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint

class siswa(models.Model):
    _inherit = 'res.partner'

    biayas = fields.One2many('siswa_keu_ocb11.siswa_biaya', inverse_name='siswa_id', string='Biaya-biaya') 
    total_biaya = fields.Float('Total Biaya')
    amount_due_biaya = fields.Float('Amount Due')