from flectra import models, fields, api
from pprint import pprint
from datetime import datetime

class non_aktif(models.TransientModel):
    _inherit = 'siswa_ocb11.non_aktif'

    @api.multi
    def action_save(self):
        res = super(non_aktif,self).action_save()
        # ketika siswa di non aktifkan maka non aktifkan semua siswa_biaya nya
        print('inside non aktif on keuangan module')
        print('set siswa biaya to active = false')
        self.env['siswa_keu_ocb11.siswa_biaya'].search([
                ('siswa_id','=',self.siswa_id.id),
                ('state','=','open'),
            ]).write({
                'active' : False
            })
        
        # recalculate keuangan dashboard
        dash_keuangan_id = self.env['ir.model.data'].search([('name','=','default_dashboard_pembayaran')]).res_id
        dash_keuangan = self.env['siswa_keu_ocb11.keuangan_dashboard'].search([('id','=',dash_keuangan_id)])
        for dash in dash_keuangan:
            dash.compute_keuangan()    

        return res 