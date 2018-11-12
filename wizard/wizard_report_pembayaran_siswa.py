from flectra import models, fields, api, _
from pprint import pprint

class wizard_report_pembayaran_siswa(models.TransientModel):
    _name = 'siswa_keu_ocb11.wizard_report_pembayaran_siswa'

    name = fields.Char('Name', default='0')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]), required=True, ondelete="cascade")
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya', required=True)
    rombel_id = fields.Many2one('siswa_ocb11.rombel', string='Rombongan Belajar')
    rombel_ids = fields.Many2many('siswa_ocb11.rombel',relation='wizard_pembayaran_siswa_siswa_rombel_rel', column1='report_id',column2='rombel_id', string="Rombongan Belajar")
    siswa_ids = fields.Many2many('res.partner',relation='wizard_pembayaran_siswa_siswa_rel', column1='report_id',column2='siswa_id', string="Siswa", domain=[('is_siswa','=',True)])
    pembayaran_ids = fields.Many2many('siswa_keu_ocb11.pembayaran',relation='wizard_pembayaran_siswa_pembayaran_rel', column1='report_id',column2='pembayaran_id', string="Data Pembayaran")
    pembayaran_siswa_ids = fields.One2many('siswa_keu_ocb11.wizard_pembayaran_siswa_biaya_rel', inverse_name='wizard_id')

    def action_save(self):
        self.ensure_one()
        # update name
        self.name = "Report Pembayaran Siswa"

        # arr_rombel_ids = []
        # for rb in self.rombel_ids:
        #     arr_rombel_ids.append(rb.id)

        if not self.rombel_ids:
            self.rombel_ids = self.env['siswa_ocb11.rombel'].search([])

        # get data siswa
        rombel_siswa = self.env['siswa_ocb11.rombel_siswa'].search([
            ('tahunajaran_id','=', self.tahunajaran_id.id),
            # ('rombel_id','=', self.rombel_id.id),
            ('rombel_id','in', self.rombel_ids.ids),
            ])

        if self.siswa_ids:
            rombel_siswa = self.env['siswa_ocb11.rombel_siswa'].search([
                    ('tahunajaran_id','=', self.tahunajaran_id.id),
                    ('siswa_id','in', self.siswa_ids.ids),
                    ])

        reg_pembayaran = []
        for rbs in rombel_siswa:
            siswa_biaya_ids = self.env['siswa_keu_ocb11.siswa_biaya'].search(['&','&',
                ('siswa_id','=', rbs.siswa_id.id),
                ('tahunajaran_id','=', self.tahunajaran_id.id),
                ('biaya_id','=', self.biaya_id.id),
            ])

            # test print data siswa dan biaya
            for sbi in siswa_biaya_ids:
                print(sbi.siswa_id.name + ' ------- ' + sbi.biaya_id.name )

            total_harga = sum(x.harga for x in siswa_biaya_ids)

            if self.biaya_id.is_bulanan:
                print('Iside biaya bulanan')
                # get data untuk biaya bulanan
                jan = 0.00
                feb = 0.00
                mar = 0.00
                apr = 0.00
                mei = 0.00
                jun = 0.00
                jul = 0.00
                aug = 0.00
                sep = 0.00
                oct = 0.00
                nov = 0.00
                dec = 0.00
                is_jan = False
                is_feb = False
                is_mar = False
                is_apr = False
                is_mei = False
                is_jun = False
                is_jul = False
                is_aug = False
                is_sep = False
                is_oct = False
                is_nov = False
                is_dec = False
                total_dibayar = 0.00

                for sb in siswa_biaya_ids:
                    if sb.state == 'paid':
                        total_dibayar += sb.dibayar
                        if sb.bulan == 1:
                            jan = sb.dibayar
                            is_jan = True
                        if sb.bulan == 2:
                            feb = sb.dibayar
                            is_feb = True
                        if sb.bulan == 3:
                            mar = sb.dibayar
                            is_mar = True
                        if sb.bulan == 4:
                            apr = sb.dibayar
                            is_apr = True
                        if sb.bulan == 5:
                            mei = sb.dibayar
                            is_mei = True
                        if sb.bulan == 6:
                            jun = sb.dibayar
                            is_jun = True
                        if sb.bulan == 7:
                            jul = sb.dibayar
                            is_jul = True
                        if sb.bulan == 8:
                            aug = sb.dibayar
                            is_aug = True
                        if sb.bulan == 9:
                            sep = sb.dibayar
                            is_sep = True
                        if sb.bulan == 10:
                            oct = sb.dibayar1
                            is_oct = True
                        if sb.bulan == 11:
                            nov = sb.dibayar
                            is_nov = True
                        if sb.bulan == 12:
                            dec = sb.dibayar
                            is_dec = True

                reg_pembayaran.append([0,0,{
                    'siswa_id' : rbs.siswa_id.id,
                    'rombel_id' : rbs.rombel_id.id,
                    'biaya_id' : self.biaya_id.id,
                    'jan' : jan,
                    'feb' : feb,
                    'mar' : mar,
                    'apr' : apr,
                    'mei' : mei,
                    'jun' : jun,
                    'jul' : jul,
                    'aug' : aug,
                    'sep' : sep,
                    'oct' : oct,
                    'nov' : nov,
                    'dec' : dec,
                    'is_jan' : is_jan,
                    'is_feb' : is_feb,
                    'is_mar' : is_mar,
                    'is_apr' : is_apr,
                    'is_mei' : is_mei,
                    'is_jun' : is_jun,
                    'is_jul' : is_jul,
                    'is_aug' : is_aug,
                    'is_sep' : is_sep,
                    'is_oct' : is_oct,
                    'is_nov' : is_nov,
                    'is_dec' : is_dec,
                    'harga' : total_harga,
                    'total_bayar' : total_dibayar,
                    'amount_due' : total_harga - total_dibayar,
                }])

            else:
                print('Iside biaya non bulanan')
                for sb in siswa_biaya_ids:
                    reg_pembayaran.append([0,0,{
                        'siswa_id' : rbs.siswa_id.id,
                        'rombel_id' : rbs.rombel_id.id,
                        'biaya_id' : self.biaya_id.id,
                        'harga' : sb.harga,
                        'amount_due' : sb.amount_due,
                        'total_bayar' : sb.dibayar,
                    }])
        
        print('print isi reg_ppembayaran')
        pprint(reg_pembayaran)

        self.write({
            'pembayaran_siswa_ids' : reg_pembayaran
        })

        # if not self.rombel_id:
        #     get_rombel_ids = self.env['siswa_ocb11.rombel'].search([])
        #     self.rombel_id = get_rombel_ids

        # return self.env.ref('siswa_keu_ocb11.report_pembayaran_siswa_per_biaya_action').report_action(self)

        # ---------------------------------------------
        if self.biaya_id.is_bulanan:
            # return {
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'res_model': 'siswa_keu_ocb11.wizard_report_pembayaran_siswa',
            #     'target': 'current',
            #     'res_id': self.id,
            #     'type': 'ir.actions.act_window',
            #     'view_id': self.env.ref('siswa_keu_ocb11.wizard_report_pembayaran_siswa_form').id,
            # }
            
            return self.env.ref('siswa_keu_ocb11.report_pembayaran_siswa_per_biaya_action_bulanan').report_action(self)

        else:
            # # return as view
            # return {
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'res_model': 'siswa_keu_ocb11.wizard_report_pembayaran_siswa',
            #     'target': 'current',
            #     'res_id': self.id,
            #     'type': 'ir.actions.act_window',
            #     'view_id': self.env.ref('siswa_keu_ocb11.wizard_report_pembayaran_siswa_form_non_bulanan').id,
            # }

            # return as report
            return self.env.ref('siswa_keu_ocb11.report_pembayaran_siswa_per_biaya_action').report_action(self)

    
    def action_print(self):
        return self.env.ref('siswa_keu_ocb11.report_pembayaran_siswa_per_biaya_action').report_action(self) 