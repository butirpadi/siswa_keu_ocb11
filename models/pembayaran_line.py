# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class pembayaran_line(models.Model):
    _name = 'siswa_keu_ocb11.pembayaran_line'
    
    pembayaran_id = fields.Many2one('siswa_keu_ocb11.pembayaran',string='Pembayaran', required=True, ondelete="cascade")
    siswa_id = fields.Many2one('res.partner', related='pembayaran_id.siswa_id')
    biaya_id = fields.Many2one('siswa_keu_ocb11.siswa_biaya', string='Biaya', required=True, domain=[('siswa_id','=',lambda self: self.siswa_id.id)] )
    harga = fields.Float('Harga', related='biaya_id.harga')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', related='biaya_id.tahunajaran_id')
    bayar = fields.Float('Bayar')

    # @api.onchange('siswa_id')
    # def _compute_biaya(self):
    #     print('inside compute biaya')

    