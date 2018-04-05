# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
import calendar

class tahunajaran_jenjang(models.Model):
    _inherit = 'siswa_ocb11.tahunajaran_jenjang'

    biayas = fields.One2many('siswa_keu_ocb11.biaya_ta_jenjang', inverse_name='tahunajaran_jenjang_id' , string='Biaya-biaya')
    
    def validate_state(self):
        self.ensure_one()
        rombel_ids = self.env['siswa_ocb11.rombel'].search([('jenjang','=',int(self.jenjang))]).ids
        siswas = self.env['siswa_ocb11.rombel_siswa'].search([
                    ('tahunajaran_id','=',self.tahunajaran_id.id),
                    ('rombel_id','in',rombel_ids),
                ])
        # create/insert biaya to siswa
        for sis in siswas:
            for by in self.biayas:
                if by.biaya_id.is_bulanan:
                    for bulan_index in range(1,13):
                        print(bulan_index)
                        self.env['siswa_keu_ocb11.siswa_biaya'].create({
                            'name' : by.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                            'siswa_id' : sis.siswa_id.id,
                            'tahunajaran_id' : self.tahunajaran_id.id,
                            'biaya_id' : by.biaya_id.id,
                            'bulan' : bulan_index,
                            'harga' : by.harga,
                        })
                else:
                    self.env['siswa_keu_ocb11.siswa_biaya'].create({
                        'name' : by.biaya_id.name,
                        'siswa_id' : sis.siswa_id.id,
                        'tahunajaran_id' : self.tahunajaran_id.id,
                        'biaya_id' : by.biaya_id.id,
                        'harga' : by.harga,
                    })
            # set total_biaya dan amount_due
            total_biaya = sum(by.harga for by in self.biayas)
            self.env['res.partner'].search([('id','=',sis.siswa_id.id)]).write({
                'total_biaya' : total_biaya,
                'amount_due_biaya' : total_biaya,
            })
            # print(sis.siswa_id.name + ' ' + sis.siswa_id.active_rombel_id.name)
        # update state
        self.write({
            'state' : 'valid'
        })
    
    def recompute_biaya(self):
        for slf in self:
            rombel_ids = self.env['siswa_ocb11.rombel'].search([('jenjang','=',int(slf.jenjang))]).ids
            siswas = self.env['siswa_ocb11.rombel_siswa'].search([
                        ('tahunajaran_id','=',slf.tahunajaran_id.id),
                        ('rombel_id','in',rombel_ids),
                    ])
            # create/insert biaya to siswa
            for sis in siswas:
                for by in slf.biayas:
                    self.env['siswa_keu_ocb11.siswa_biaya'].create({
                        'name' : sis.siswa_id.induk + ' ' + by.biaya_id.name,
                        'siswa_id' : sis.siswa_id.id,
                        'tahunajaran_id' : slf.tahunajaran_id.id,
                        'biaya_id' : by.biaya_id.id,
                        'harga' : by.harga,
                    })
                # set total_biaya dan amount_due
                total_biaya = sum(by.harga for by in slf.biayas)
                self.env['res.partner'].search([('id','=',sis.siswa_id.id)]).write({
                    'total_biaya' : total_biaya,
                    'amount_due_biaya' : total_biaya,
                })
                # print(sis.siswa_id.name + ' ' + sis.siswa_id.active_rombel_id.name)
            # update state
            slf.write({
                'state' : 'valid'
            })