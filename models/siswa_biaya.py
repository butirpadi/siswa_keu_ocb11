# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class siswa_biaya(models.Model):
    _name = 'siswa_keu_ocb11.siswa_biaya'

    name = fields.Char(string='Nama')
    siswa_id = fields.Many2one('res.partner', string='Siswa', ondelete='cascade')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', required=True, ondelete='cascade')
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya', required=True, ondelete='restrict')
    bulan = fields.Selection([(1, 'Januari'), 
                            (2, 'Februari'),
                            (3, 'Maret'),
                            (4, 'April'),
                            (5, 'Mei'),
                            (6, 'Juni'),
                            (7, 'Juli'),
                            (8, 'Agustus'),
                            (9, 'September'),
                            (10, 'Oktober'),
                            (11, 'November'),
                            (12, 'Desember'),
                            ], string='Bulan', default=1)
    harga = fields.Float('Harga', required=True, default=0)
    amount_due = fields.Float('Amount Due', required=True, default=0)
    dibayar = fields.Float('Dibayar', required=True, default=0)
    state = fields.Selection([('open', 'Open'), ('paid', 'Paid')], string='Paid', required=True, default='open')
    active_rombel_id = fields.Many2one('siswa_ocb11.rombel', related='siswa_id.active_rombel_id', string='Rombongan Belajar')
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang')