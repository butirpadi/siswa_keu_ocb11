# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.addons import decimal_precision as dp
from datetime import datetime
from pprint import pprint


class pembayaran(models.Model):
    _name = 'siswa_keu_ocb11.pembayaran'

    state = fields.Selection([('draft', 'Draft'), ('paid', 'Paid')], string='State', required=True, default='draft')
    name = fields.Char(string='Kode Pembayaran', requred=True, default='New')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', required=True, default=lambda x: x.env['siswa_ocb11.tahunajaran'].search([('active', '=', True)]))
    siswa_id = fields.Many2one('res.partner', string='Siswa', required=True)
    induk = fields.Char(string='No. Induk', related='siswa_id.induk')
    active_rombel_id = fields.Many2one('siswa_ocb11.rombel', related='siswa_id.active_rombel_id', string='Rombongan Belajar')
    rombel_id = fields.Many2one('siswa_ocb11.rombel', string="Rombongan Belajar", compute="_compute_set_rombel", store=True)
    tanggal = fields.Date('Tanggal', required=True, default=datetime.today())
    total = fields.Float('Total', required=True, default=0.00, compute="_compute_biaya")
    terbilang = fields.Char('Terbilang', compute="_compute_terbilang", store=True)
    pembayaran_lines = fields.One2many('siswa_keu_ocb11.pembayaran_line', inverse_name='pembayaran_id' , string='Biaya-biaya', require=True)
    satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
          'delapan', 'sembilan', 'sepuluh', 'sebelas']
    is_potong_tabungan = fields.Boolean('Potong Tabungan ?', default=False)
    jumlah_potongan_tabungan = fields.Float('Potongan Tabungan', default=0)
    tabungan_id = fields.Many2one('siswa_tab_ocb11.tabungan', string="Transaksi Tabungan")
    saldo_tabungan_siswa = fields.Float(related='siswa_id.saldo_tabungan', store=True)
    total_temp = fields.Float('Total Bayar', default=0, readonly=True, store=True)

    @api.onchange('jumlah_potongan_tabungan')
    def jumlah_potongan_tabungan_change(self):
        if self.jumlah_potongan_tabungan > self.total:
            # self.jumlah_potongan_tabungan = 0
            # self.total_temp = self.total - self.jumlah_potongan_tabungan
            return {'warning': {
                    'title': _('Warning'),
                    'message': _('Potongan tabungan melebihi jumlah total tagihan.')
                    }}

        if self.jumlah_potongan_tabungan > self.saldo_tabungan_siswa:
            # alert jumlah potongan melebihgi saldo
            # self.jumlah_potongan_tabungan = 0
            # self.total_temp = self.total - self.jumlah_potongan_tabungan
            return {'warning': {
                    'title': _('Warning'),
                    'message': _('Saldo tabungan tidak mencukupi.')
                    }}
        
        self.total_temp = self.total - self.jumlah_potongan_tabungan

    @api.depends('siswa_id')
    def _compute_set_rombel(self):
        for rec in self:
            # get rombel on this tahunajaran for this siswa
            rombel = self.env['siswa_ocb11.rombel_siswa'].search([
                ('tahunajaran_id', '=', rec.tahunajaran_id.id),
                ('siswa_id', '=', rec.siswa_id.id),
                ])
            pprint(rombel)
            for rb in rombel:
                rec.rombel_id = rb.rombel_id.id
            print('compute set rombel')

    @api.onchange('is_potong_tabungan')
    def potong_tabungan_change(self):
        if self.is_potong_tabungan:
            # if self.saldo_tabungan_siswa < self.total:
            #     # tampilkan pesan tidak mencukupi
            #     self.is_potong_tabungan = False

            #     return {'warning': {
            #             'title': _('Warning'),
            #             'message': _('Saldo tabungan tidak mencukupi.')
            #             }}

            # pre set total_temp
            self.total_temp = self.total - self.jumlah_potongan_tabungan

            # tampilkan form input potongan
            if self.saldo_tabungan_siswa == 0:
                # tampilkan pesan tidak mencukupi
                self.is_potong_tabungan = False

                return {'warning': {
                    'title': _('Warning'),
                    'message': _('Saldo tabungan tidak mencukupi.')
                }}
        else:
            # reset total dan jumlah_potongan_tabungan
            self.jumlah_potongan_tabungan = 0
            self.total_temp = self.total - self.jumlah_potongan_tabungan
        
        print('is potong tabungan : ' + str(self.is_potong_tabungan))

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
        # delete from tabungan if potong_tabungan
        if self.is_potong_tabungan:
            # print(self.tabungan_id.name)
            self.tabungan_id.action_cancel()
            self.tabungan_id.unlink()
        #     raise exceptions.except_orm(_('Warning'), _('TEST ERROR'))

        # delete from action_confirm table
        self.env['siswa_keu_ocb11.action_confirm'].search([('pembayaran_id', '=', self.id)]).unlink()
        # delete from kas statement
        kas = self.env['siswa_keu_ocb11.kas'].search([('pembayaran_id', '=', self.id)])
        for dt in kas:
            dt.action_cancel()
            dt.unlink()
            
        # update status di siswa_biaya
        for bayar in self.pembayaran_lines:
            self.env['siswa_keu_ocb11.siswa_biaya'].search([('id', '=', bayar.biaya_id.id)]).write({
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

        # recompute keuangan dashboard
        self.recompute_keuangan_dashboard()
        
        # reset amount_due on pembayaran_lines
        print('reset amount due on siswa_biaya using potongan_biaya ...')
        for bayar in self.pembayaran_lines:
            self.env['siswa_keu_ocb11.siswa_biaya'].search([('id', '=', bayar.biaya_id.id)]).write({
                'amount_due' : bayar.biaya_id.amount_due + bayar.jumlah_potongan,
                'dibayar' : bayar.biaya_id.dibayar - bayar.jumlah_potongan,
            })

            # update amount_due on siswa
            print('update amount_due_biaya on siswa ...')
            self.siswa_id.write({
                'amount_due_biaya' : self.siswa_id.amount_due_biaya + bayar.jumlah_potongan
            })

            # reset status potongan_biaya
            if bayar.biaya_id.potongan_ids:
                for pot in bayar.biaya_id.potongan_ids:
                    pot.state = 'open'
        
        # reset amount_due on pembayaran_lines
        print('reset amount due on siswa_biaya using potongan_biaya ...')
        for bayar in self.pembayaran_lines:
            self.env['siswa_keu_ocb11.siswa_biaya'].search([('id', '=', bayar.biaya_id.id)]).write({
                'amount_due' : bayar.biaya_id.amount_due + bayar.jumlah_potongan,
                'dibayar' : bayar.biaya_id.dibayar - bayar.jumlah_potongan,
            })

            # update amount_due on siswa
            print('update amount_due_biaya on siswa ...')
            self.siswa_id.write({
                'amount_due_biaya' : self.siswa_id.amount_due_biaya + bayar.jumlah_potongan
            })

            # reset status potongan_biaya
            if bayar.biaya_id.potongan_ids:
                for pot in bayar.biaya_id.potongan_ids:
                    pot.state = 'open'

        return self.reload_page()
    
    def recompute_keuangan_dashboard(self):
        # recompute dashboard tagihan siswa
        dash_keuangan_id = self.env['ir.model.data'].search([('name', '=', 'default_dashboard_pembayaran')]).res_id
        dash_keuangan = self.env['siswa_keu_ocb11.keuangan_dashboard'].search([('id', '=', dash_keuangan_id)])
        for dash in dash_keuangan:
            dash.compute_keuangan()        
        # raise exceptions.except_orm(_('Warning'), _('TEST ERROR COMPUTE KEUANGAN DASHBOARD'))
    
#     def action_confirm(self):
#         self.ensure_one()
#         # check if pembayaran is set or no
#         if len(self.pembayaran_lines) > 0:
#             # update state
#             self.write({
#                 'state' : 'paid'
#             })
#             # set paid to siswa_biaya
#             for bayar in self.pembayaran_lines:
#                 if bayar.bayar == bayar.amount_due - bayar.jumlah_potongan:
#                     bayar.biaya_id.write({
#                         'state' : 'paid',
#                         'amount_due' : 0,
#                         'dibayar' : bayar.biaya_id.dibayar + bayar.bayar,
#                     })
#                 else:
#                     bayar.biaya_id.write({
#                         # 'amount_due' : bayar.biaya_id.amount_due - bayar.jumlah_potongan - bayar.bayar,
#                         'amount_due' : bayar.biaya_id.amount_due - bayar.bayar,
#                         'dibayar' : bayar.biaya_id.dibayar + bayar.bayar
#                     })
#                 # update amount_due_biaya on siswa
#                 self.siswa_id.write({
#                     'amount_due_biaya' : self.siswa_id.amount_due_biaya - bayar.bayar
#                 })
# 
#                 # set potongan biaya to paid 
#                 if bayar.biaya_id.potongan_ids:
#                     for pot_by in bayar.biaya_id.potongan_ids:
#                         pot_by.state = 'paid'
#             
#             # add confirm progress to table action_confirm
#             self.env['siswa_keu_ocb11.action_confirm'].create({
#                 'pembayaran_id' : self.id
#             })
# 
#             # update kas statement per item pembayaran lines
#             for pb in self.pembayaran_lines:
#                 akun_kas_id = self.env['siswa_keu_ocb11.kas_kategori'].search([('biaya_id', '=', pb.biaya_id.biaya_id.id)]).id
#                 
#                 kas = self.env['siswa_keu_ocb11.kas'].create({
#                     'tanggal' : self.tanggal,
#                     'jumlah' : pb.bayar,
#                     'pembayaran_id' : self.id ,
#                     'is_related' : True ,
#                     'kas_kategori_id' : akun_kas_id,
#                 })
#                 kas.action_confirm()
# 
#             # if is_potong_tabungan = True, maka potong tabungan
#             if self.is_potong_tabungan:
#                 # create trans tabungan
#                 new_tab = self.env['siswa_tab_ocb11.tabungan'].create({
#                     'siswa_id' : self.siswa_id.id,
#                     'tanggal' : self.tanggal,
#                     'jenis' : 'tarik',
#                     'jumlah_temp' : self.jumlah_potongan_tabungan,
#                     'desc' : 'Pembayaran ' + self.name,
#                 })
#                 new_tab.action_confirm()
#                 self.tabungan_id = new_tab.id
#             
#             # recompute keuangan dashboard
#             self.recompute_keuangan_dashboard()
# 
#             # reload
#             return self.reload_page()
# 
#         else:
#             raise exceptions.except_orm(_('Warning'), _('There is no data to confirm, complete payment first!'))

    def action_confirm(self):
        self.ensure_one()
        # check if pembayaran is set or no
        if len(self.pembayaran_lines) > 0:
            # update state
            self.write({
                'state' : 'paid'
            })
            # set paid to siswa_biaya
            for bayar in self.pembayaran_lines:
                print('Bayar : ' + str(bayar.bayar))
                print('Amount due : ' + str(bayar.amount_due))
#                 if bayar.bayar == (bayar.amount_due - bayar.jumlah_potongan):
                if str(bayar.bayar) == str(bayar.biaya_id.amount_due):
                    print('update amount due on siswa biaya and set siswa_biaya to paid')
                    bayar.biaya_id.write({
                        'state' : 'paid',
                        'amount_due' : 0,
                        'dibayar' : bayar.biaya_id.dibayar + bayar.bayar,
                    })
                else:
                    print('update amount due on siswa_biaya')
                    bayar.biaya_id.write({
                        # 'amount_due' : bayar.biaya_id.amount_due - bayar.jumlah_potongan - bayar.bayar,
                        'amount_due' : bayar.biaya_id.amount_due - bayar.bayar,
                        'dibayar' : bayar.biaya_id.dibayar + bayar.bayar,
                        'state' : 'paid' if (bayar.biaya_id.amount_due - bayar.bayar) == 0.0 else 'open'
                    })
                # update amount_due_biaya on siswa
                self.siswa_id.write({
                    'amount_due_biaya' : self.siswa_id.amount_due_biaya - bayar.bayar
                })

                # set potongan biaya to paid 
                if bayar.biaya_id.potongan_ids:
                    for pot_by in bayar.biaya_id.potongan_ids:
                        pot_by.state = 'paid'
            
            # add confirm progress to table action_confirm
            self.env['siswa_keu_ocb11.action_confirm'].create({
                'pembayaran_id' : self.id
            })

            # update kas statement per item pembayaran lines
            for pb in self.pembayaran_lines:
                akun_kas_id = self.env['siswa_keu_ocb11.kas_kategori'].search([('biaya_id', '=', pb.biaya_id.biaya_id.id)]).id
                
                kas = self.env['siswa_keu_ocb11.kas'].create({
                    'tanggal' : self.tanggal,
                    'jumlah' : pb.bayar,
                    'pembayaran_id' : self.id ,
                    'is_related' : True ,
                    'kas_kategori_id' : akun_kas_id,
                })
                kas.action_confirm()

            # if is_potong_tabungan = True, maka potong tabungan
            if self.is_potong_tabungan:
                # create trans tabungan
                new_tab = self.env['siswa_tab_ocb11.tabungan'].create({
                    'siswa_id' : self.siswa_id.id,
                    'tanggal' : self.tanggal,
                    'jenis' : 'tarik',
                    'jumlah_temp' : self.jumlah_potongan_tabungan,
                    'desc' : 'Pembayaran ' + self.name,
                })
                new_tab.action_confirm()
                self.tabungan_id = new_tab.id
            
            # recompute keuangan dashboard
            self.recompute_keuangan_dashboard()

            # reload
            return self.reload_page()

        else:
            raise exceptions.except_orm(_('Warning'), _('There is no data to confirm, complete payment first!'))

#     def action_confirm(self):
#         self.ensure_one()
#         # check if pembayaran is set or no
#         if len(self.pembayaran_lines) > 0:
#             # update state
#             self.write({
#                 'state' : 'paid'
#             })
#             # set paid to siswa_biaya
#             for bayar in self.pembayaran_lines:
#                 if bayar.bayar == bayar.amount_due:
#                     bayar.biaya_id.write({
#                         'state' : 'paid',
#                         'amount_due' : 0,
#                         'dibayar' : bayar.biaya_id.dibayar + bayar.bayar,
#                     })
#                 else:
#                     bayar.biaya_id.write({
#                         'amount_due' : bayar.biaya_id.amount_due - bayar.bayar,
#                         'dibayar' : bayar.biaya_id.dibayar + bayar.bayar
#                     })
#                 # update amount_due_biaya on siswa
#                 self.siswa_id.write({
#                     'amount_due_biaya' : self.siswa_id.amount_due_biaya - bayar.bayar
#                 })
#             
#             # add confirm progress to table action_confirm
#             self.env['siswa_keu_ocb11.action_confirm'].create({
#                 'pembayaran_id' : self.id
#             })
#             
#             # add kas statement
#             # kas_kategori_pembayaran_id = self.env['ir.model.data'].search([('name','=','default_kategori_kas')]).res_id
#             
#             # kas = self.env['siswa_keu_ocb11.kas'].create({
#             #     'tanggal' : self.tanggal,
#             #     'jumlah' : self.total,
#             #     'pembayaran_id' : self.id ,
#             #     'is_related' : True ,
#             #     'kas_kategori_id' : kas_kategori_pembayaran_id,
#             # })
#             # kas.action_confirm()
# 
#             # update kas statement per item pembayaran lines
#             for pb in self.pembayaran_lines:
#                 akun_kas_id = self.env['siswa_keu_ocb11.kas_kategori'].search([('biaya_id', '=', pb.biaya_id.biaya_id.id)]).id
#                 
#                 kas = self.env['siswa_keu_ocb11.kas'].create({
#                     'tanggal' : self.tanggal,
#                     'jumlah' : pb.bayar,
#                     'pembayaran_id' : self.id ,
#                     'is_related' : True ,
#                     'kas_kategori_id' : akun_kas_id,
#                 })
#                 kas.action_confirm()
# 
#             # if is_potong_tabungan = True, maka potong tabungan
#             if self.is_potong_tabungan:
#                 # create trans tabungan
#                 new_tab = self.env['siswa_tab_ocb11.tabungan'].create({
#                     'siswa_id' : self.siswa_id.id,
#                     'tanggal' : self.tanggal,
#                     'jenis' : 'tarik',
#                     'jumlah_temp' : self.jumlah_potongan_tabungan,
#                     'desc' : 'Pembayaran ' + self.name,
#                 })
#                 new_tab.action_confirm()
#                 self.tabungan_id = new_tab.id
#             
#             # recompute keuangan dashboard
#             self.recompute_keuangan_dashboard()
# 
#             # reload
#             return self.reload_page()
# 
#         else:
#             raise exceptions.except_orm(_('Warning'), _('There is no data to confirm, complete payment first!'))
# 
#     # @api.onchange('pembayaran_lines')
    
    @api.depends('pembayaran_lines.bayar')
    def _compute_biaya(self):
        for rec in self:
            # rec.total = sum(x.bayar for x in rec.pembayaran_lines)
            total_bayar = 0.0
            for pb in rec.pembayaran_lines:
                total_bayar += pb.bayar
                
            rec.update({
                'total' : total_bayar 
            })
            # print('Inside _compute_biaya')
    
    def reset_pembayaran_lines(self):
        self.ensure_one()
        biayas = self.env['siswa_keu_ocb11.siswa_biaya'].search([('siswa_id', '=', self.siswa_id.id), ('state', '=', 'open')])
        reg_biaya = []
        for by in biayas:
            reg_biaya.append([0, 0, {
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
        
        # calculate total_temp
        # self.total_temp = result.total = result.jumlah_potongan_tabungan
    
    @api.multi
    def write(self, vals):
        self.ensure_one()

        # update total_temp
        if 'is_potong_tabungan' in vals:
            # pprint(vals)
            # print('----------------------')
            vals['total_temp'] = float(self.total - vals['jumlah_potongan_tabungan'])
            # pprint(vals)

        res = super(pembayaran, self).write(vals)

        # update total
        if 'pembayaran_lines' in vals:
            self.total = sum(x.bayar for x in self.pembayaran_lines)
            # update total_temp
            self.total_temp = self.total - self.jumlah_potongan_tabungan
        
        # if 'jumlah_potongan_tabungan' in vals:
        #     print('saldo tabungan ' + str(self.saldo_tabungan_siswa))
        #     vals['total_temp'] = self.saldo_tabungan_siswa - vals['jumlah_potongan_tabungan']
        #     # vals['total_temp'] = 10000
        #     vals.update({
        #         total_temp : self.saldo_tabungan_siswa - vals['jumlah_potongan_tabungan']
        #     })
        
        # pprint(vals)

        # get siswa
        # if 'is_potong_tabungan' in vals:
            # pprint(vals)
            # print('----------------------')
            # siswa = self.env['res.partner'].search([('id','=',self.siswa_id)])
            # vals['total_temp'] = float(self.siswa_id.saldo_tabungan - vals['jumlah_potongan_tabungan'])
            # pprint(vals)

        return res

        # self.write({
        #     'total_temp' : self.saldo_tabungan_siswa - res.jumlah_potongan_tabungan
        # })
        
        # calculate total_temp
        # self.total_temp = res.total = res.jumlah_potongan_tabungan
        
    @api.multi
    def unlink(self):
        if self.state == 'paid':
            raise exceptions.except_orm(_('Warning'), _('You can not delete a payment that is already paid!'))
        else:
            return super(pembayaran, self).unlink()
