# -*- coding: utf-8 -*-

from flectra import models, fields, api
from flectra.addons import decimal_precision as dp

class biaya(models.Model):
    _name = 'siswa_keu_ocb11.biaya'
    name = fields.Char(string='Nama', requred=True)
    is_bulanan = fields.Boolean('Bulanan',default=False)
    is_different_by_gender = fields.Boolean('Different by Gender?', default=False)
    is_siswa_baru_only = fields.Boolean('Hanya untuk siswa baru?', default=False)
    is_optional = fields.Boolean('Biaya Opsional?', default=False) 


    @api.model
    def create(self, vals):
        res = super(biaya, self).create(vals)

        # auto generate kas_kategori
        self.env['siswa_keu_ocb11.kas_kategori'].create({
            'name' : res.name,
            'tipe' : 'in',
            'is_biaya_account' : True,
            'biaya_id' : res.id
        })

        return res
    
    def regenerate_akun_kas(self):
        # cek apakah sudah ada atau belum
        akun_kas = self.env['siswa_keu_ocb11.kas_kategori'].search([('biaya_id','=',self.id)])
        if akun_kas:
            print('ada')
        else:
            # generate akun kas
            self.env['siswa_keu_ocb11.kas_kategori'].create({
                'name' : self.name,
                'tipe' : 'in',
                'is_biaya_account' : True,
                'biaya_id' : self.id
            })
