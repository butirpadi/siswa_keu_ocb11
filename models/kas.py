# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.addons import decimal_precision as dp
from datetime import datetime

class kas(models.Model):
    _name = 'siswa_keu_ocb11.kas'

    name = fields.Char(string='Nama', requred=True, default=_('New'))
    tanggal = fields.Date('Tanggal', required=True, default=datetime.today())
    desc = fields.Char('Keterangan')
    jumlah = fields.Float('Jumlah', required=True)
    debet = fields.Float('Debet' )
    kredit = fields.Float('Kredit')    
    pembayaran_id = fields.Many2one('siswa_keu_ocb11.pembayaran', string='Pembayaran', ondelete='cascade')
    is_related = fields.Boolean('Is Related', default=False)
    state = fields.Selection([('draft', 'Draft'), ('post', 'Posted')], string='State', required=True, default='draft')
    is_allow_to_delete = fields.Boolean('Allow to Delete', default=False)
    kas_kategori_id = fields.Many2one('siswa_keu_ocb11.kas_kategori', required=True, string='Akun Kas', ondelete="restrict")

    def reload_page(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_confirm(self):
        self.ensure_one()
        # add related to action_confirm table
        self.env['siswa_keu_ocb11.action_confirm'].create({
            'kas_id' : self.id
        })
        # update state
        self.write({
            'state' : 'post'
        })

        # update keuangan_dashboard
        self.recompute_keuangan_dashboard()

        return self.reload_page()
    
    def action_cancel(self):
        self.ensure_one()
        
        # remove from action_confirm
        self.env['siswa_keu_ocb11.action_confirm'].search([('kas_id','=',self.id)]).unlink()

        # update state
        self.write({
            'state' : 'draft',
            'is_allow_to_delete' : True
        })

        # update keuangan_dashboard
        self.recompute_keuangan_dashboard()

        return self.reload_page()
    
    def recompute_keuangan_dashboard(self):
        # recompute dashboard tagihan siswa
        dash_keuangan_id = self.env['ir.model.data'].search([('name','=','default_dashboard_kas')]).res_id
        dash_keuangan = self.env['siswa_keu_ocb11.keuangan_dashboard'].search([('id','=',dash_keuangan_id)])
        for dash in dash_keuangan:
            dash.compute_kas()        

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('siswa.keu.ocb11.kas') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('siswa.keu.ocb11.kas') or _('New')
        
        # if 'jumlah' in vals:
            # tentukan debet atau kredit
            #
            # if vals['jumlah'] > 0 :
            #     vals['debet'] = vals['jumlah']
            # else:
            #     vals['kredit'] = abs(vals['jumlah'])
        
        # get kas kategori
        kategori_id = self.env['siswa_keu_ocb11.kas_kategori'].search([('id', '=', vals['kas_kategori_id'])])

        if kategori_id.tipe == 'in':
            vals['debet'] = vals['jumlah']
        else:
            vals['kredit'] = abs(vals['jumlah'])

        result = super(kas, self).create(vals)
        return result

    @api.multi
    def unlink(self):
        for rec in self:
            if not rec.is_allow_to_delete:
                raise exceptions.except_orm(_('Warning'), _('You can not delete this type of data.'))
                
        return super(kas, self).unlink()

