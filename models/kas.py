# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.addons import decimal_precision as dp
from datetime import datetime

class kas(models.Model):
    _name = 'siswa_keu_ocb11.kas'

    name = fields.Char(string='Nama', requred=True, default=_('New'))
    tanggal = fields.Date('Tanggal', required=True, default=datetime.today())
    desc = fields.Char('Keterangan', require=True)
    jumlah = fields.Float('Jumlah', required=True)
    debet = fields.Float('Debet' )
    kredit = fields.Float('Kredit')    
    pembayaran_id = fields.Many2one('siswa_keu_ocb11.pembayaran', string='Pembayaran', ondelete='restrict')
    is_related = fields.Boolean('Is Related', default=False)
    state = fields.Selection([('draft', 'Draft'), ('post', 'Posted')], string='State', required=True, default='draft')

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

        return self.reload_page()
    
    def action_cancel(self):
        self.ensure_one()
        # remove from action_confirm
        self.env['siswa_keu_ocb11.action_confirm'].search([('kas_id','=',self.id)]).unlink()
        # update state
        self.write({
            'state' : 'draft'
        })

        return self.reload_page()

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('siswa.keu.ocb11.kas') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('siswa.keu.ocb11.kas') or _('New')
        
        if 'jumlah' in vals:
            if vals['jumlah'] > 0 :
                vals['debet'] = vals['jumlah']
            else:
                vals['kredit'] = abs(vals['jumlah'])

        result = super(kas, self).create(vals)
        return result

    @api.multi
    def unlink(self):
        if self.is_related or self.pembayaran_id:
            raise exceptions.except_orm(_('Warning'), _('You can not delete this type of data.'))
        return super(kas, self).unlink()

