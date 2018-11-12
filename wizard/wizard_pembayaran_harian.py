from flectra import models, fields, api, _
from pprint import pprint
from datetime import datetime

class wizard_pembayaran_harian(models.TransientModel):
    _name = 'siswa_keu_ocb11.wizard_pembayaran_harian'
    
    name = fields.Char('Nama', default="0")
    awal = fields.Date('Periode Awal', default=datetime.today(), required=True)
    akhir = fields.Date('Periode Akhir', default=datetime.today(), required=True)
    pembayaran_ids = fields.Many2many('siswa_keu_ocb11.pembayaran',relation='wizard_pembayaran_harian_rel', column1='report_id',column2='pembayaran_id', string="Data Pembayaran")
    tipe = fields.Selection([('sum', 'Summary'), ('det', 'Detail')], required=True, default='sum')

    def action_save(self):
        self.name = "Report Pembayaran Harian"

        # get data pembayaran
        pb_ids = self.env['siswa_keu_ocb11.pembayaran'].search([
            ('tanggal', '>=', self.awal),
            ('tanggal', '<=', self.akhir),
        ])

        reg_pb = []
        for pb in pb_ids:
            reg_pb.append([(4, pb.id)])
            self.write({
                'pembayaran_ids' : [(4, pb.id)]
            })
        
        # pprint(reg_pb)

        self.write({
            'pembayaran_ids' : reg_pb
        })

        return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'siswa_keu_ocb11.wizard_pembayaran_harian',
                'target': 'current',
                'res_id': self.id,
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('siswa_keu_ocb11.wizard_pembayaran_harian_form').id,
            }

    def action_print(self):
        self.action_save()
        
        if self.tipe == 'sum' : 
            return self.env.ref('siswa_keu_ocb11.report_pembayaran_harian_action').report_action(self)
        else:
            return self.env.ref('siswa_keu_ocb11.report_pembayaran_harian_detail_action').report_action(self) 