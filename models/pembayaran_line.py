# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class pembayaran_line(models.Model):
    _name = 'siswa_keu_ocb11.pembayaran_line'
    
    pembayaran_id = fields.Many2one('siswa_keu_ocb11.pembayaran',string='Pembayaran', required=True, ondelete="cascade")
    siswa_id = fields.Many2one('res.partner', related='pembayaran_id.siswa_id')
    # biaya_id = fields.Many2one('siswa_keu_ocb11.siswa_biaya', string='Biaya', required=True)
    harga = fields.Float('Harga', related='biaya_id.harga')
    amount_due = fields.Float('Amount Due', related='biaya_id.amount_due')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', related='biaya_id.tahunajaran_id')
    bayar = fields.Float('Bayar')
    biaya_id = fields.Many2one('siswa_keu_ocb11.siswa_biaya', string='Biaya', required=True )

    @api.onchange('biaya_id')
    def _compute_dibayar(self):
        self.ensure_one()
        self.bayar = self.biaya_id.amount_due

    @api.onchange('pembayaran_id')
    def pembayaran_id_onchange(self):
        domain = {'biaya_id':[('siswa_id','=',self.pembayaran_id.siswa_id.id), ('state','=','open') ]}
        return {'domain':domain, 'value':{'biaya_id':[]}}
    