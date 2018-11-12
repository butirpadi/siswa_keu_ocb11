from flectra import models, fields, api, _
from pprint import pprint
from datetime import datetime

class wizard_rekap_kas(models.TransientModel):
    _name = 'siswa_keu_ocb11.wizard_rekap_kas'

    name = fields.Char('Name', default='Rekapitulasi Kas')
    awal = fields.Date('Periode Awal', default=datetime.today(), required=True)
    akhir = fields.Date('Periode Akhir', default=datetime.today(), required=True)
    jenis = fields.Selection([(1, 'All'), (2, 'Pendaptan'), (3, 'Pengeluaran')], string='Jenis Kas', required=True, default=1)
    # kas_ids = fields.Many2many('siswa_keu_ocb11.kas', string='Data Kas')
    kas_ids = fields.Many2many('siswa_keu_ocb11.kas',relation='siswa_keu_ocb11_rekapitulasi_kas_rel', column1='report_id',column2='kas_id', string="Data Kas")
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

        print('saldo begining  : ' + str(saldo_begining))
        print('saldo current  : ' + str(saldo_current))
        print('saldo ending  : ' + str(saldo_ending))
        
        return self.env.ref('siswa_keu_ocb11.report_kas_action').report_action(self)

