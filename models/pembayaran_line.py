# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra.addons import decimal_precision as dp

class pembayaran_line(models.Model):
    _name = 'siswa_keu_ocb11.pembayaran_line'
    
    pembayaran_id = fields.Many2one('siswa_keu_ocb11.pembayaran',string='Pembayaran', required=True, ondelete="cascade")
    siswa_id = fields.Many2one('res.partner', related='pembayaran_id.siswa_id')
    # biaya_id = fields.Many2one('siswa_keu_ocb11.siswa_biaya', string='Biaya', required=True)
    harga = fields.Float('Harga', related='biaya_id.harga')
    related_amount_due = fields.Float('Amount Due', related='biaya_id.amount_due')
    amount_due = fields.Float('Amount Due', compute="_compute_amount_due")
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', related='biaya_id.tahunajaran_id')
    bayar = fields.Float('Bayar')
    biaya_id = fields.Many2one('siswa_keu_ocb11.siswa_biaya', string='Biaya', required=True )
    jumlah_potongan = fields.Float('Potongan', compute="_compute_potongan")

    @api.depends('biaya_id')
    def _compute_amount_due(self):
        for rec in self:
            rec.amount_due = rec.biaya_id.amount_due

#     @api.onchange('biaya_id')
#     def biaya_id_onchange(self):
#         self.amount_due = self.biaya_id.amount_due

    # def _compute_dibayar(self):
    #     self.ensure_one()
    #     self.bayar = self.biaya_id.amount_due

    @api.onchange('pembayaran_id')
    def pembayaran_id_onchange(self):
        domain = {'biaya_id':[('siswa_id','=',self.pembayaran_id.siswa_id.id), ('state','=','open') ]}
        return {'domain':domain, 'value':{'biaya_id':[]}}
    
    @api.depends('biaya_id')
    def _compute_potongan(self):
        for rec in self:
            jml_pot = 0
            for pot in rec.biaya_id.potongan_ids:
                jml_pot += pot.jumlah_potongan
            rec.jumlah_potongan = jml_pot 