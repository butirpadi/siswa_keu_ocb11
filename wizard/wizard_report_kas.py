from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime

class wizard_report_kas(models.TransientModel):
    _name = 'siswa_keu_ocb11.wizard_report_kas'

    name = fields.Char('Name', default='Report Kas')
    awal = fields.Date('Periode Awal', default=datetime.today(), required=True)
    akhir = fields.Date('Periode Akhir', default=datetime.today(), required=True)
    jenis = fields.Selection([(1, 'All'), (2, 'Pendaptan'), (3, 'Pengeluaran')], string='Jenis Kas', required=True, default=1)
    # kas_ids = fields.Many2many('siswa_keu_ocb11.kas', string='Data Kas')
    kas_ids = fields.Many2many('siswa_keu_ocb11.kas',relation='siswa_keu_ocb11_report_kas_rel', column1='report_id',column2='kas_id', string="Data Kas")
    saldo_begining = fields.Float('Saldo Begining', default=0)
    saldo_ending = fields.Float('Saldo Ending', default=0)
    saldo_current = fields.Float('Saldo Current', default=0)


    def action_save(self):
        self.ensure_one()
        # set kas_ids
        kases = self.env['siswa_keu_ocb11.kas'].search([('tanggal','>=',self.awal),('tanggal','<=',self.akhir)])
        reg_kas = []
        for kas in kases:
            self.write({
                'kas_ids' : [(4,kas.id)]
            })
        kas_before = self.env['siswa_keu_ocb11.kas'].search([('tanggal','<',self.awal)])
        saldo_begining = sum(x.jumlah for x in kas_before)
        
        kas_after = self.env['siswa_keu_ocb11.kas'].search([('tanggal','>',self.akhir)])
        saldo_ending = sum(x.jumlah for x in kas_after)
        
        saldo_current = sum(x.jumlah for x in kases)
        
        self.write({
                'saldo_begining' : saldo_begining,
                'saldo_ending' : saldo_ending,
                'saldo_current' : saldo_current,
            })        
    
    def action_print_kas(self):
        self.action_save()
        return self.env.ref('siswa_keu_ocb11.report_kas_action').report_action(self)
    
    def action_print_rekap(self):
        self.action_save()
        return self.env.ref('siswa_keu_ocb11.report_rekap_kas_action').report_action(self)
        

