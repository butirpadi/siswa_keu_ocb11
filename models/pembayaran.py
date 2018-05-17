# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.addons import decimal_precision as dp
from datetime import datetime
from pprint import pprint

class pembayaran(models.Model):
    _name = 'siswa_keu_ocb11.pembayaran'

    state = fields.Selection([('draft', 'Draft'), ('paid', 'Paid')], string='State', required=True, default='draft')
    name = fields.Char(string='Kode Pembayaran', requred=True, default='New')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', required=True, default=lambda x: x.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]))
    siswa_id = fields.Many2one('res.partner', string='Siswa', required=True)
    induk = fields.Char(string='Induk', related='siswa_id.induk')
    active_rombel_id = fields.Many2one('siswa_ocb11.rombel', related='siswa_id.active_rombel_id', string='Rombongan Belajar')
    tanggal = fields.Date('Tanggal', required=True, default=datetime.today())
    total = fields.Float('Total', required=True, default=0.00)
    terbilang = fields.Char('Terbilang', compute="_compute_terbilang", store=True)
    pembayaran_lines = fields.One2many('siswa_keu_ocb11.pembayaran_line', inverse_name='pembayaran_id' , string='Biaya-biaya', require=True)
    satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
          'delapan', 'sembilan', 'sepuluh', 'sebelas']

    def terbilang_(self, n):
        if n >= 0 and n <= 11:
            hasil = [self.satuan[int(n)]]
        elif n >= 12 and n <= 19:
            hasil = self.terbilang_(n % 10) + ['belas']
        elif n >= 20 and n <= 99:
            hasil = self.terbilang_(n / 10) + ['puluh'] + self.terbilang_(n % 10)
        elif n >= 100 and n <= 199:
            hasil = ['seratus'] + self.terbilang_(n - 100)
        elif n >= 200 and n <= 999:
            hasil = self.terbilang_(n / 100) + ['ratus'] + self.terbilang_(n % 100)
        elif n >= 1000 and n <= 1999:
            hasil = ['seribu'] + self.terbilang_(n - 1000)
        elif n >= 2000 and n <= 999999:
            hasil = self.terbilang_(n / 1000) + ['ribu'] + self.terbilang_(n % 1000)
        elif n >= 1000000 and n <= 999999999:
            hasil = self.terbilang_(n / 1000000) + ['juta'] + self.terbilang_(n % 1000000)
        else:
            hasil = self.terbilang_(n / 1000000000) + ['milyar'] + self.terbilang_(n % 100000000)
        return hasil

    @api.depends('total')
    def _compute_terbilang(self):
        for rec in self:
            if rec.total == 0:
                rec.terbilang = 'nol'
            else:
                t = rec.terbilang_(rec.total)
                while '' in t:
                    t.remove('')
                rec.terbilang = ' '.join(t)        

    def reload_page(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_print(self):
        return self.env.ref('siswa_keu_ocb11.report_pembayaran_action').report_action(self)

    def action_cancel(self):
        self.ensure_one()
        # delete from action_confirm table
        self.env['siswa_keu_ocb11.action_confirm'].search([('pembayaran_id','=',self.id)]).unlink()
        # delete from kas statement
        kas = self.env['siswa_keu_ocb11.kas'].search([('pembayaran_id','=',self.id)])
        for dt in kas:
            dt.action_cancel()
            dt.unlink()
            
        # update status di siswa_biaya
        for bayar in self.pembayaran_lines:
            self.env['siswa_keu_ocb11.siswa_biaya'].search([('id','=',bayar.biaya_id.id)]).write({
                'state' : 'open',
                'amount_due' : bayar.biaya_id.amount_due + bayar.bayar,
                'dibayar' : bayar.biaya_id.dibayar - bayar.bayar,
            })
            # update amount_due on siswa
            self.siswa_id.write({
                'amount_due_biaya' : self.siswa_id.amount_due_biaya + bayar.bayar
            })
        # reset state
        self.write({
            'state' : 'draft'
        })
        return self.reload_page()

    def action_confirm(self):
        self.ensure_one()
        # update state
        self.write({
            'state' : 'paid'
        })
        # set paid to siswa_biaya
        for bayar in self.pembayaran_lines:
            if bayar.bayar == bayar.amount_due:
                bayar.biaya_id.write({
                    'state' : 'paid',
                    'amount_due' : 0,
                    'dibayar' : bayar.biaya_id.dibayar + bayar.bayar,
                })
            else:
                bayar.biaya_id.write({
                    'amount_due' : bayar.biaya_id.amount_due - bayar.bayar,
                    'dibayar' : bayar.biaya_id.dibayar + bayar.bayar
                })
            # update amount_due_biaya on siswa
            self.siswa_id.write({
                'amount_due_biaya' : self.siswa_id.amount_due_biaya - bayar.bayar
            })
        # add confirm progress to table action_confirm
        self.env['siswa_keu_ocb11.action_confirm'].create({
            'pembayaran_id' : self.id
        })
        # add kas statement
        kas_kategori_pembayaran_id = self.env['ir.model.data'].search([('name','=','default_kategori_kas')]).res_id
        
        kas = self.env['siswa_keu_ocb11.kas'].create({
            'tanggal' : self.tanggal,
            'desc' : 'Penerimaan Pembayaran Siswa' ,
            'jumlah' : self.total,
            'debet' : self.total,
            'pembayaran_id' : self.id ,
            'is_related' : True ,
            'kas_kategori_id' : kas_kategori_pembayaran_id,
        })
        kas.action_confirm()
        # reload
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }
        return self.reload_page()

    @api.onchange('pembayaran_lines')
    def _compute_biaya(self):
        self.ensure_one()
        self.total = sum(x.bayar for x in self.pembayaran_lines)
    
    def reset_pembayaran_lines(self):
        self.ensure_one()
        biayas = self.env['siswa_keu_ocb11.siswa_biaya'].search([('siswa_id','=',self.siswa_id.id),('state','=','open')])
        reg_biaya = []
        for by in biayas:
            reg_biaya.append([0,0,{
                'siswa_id' : self.siswa_id.id,
                'biaya_id' : by.id,
                'bayar' : by.harga,
            }])
        # delete existing record
        self.pembayaran_lines.unlink()
        # reset record
        self.write({
            'pembayaran_lines' : reg_biaya
        })

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('pembayaran.siswa.ocb11') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('pembayaran.siswa.ocb11') or _('New')

        # # populate biaya siswa        
        # biayas = self.env['siswa_keu_ocb11.siswa_biaya'].search([('siswa_id','=',vals['siswa_id']),('state','=','open')])
        # reg_biaya = []
        # for by in biayas:
        #     reg_biaya.append([0,0,{
        #         'siswa_id' : vals['siswa_id'],
        #         'biaya_id' : by.id,
        #         'bayar' : by.amount_due,
        #     }])
        
        # vals.update({
        #     'pembayaran_lines' : reg_biaya
        # })
        # vals['total'] = sum(x.harga for x in biayas)

        result = super(pembayaran, self).create(vals)
        return result
    
    @api.multi
    def write(self, vals):
        self.ensure_one()
        res = super(pembayaran, self).write(vals)
        # update total
        if 'pembayaran_lines' in vals:
            self.total = sum(x.bayar for x in self.pembayaran_lines)
        
        return res
