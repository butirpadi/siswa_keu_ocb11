from odoo import models, fields, api, _
from pprint import pprint

class wizard_report_pembayaran_siswa(models.TransientModel):
    _name = 'siswa_keu_ocb11.wizard_report_pembayaran_siswa'

    name = fields.Char('Name', default='0')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]), required=True, ondelete="cascade")
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya', required=True)
    rombel_id = fields.Many2one('siswa_ocb11.rombel', string='Rombel', required=True)
    siswa_ids = fields.Many2many('res.partner',relation='wizard_pembayaran_siswa_siswa_rel', column1='report_id',column2='siswa_id', string="Data Siswa")
    pembayaran_ids = fields.Many2many('siswa_keu_ocb11.pembayaran',relation='wizard_pembayaran_siswa_pembayaran_rel', column1='report_id',column2='pembayaran_id', string="Data Pembayaran")

    def action_save(self):
        self.ensure_one()
        # update name
        self.name = "Report Pembayaran Siswa"

        # get data siswa
        rombel_siswa = self.env['siswa_ocb11.rombel_siswa'].search([
            ('tahunajaran_id','=', self.tahunajaran_id.id),
            ('rombel_id','=', self.rombel_id.id),
            ])
            
        for rbs in rombel_siswa:
            self.write({
                'siswa_ids' : [(4,rbs.siswa_id.id)]
            })
        
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'siswa_keu_ocb11.wizard_report_pembayaran_siswa',
            'target': 'current',
            'res_id': self.id,
            'type': 'ir.actions.act_window'
        }