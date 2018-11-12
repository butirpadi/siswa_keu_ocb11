# -*- coding: utf-8 -*-

from flectra import models, fields, api, exceptions, _
from flectra.addons import decimal_precision as dp
from datetime import datetime
from pprint import pprint

class keuangan_dashboard(models.Model):
    _name = 'siswa_keu_ocb11.keuangan_dashboard'

    color = fields.Integer(string='Color Index') 
    name = fields.Char('Name')
    subtitle = fields.Char('Subtitle')
    rombel_id = fields.Many2one('siswa_ocb11.rombel', string='Rombongan Belajar')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran')
    total = fields.Float('Total', default=0.00)
    amount_due = fields.Float('Amount Due', default=0.00)
    paid_amount = fields.Float('Dibayar', default=0.00)
    amount_due_per_tahunajaran = fields.One2many('siswa_keu_ocb11.keuangan_dashboard_tahunajaran_rel',inverse_name='dashboard_id')

    def get_amount_per_ta(self, ta_id):
        am_ta = self.amount_due_per_tahunajaran.search([(
            'tahunajaran_id','=', ta_id
        )])
        return am_ta.amount_due

    def compute_keuangan(self):
        # get amount due
        self.env.cr.execute("select sum(coalesce(amount_due,0)) from siswa_keu_ocb11_siswa_biaya where state = 'open' and active=True")
        total_kas = self.env.cr.fetchone()[0]        
        
        self.amount_due = total_kas
        
        # # get amount due
        # siswa_biayas = self.env['siswa_keu_ocb11.siswa_biaya'].search([('state','=','open')])
        
        # if siswa_biayas:
        #     if len(siswa_biayas) > 0:
        #         self.amount_due = sum(siswa_biayas.mapped('amount_due'))

        # # get amount due per tahun ajaran
        # tahunajarans = self.env['siswa_ocb11.tahunajaran'].search([
        #                 ('active','ilike','%'),
        #                 ('name','ilike','%')
        #             ])
        # if tahunajarans:
        #     if len(tahunajarans) > 0:
        #         reg_amount_due_per_ta = []
        #         for ta in tahunajarans:
        #             amount_due_per_ta = sum(self.env['siswa_keu_ocb11.siswa_biaya'].search([
        #                 ('state','=','open'),
        #                 ('tahunajaran_id','=',ta.id),
        #                 ]).mapped('amount_due'))
        #             if amount_due_per_ta > 0:
        #                 reg_amount_due_per_ta.append([0,0,{
        #                     'amount_due' : amount_due_per_ta,
        #                     'tahunajaran_id' : ta.id
        #                 }])
                
        #         # delete data sebelumnya
        #         self.amount_due_per_tahunajaran.unlink()
        #         # input data terbaru
        #         self.amount_due_per_tahunajaran = reg_amount_due_per_ta
    
    def compute_kas(self):
        self.env.cr.execute("select sum(coalesce(debet,0))-sum(coalesce(kredit,0)) as saldo from siswa_keu_ocb11_kas where state ='post' ")
        total_kas = self.env.cr.fetchone()[0]        
        self.total = total_kas
        self.amount_due = total_kas
        print('saldo kas (total) : '  + str(self.total))
        print('saldo kas (amount_due) : '  + str(self.amount_due))
    
    def get_default_name(self):
        default_name = self.env['ir.model.data'].search([
                            ('model','=','siswa_keu_ocb11.keuangan_dashboard'),
                            ('res_id','=',self.id),
                        ]).name
        return default_name
             