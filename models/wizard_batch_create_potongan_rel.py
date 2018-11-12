from flectra import models, fields, api, _

class wizard_batch_create_potongan_rel(models.Model):
    _name = 'siswa_wizard_batch_create_potongan_rel'

    wizard_id = fields.Many2one('siswa_wizard_batch_create_potongan', string="Wizard", ondelete="cascade")
    siswa_id = fields.Many2one('res.partner', string="Siswa", required=True, ondelete="cascade")
    siswa_biaya_id = fields.Many2one('siswa_keu_ocb11.siswa_biaya', required=True, ondelete="cascade")
    related_siswa_id = fields.Many2one('res.partner', string="Siswa", related='siswa_biaya_id.siswa_id', store=True)
    related_biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string="Biaya", related='siswa_biaya_id.biaya_id', store=True)
    related_tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", related="siswa_biaya_id.tahunajaran_id", store=True)
    related_harga = fields.Float('Harga', related="siswa_biaya_id.harga", store=True)
    related_amount_due = fields.Float('Amount Due', related="siswa_biaya_id.amount_due", store=True)
    related_bulan = fields.Selection([(0, '-'), 
                            (1, 'Januari'),
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
                            ], string='Bulan', related="siswa_biaya_id.bulan")
    jumlah_potongan = fields.Float('Jumlah Potongan', default=0.0, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ], string='Status', default='draft')
                     