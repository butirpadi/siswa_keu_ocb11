# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class tahunajaran_jenjang(models.Model):
    _name = 'siswa_keu_ocb11.tahunajaran_jenjang'

    name = fields.Char(string='Nama')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', required=True, ondelete='cascade')
    jenjang = fields.Selection([(0, 'PG'), (1, 'TK A'), (2, 'TK B')], string='Jenjang', required=True, default=0)
    biayas = fields.One2many('siswa_keu_ocb11.biaya_ta_jenjang', inverse_name='tahunajaran_jenjang_id' , string='Biaya-biaya')

    # @api.model
    # def create(self, vals):
    #     vals['name'] = str(vals['tahunajaran_id']) + str(vals['jenjang'])

    #     result = super(tahunajaran_jenjang, self).create(vals)
    #     return result
