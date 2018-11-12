# -*- coding: utf-8 -*-

from flectra import models, fields, api, _
from pprint import pprint
from datetime import datetime, date
import calendar

class biaya_ta_jenjang(models.Model):
    _name = 'siswa_keu_ocb11.biaya_ta_jenjang'

    name = fields.Char('Name', related="biaya_id.name")
    tahunajaran_jenjang_id = fields.Many2one('siswa_ocb11.tahunajaran_jenjang', string='Tahun Ajaran', required=True, ondelete='cascade')
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya', required=True)
    is_different_by_gender = fields.Boolean('Different by Gender',related='biaya_id.is_different_by_gender')
    harga = fields.Float('Harga', required=True, default=0)
    harga_alt = fields.Float('Harga (Alt)', required=True, default=0)

    def recompute_biaya_ta_jenjang(self):
        print('recompute biaya ta jenjang')

        # get data siswa
        rb_sis_ids = self.env['siswa_ocb11.rombel_siswa'].search([
            ('tahunajaran_id', '=', self.tahunajaran_jenjang_id.tahunajaran_id.id),
            ('jenjang_id', '=', self.tahunajaran_jenjang_id.jenjang_id.id),
        ])

        for sis in rb_sis_ids:
            siswa = sis.siswa_id
            total_biaya = 0

            if sis.siswa_id.active:
                if siswa.is_siswa_lama and self.biaya_id.is_siswa_baru_only:
                    print('skip')
                else:
                    print('JENJANG ID : ' + str(self.tahunajaran_jenjang_id.jenjang_id.id))
                    if self.biaya_id.is_bulanan:
                        for bulan_index in range(1,13):
                            harga = self.harga
                            
                            if self.biaya_id.is_different_by_gender:
                                if siswa.jenis_kelamin == 'perempuan':
                                    harga = self.harga_alt

                            self.env['siswa_keu_ocb11.siswa_biaya'].create({
                                'name' : self.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                                'siswa_id' : siswa.id,
                                'tahunajaran_id' : self.tahunajaran_jenjang_id.tahunajaran_id.id,
                                'biaya_id' : self.biaya_id.id,
                                'bulan' : bulan_index,
                                'harga' : harga,
                                'amount_due' : harga,
                                'jenjang_id' : self.tahunajaran_jenjang_id.jenjang_id.id
                            })
                            total_biaya += harga
                    else:
                        harga = self.harga
                        
                        if self.biaya_id.is_different_by_gender:
                            if siswa.jenis_kelamin == 'perempuan':
                                harga = self.harga_alt

                        self.env['siswa_keu_ocb11.siswa_biaya'].create({
                            'name' : self.biaya_id.name,
                            'siswa_id' : siswa.id,
                            'tahunajaran_id' : self.tahunajaran_jenjang_id.tahunajaran_id.id,
                            'biaya_id' : self.biaya_id.id,
                            'harga' : harga,
                            'amount_due' : harga,
                            'jenjang_id' : self.tahunajaran_jenjang_id.jenjang_id.id
                        })
                        total_biaya += harga
                            
            # set total_biaya dan amount_due
            # total_biaya = sum(self.harga for by in self.biayas)
            print('ID SISWA : ' + str(siswa.id))
            res_partner_siswa = self.env['res.partner'].search([('id','=',siswa.id)])
            self.env['res.partner'].search([('id','=',siswa.id)]).write({
                'total_biaya' : total_biaya,
                'amount_due_biaya' : res_partner_siswa.amount_due_biaya + total_biaya,
            })  

        # Recompute Tagihan Siswa Dashboard/ Keuangan Dashboard
        self.recompute_dashboard()
    
    def reset_biaya_ta_jenjang(self):
        rb_sis_ids = self.env['siswa_ocb11.rombel_siswa'].search([
            ('tahunajaran_id', '=', self.tahunajaran_jenjang_id.tahunajaran_id.id),
            ('jenjang_id', '=', self.tahunajaran_jenjang_id.jenjang_id.id),
        ])

        for sis in rb_sis_ids:
            siswa = sis.siswa_id

            self.env['siswa_keu_ocb11.siswa_biaya'].search(['&','&','&',
                ('tahunajaran_id', '=', self.tahunajaran_jenjang_id.tahunajaran_id.id),
                ('biaya_id', '=', self.biaya_id.id),
                ('state', '=', 'open'),
                ('siswa_id', '=', siswa.id),
            ]).unlink()
        
        # Recompute Tagihan Siswa Dashboard/ Keuangan Dashboard
        self.recompute_dashboard()
    
    def recompute_dashboard(self):
        dash_keuangan_id = self.env['ir.model.data'].search([('name','=','default_dashboard_pembayaran')]).res_id
        dash_keuangan = self.env['siswa_keu_ocb11.keuangan_dashboard'].search([('id','=',dash_keuangan_id)])
        for dash in dash_keuangan:
            dash.compute_keuangan()  
        print('Recompute Keuangan Dashboard done')

    @api.model
    def create(self, vals):
        if not vals['is_different_by_gender']:
            vals['harga_alt'] = vals['harga']        
        result = super(biaya_ta_jenjang, self).create(vals)
        return result

    @api.multi
    def write(self, vals):
        self.ensure_one()

        # print('isisnya : ')
        # pprint(vals)

        # # get biaya
        # # biaya_ta_jenjang = self.env['siswa_keu_ocb11.biaya_ta_jenjang'].search([('id','=',vals['id'])])
        # biaya = self.env['siswa_keu_ocb11.biaya'].search([('id','=',vals['biaya_id'])])

        # if not biaya[0].is_different_by_gender: #vals['is_different_by_gender']:
        if not self.biaya_id.is_different_by_gender: 
            if 'harga' in vals:
                vals['harga_alt'] = vals['harga']
        res = super(biaya_ta_jenjang, self).write(vals)        
        return res
