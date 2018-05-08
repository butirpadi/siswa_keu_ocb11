# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class tahunajaran_biaya(models.Model):
    _name = 'siswa_keu_ocb11.tahunajaran_biaya'

    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran')
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya')
    harga = fields.Float('Harga', compute='_compute_harga')

    @api.depends('biaya_id')
    def _compute_harga(self):
        for rec in self:
            rec.harga = rec.biaya_id.harga 
