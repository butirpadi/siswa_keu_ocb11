# -*- coding: utf-8 -*-

from flectra import models, fields, api, exceptions, _

class PotonganBiaya(models.Model):
    _name = 'siswa.potongan_biaya'

    name = fields.Char('Name', default="")
    siswa_id = fields.Many2one('res.partner', string="Siswa", required=True, ondelete="cascade")
    siswa_biaya_id = fields.Many2one('siswa_keu_ocb11.siswa_biaya', required=True, ondelete="cascade")
    related_siswa_id = fields.Many2one('res.partner', string="Siswa", related='siswa_biaya_id.siswa_id', store=True)
    related_biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string="Biaya", related='siswa_biaya_id.biaya_id', store=True)
    related_tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", related="siswa_biaya_id.tahunajaran_id", store=True)
    related_amount_due = fields.Float('Amount Due', related="siswa_biaya_id.amount_due", store=True)
    related_harga = fields.Float('Harga', related="siswa_biaya_id.harga", store=True)
    related_bulan = fields.Selection([(0, '-'), 
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
                            ], string='Bulan', related="siswa_biaya_id.bulan")
    jumlah_potongan = fields.Float('Jumlah Potongan', default=0.0, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    wizard_id = fields.Many2one('siswa_wizard_batch_create_potongan', string="Wizard", ondelete="cascade")

    def _recalculate_keuangan_dashboard(self):
        # recalculate keuangan dashboard
        dash_keuangan_id = self.env['ir.model.data'].search([('name','=','default_dashboard_pembayaran')]).res_id
        dash_keuangan = self.env['siswa_keu_ocb11.keuangan_dashboard'].search([('id','=',dash_keuangan_id)])
        for dash in dash_keuangan:
            dash.compute_keuangan()    
    
    def action_confirm(self):
        # # update amount due siswa_biaya
        if self.siswa_biaya_id.state == 'open':
            # set name
            self.name = self.siswa_id.name
            # update amount_due on siswa_biaya
            print('update amount due of siswa biaya ------')
            self.env['siswa_keu_ocb11.siswa_biaya'].search([('id','=',self.siswa_biaya_id.id)]).write({
                'amount_due' : self.siswa_biaya_id.amount_due - self.jumlah_potongan
            })
            # self.env.cr.execute("update siswa_keu_ocb11_siswa_biaya set amount_due = " + str(self.siswa_biaya_id.amount_due - self.jumlah_potongan) + " where id = " + str(self.siswa_biaya_id.id))
            
            # update total tagihan siswa
            print('Recompute Total Biaya Siswa')
            self.siswa_id._compute_total_biaya()
            print('Recompute total biaya siswa after potongan done')
            # update state to 'open'
            self.state = 'open'
            # recalculate keuangan dashboard
            self._recalculate_keuangan_dashboard()
            print('Recalculate keuangan dashboard after potongan done')
        else:
            print('state of siswa_biaya is paid')
        #     raise exceptions.except_orm(_('Error'), _('Potongan Biaya tidak dapat di gunakan pada biaya "' + self.siswa_biaya_id.biaya_id.name + '"'))

        # cek state siswa_biaya_id 
        # print('state of siswa_biaya : ' + self.siswa_biaya_id.state)
    
    def action_reset(self):
        if self.state == 'open':
            # update amount_due siswa_biaya
            self.env.cr.execute("update siswa_keu_ocb11_siswa_biaya set amount_due = " + str(self.siswa_biaya_id.amount_due + self.jumlah_potongan) + " where id = " + str(self.siswa_biaya_id.id))
            # update total tagihan siswa
            print('Recompute Total Biaya Siswa')
            self.siswa_id._compute_total_biaya()
            # update state to draft
            self.state = 'draft'
            # recalculate keuangan dashboard
            self._recalculate_keuangan_dashboard()
        else:
            raise exceptions.except_orm(_('Error'), _('Can not reset on this state.'))
    
    def action_wizard(self):
        print('how wizard batch create')

        return {

            'type': 'ir.actions.act_window', 
            'view_type': 'form', 
            'view_mode': 'form',
            'res_model': 'siswa_wizard_batch_create_potongan', 
            'target': 'new', 

        }

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                # alert can not delete on paid state
                raise exceptions.except_orm(_('Warning'), _('You can not delete this data at this state.'))
            else:
                res =  super(PotonganBiaya, self).unlink()
                return res


    # @api.onchange('siswa_id')
    # def siswa_id_onchange(self):
    #     # set name
    #     # print('Nama Siswa : ' + str(self.siswa_id.name))
    #     self.name = self.siswa_id.name
    #     # set domain
    #     domain = {'siswa_biaya_id':[('siswa_id','=',self.siswa_id.id)]}
    #     return {'domain':domain, 'value':{'siswa_biaya_id':[]}} 