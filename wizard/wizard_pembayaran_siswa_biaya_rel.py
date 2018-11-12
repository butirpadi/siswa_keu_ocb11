from flectra import models, fields, api, _
from pprint import pprint

class wizard_pembayaran_siswa_biaya_rel(models.TransientModel):
    _name = 'siswa_keu_ocb11.wizard_pembayaran_siswa_biaya_rel'

    siswa_id = fields.Many2one('res.partner', string='Siswa')
    induk = fields.Char('No. Induk', related='siswa_id.induk')
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya')
    is_bulanan = fields.Boolean('Is Bulanan', related='biaya_id.is_bulanan')
    wizard_id = fields.Many2one('siswa_keu_ocb11.wizard_report_pembayaran_siswa', string='Wizard')
    rombel_id = fields.Many2one('siswa_ocb11.rombel', string="Rombongan Belajar")

    jan = fields.Float('Jan')
    feb = fields.Float('Feb')
    mar = fields.Float('Mar')
    apr = fields.Float('Apr')
    mei = fields.Float('Mei')
    jun = fields.Float('Jun')
    jul = fields.Float('Jul')
    aug = fields.Float('Aug')
    sep = fields.Float('Sep')
    oct = fields.Float('Oct')
    nov = fields.Float('Nov')
    dec = fields.Float('Dec')

    is_jan = fields.Boolean('Jan')
    is_feb = fields.Boolean('Feb')
    is_mar = fields.Boolean('Mar')
    is_apr = fields.Boolean('Apr')
    is_mei = fields.Boolean('Mei')
    is_jun = fields.Boolean('Jun')
    is_jul = fields.Boolean('Jul')
    is_aug = fields.Boolean('Aug')
    is_sep = fields.Boolean('Sep')
    is_oct = fields.Boolean('Oct')
    is_nov = fields.Boolean('Nov')
    is_dec = fields.Boolean('Dec')

    harga = fields.Float('Total Tagihan')
    total_bayar = fields.Float('Total Bayar')
    amount_due = fields.Float('Amount Due')
