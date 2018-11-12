# -*- coding: utf-8 -*-

from flectra import models, fields, api, _

class action_confirm(models.Model):
    _name = 'siswa_keu_ocb11.action_confirm'

    pembayaran_id = fields.Many2one('siswa_keu_ocb11.pembayaran', string='Pembayaran', ondelete='restrict')
    kas_id = fields.Many2one('siswa_keu_ocb11.kas', 'Kas', ondelete='restrict')
     