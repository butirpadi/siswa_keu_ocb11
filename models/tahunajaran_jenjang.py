# -*- coding: utf-8 -*-

from flectra import models, fields, api, exceptions, _
from pprint import pprint
import calendar

class tahunajaran_jenjang(models.Model):
    _inherit = 'siswa_ocb11.tahunajaran_jenjang'

    biayas = fields.One2many('siswa_keu_ocb11.biaya_ta_jenjang', inverse_name='tahunajaran_jenjang_id' , string='Biaya-biaya')

    def action_reset(self):
        # delete siswa_biaya
        rombel_ids = self.env['siswa_ocb11.rombel'].search([('jenjang_id','=',self.jenjang_id.id)]).ids
        siswas = self.env['siswa_ocb11.rombel_siswa'].search([
                    ('tahunajaran_id','=',self.tahunajaran_id.id),
                    ('rombel_id','in',rombel_ids),
                ])
        siswa_ids = []
        for sis in siswas:
            siswa_ids.append(sis.siswa_id.id)
            
        self.env['siswa_keu_ocb11.siswa_biaya'].search([('tahunajaran_id','=',self.tahunajaran_id.id),('siswa_id','in',siswa_ids)]).unlink()        
        # update state 
        self.state = 'draft'
        # delete biaya
        self.biayas.unlink()

    def validate_state(self):
        self.ensure_one()
        if self.biayas and len(self.biayas) > 0:
            # rombel_ids = self.env['siswa_ocb11.rombel'].search([('jenjang','=',int(self.jenjang))]).ids
            rombel_ids = self.env['siswa_ocb11.rombel'].search([('jenjang_id','=',self.jenjang_id.id)]).ids
            siswas = self.env['siswa_ocb11.rombel_siswa'].search([
                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                        ('rombel_id','in',rombel_ids),
                    ])
            
            # create/insert biaya to siswa
            for sis in siswas:
                total_biaya = 0
                for by in self.biayas:
                    if sis.siswa_id.is_siswa_lama and by.biaya_id.is_siswa_baru_only:
                        print('skip')
                    else:
                        if by.biaya_id.is_bulanan:
                            for bulan_index in range(1,13):
                                harga = by.harga
                                if by.is_different_by_gender:
                                    if sis.siswa_id.jenis_kelamin == 'perempuan':
                                        harga = by.harga_alt
                                self.env['siswa_keu_ocb11.siswa_biaya'].create({
                                    'name' : by.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                                    'siswa_id' : sis.siswa_id.id,
                                    'tahunajaran_id' : self.tahunajaran_id.id,
                                    'biaya_id' : by.biaya_id.id,
                                    'bulan' : bulan_index,
                                    'harga' : harga,
                                    'amount_due' : harga,
                                    'jenjang_id' : self.jenjang_id.id
                                })
                                total_biaya += harga
                        else:
                            harga = by.harga
                            if by.is_different_by_gender:
                                if sis.siswa_id.jenis_kelamin == 'perempuan':
                                    harga = by.harga_alt
                            self.env['siswa_keu_ocb11.siswa_biaya'].create({
                                'name' : by.biaya_id.name,
                                'siswa_id' : sis.siswa_id.id,
                                'tahunajaran_id' : self.tahunajaran_id.id,
                                'biaya_id' : by.biaya_id.id,
                                'harga' : harga,
                                'amount_due' : harga,
                                'jenjang_id' : self.jenjang_id.id
                            })
                            total_biaya += harga
                            
                # set total_biaya dan amount_due
                # total_biaya = sum(by.harga for by in self.biayas)
                self.env['res.partner'].search([('id','=',sis.siswa_id.id)]).write({
                    'total_biaya' : total_biaya,
                    'amount_due_biaya' : total_biaya,
                })
                # print(sis.siswa_id.name + ' ' + sis.siswa_id.active_rombel_id.name)
            #update state
            self.write({
                'state' : 'valid'
            })
        else:
            # raise error warning
            raise exceptions.except_orm(_('Warning'), _('There is no data to validate.'))        
    
    def recompute_biaya(self):
        self.ensure_one()
        print('Recompute Biaya Siswa')
        if self.biayas and len(self.biayas) > 0:
            # siswas = self.env['siswa_ocb11.rombel_siswa'].search([('tahunajaran_id','=',self.tahunajaran_id.id),('jenjang','=',self.jenjang)])
            siswas = self.env['siswa_ocb11.rombel_siswa'].search([('tahunajaran_id','=',self.tahunajaran_id.id),('jenjang_id','=',self.jenjang_id.id)])
            for biy in self.biayas:
                for sis in siswas:
                    found = False
                    for siswa_biaya in sis.siswa_id.biayas:
                        if(siswa_biaya.biaya_id.id == biy.biaya_id.id):
                            found = True
                    
                    if not found:
                        print('Add biaya to : ' + sis.siswa_id.name)
                        # jika tidak tersedia maka inputkan baru
                        if sis.siswa_id.is_siswa_lama and biy.biaya_id.is_siswa_baru_only:
                            print('skip')
                        else:
                            if biy.biaya_id.is_bulanan:
                                for bulan_index in range(1,13):
                                    harga = biy.harga
                                    if biy.is_different_by_gender:
                                        if sis.siswa_id.jenis_kelamin == 'perempuan':
                                            harga = biy.harga_alt
                                    print(harga)
                                    self.env['siswa_keu_ocb11.siswa_biaya'].create({
                                        'name' : biy.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                                        'siswa_id' : sis.siswa_id.id,
                                        'tahunajaran_id' : self.tahunajaran_id.id,
                                        'biaya_id' : biy.biaya_id.id,
                                        'bulan' : bulan_index,
                                        'harga' : harga,
                                        'amount_due' : harga,
                                        'jenjang_id' : self.jenjang_id.id
                                    })
                            else:
                                harga = biy.harga
                                if biy.is_different_by_gender:
                                    if sis.siswa_id.jenis_kelamin == 'perempuan':
                                        harga = biy.harga_alt
                                print(harga)
                                self.env['siswa_keu_ocb11.siswa_biaya'].create({
                                    'name' : biy.biaya_id.name,
                                    'siswa_id' : sis.siswa_id.id,
                                    'tahunajaran_id' : self.tahunajaran_id.id,
                                    'biaya_id' : biy.biaya_id.id,
                                    'harga' : harga,
                                    'amount_due' : harga,
                                    'jenjang_id' : self.jenjang_id.id
                                })
            print('End of Recompute Siswa Biaya')
        else:
            # raise error warning
            raise exceptions.except_orm(_('Warning'), _('There is no data to validate.'))

        # print(len(siswas))
        # for slf in self:
        #     rombel_ids = self.env['siswa_ocb11.rombel'].search([('jenjang','=',int(slf.jenjang))]).ids
        #     siswas = self.env['siswa_ocb11.rombel_siswa'].search([
        #                 ('tahunajaran_id','=',slf.tahunajaran_id.id),
        #                 ('rombel_id','in',rombel_ids),
        #             ])
        #     # create/insert biaya to siswa
        #     for sis in siswas:
        #         for by in slf.biayas:
        #             self.env['siswa_keu_ocb11.siswa_biaya'].create({
        #                 'name' : sis.siswa_id.induk + ' ' + by.biaya_id.name,
        #                 'siswa_id' : sis.siswa_id.id,
        #                 'tahunajaran_id' : slf.tahunajaran_id.id,
        #                 'biaya_id' : by.biaya_id.id,
        #                 'harga' : by.harga,
        #             })
        #         # set total_biaya dan amount_due
        #         total_biaya = sum(by.harga for by in slf.biayas)
        #         self.env['res.partner'].search([('id','=',sis.siswa_id.id)]).write({
        #             'total_biaya' : total_biaya,
        #             'amount_due_biaya' : total_biaya,
        #         })
        #         # print(sis.siswa_id.name + ' ' + sis.siswa_id.active_rombel_id.name)
        #     # update state
        #     slf.write({
        #         'state' : 'valid'
        #     })

    @api.multi
    def write(self, vals):
        print('inside write tahunajaran jenjang')
        self.ensure_one()
        res = super(tahunajaran_jenjang, self).write(vals)        
        return res 