# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint

class siswa(models.Model):
    _inherit = 'res.partner'

    biayas = fields.One2many('siswa_keu_ocb11.siswa_biaya', inverse_name='siswa_id', string='Biaya-biaya') 
    total_biaya = fields.Float('Total Biaya')
    amount_due_biaya = fields.Float('Amount Due')

    def _compute_total_biaya(self):
        print('inside _compute_total_biaya')
        total = 0
        amount = 0
        for by in self.biayas:
            total+=by.harga
            amount+=by.amount_due

        # self.total_biaya = total
        # self.amount_due_biaya = amount
        
        query = "update res_partner \
                set total_biaya = (select sum(harga) from siswa_keu_ocb11_siswa_biaya where siswa_id = " + str(self.id) + "),  \
                amount_due_biaya = (select sum(amount_due) from siswa_keu_ocb11_siswa_biaya where siswa_id = " + str(self.id) + ") \
                where id = " + str(self.id)
        print('running query ... ')
        print(query)
        self.env.cr.execute(query)


