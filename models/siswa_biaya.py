# -*- coding: utf-8 -*-

from flectra import models, fields, api, _

class siswa_biaya(models.Model):
    _name = 'siswa_keu_ocb11.siswa_biaya'

    active = fields.Boolean(default=True)
    name = fields.Char(string='Nama')
    siswa_id = fields.Many2one('res.partner', string='Siswa', ondelete='cascade')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', required=True, ondelete='cascade')
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya', required=True, ondelete='restrict')
    bulan = fields.Selection([(0, 'Bulan'), 
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
                            ], string='Bulan', default=0)
    harga = fields.Float('Harga', required=True, default=0)
    amount_due = fields.Float('Amount Due', required=True, default=0)
    dibayar = fields.Float('Dibayar', required=True, default=0)
    state = fields.Selection([('open', 'Open'), ('paid', 'Paid')], string='Paid', required=True, default='open')
    active_rombel_id = fields.Many2one('siswa_ocb11.rombel', related='siswa_id.active_rombel_id', string='Rombongan Belajar')
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang')
    potongan_ids = fields.One2many('siswa.potongan_biaya',inverse_name='siswa_biaya_id')
    jumlah_potongan = fields.Float('Jumlah Potongan', compute="_compute_jumlah_potongan", store=True)
    
    @api.depends('potongan_ids')
    def _compute_jumlah_potongan(self):
        for rec in self:
            for pot in rec.potongan_ids:
                rec.jumlah_potongan += pot.jumlah_potongan

    # @api.depends('biaya_id')
    # def biaya_id_onchange(self):
    #     # get harga

    def generate_default(self):
        self.ensure_one()
        # get jenjang
        # rombel = self.siswa_id.rombels.search([('tahunajaran_id','=',self.tahunajaran_id.id)]).rombel_id
        rombel = self.env['siswa_ocb11.rombel_siswa'].search([
                ('siswa_id','=',self.siswa_id.id),
                ('tahunajaran_id','=',self.tahunajaran_id.id)
            ]).rombel_id
        self.jenjang_id = rombel.jenjang_id.id

        tahunajaran_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([
                ('tahunajaran_id', '=', self.tahunajaran_id.id),
                ('jenjang_id', '=', self.jenjang_id.id),
            ])
        biaya_ta_jenjang = tahunajaran_jenjang.biayas.search([
                ('biaya_id', '=', self.biaya_id.id),
                ('tahunajaran_jenjang_id', '=', tahunajaran_jenjang.id),
            ])

        self.harga = biaya_ta_jenjang.harga
        self.amount_due = biaya_ta_jenjang.harga

        if self.biaya_id.is_different_by_gender:
            if self.siswa_id.jenis_kelamin == 'perempuan':
                self.harga = biaya_ta_jenjang.harga_alt
                self.amount_due = biaya_ta_jenjang.harga_alt

        if self.biaya_id.is_bulanan:
            self.name = self.biaya_id.name + ' ' + dict(self._fields['bulan'].selection).get(self.bulan)
        else:
            self.name = self.biaya_id.name
            self.bulan = None
        
        # compute siswa biaya & amount
        self.siswa_id._compute_total_biaya()
    
    @api.multi
    def unlink(self):
    #     self.ensure_one()
        siswaId = 0
        for rec in self:
            siswaId = rec.siswa_id.id
    #     print('Siswa ID To Compute : ' + str(siswa_id))

        res =  super(siswa_biaya, self).unlink()

        # recompute total biaya siswa
        siswa = self.env['res.partner'].search([('id','=',siswaId)])
    
        for rec in siswa:
            rec._compute_total_biaya()

        # update dashboard keuangan
        self.recompute_dashboard_keuangan()

        return res
    
    @api.multi
    def write(self, vals):
        result = super(siswa_biaya, self).write(vals)

        # update dashboard keuangan
        self.recompute_dashboard_keuangan()

        return result
    
    @api.model
    def create(self, vals):
        result = super(siswa_biaya, self).create(vals)

        # update dashboard keuangan
        self.recompute_dashboard_keuangan()

        return result
    
    def recompute_dashboard_keuangan(self):
        dash_keuangan_id = self.env['ir.model.data'].search([('name','=','default_dashboard_pembayaran')]).res_id
        dash_keuangan = self.env['siswa_keu_ocb11.keuangan_dashboard'].search([('id','=',dash_keuangan_id)])
        for dash in dash_keuangan:
            dash.compute_keuangan()   