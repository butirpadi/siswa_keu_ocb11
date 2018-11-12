from flectra import models, fields, api, _
from pprint import pprint

class wizard_batch_create_potongan(models.Model):
    _name = 'siswa_wizard_batch_create_potongan'

    name = fields.Char('Name', default='0')
    my_siswa_id = fields.Many2one('res.partner', string="Siswa", domain=[('is_siswa','=',True)], required=True, ondelete="cascade")
    potongan_ids = fields.One2many('siswa_wizard_batch_create_potongan_rel', string="Data Potongan", inverse_name="wizard_id")
    # potongan_ids = fields.Many2many('siswa.potongan_biaya',relation='siswa_wizard_batch_create_potongan_biaya_rel', 
    #                                 column1='wizard_id',column2='potongan_id', string="Data Potongan")
                
    @api.multi 
    def action_save(self):
        for rec in self:
            for potongan in rec.potongan_ids:
                # create potongan
                new_potongan = self.env['siswa.potongan_biaya'].create({
                    'siswa_id' : self.my_siswa_id.id,
                    'siswa_biaya_id' : potongan.siswa_biaya_id.id,
                    'jumlah_potongan' : potongan.jumlah_potongan,
                })
                new_potongan.action_confirm()
        
        return {
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'siswa.potongan_biaya',
            'target': 'current',
            # 'res_id': self.id,
            # 'domain' : [('wizard_stock_on_hand_id','=',self.id)],
            # 'context' : {'search_default_group_location_id':1,'search_default_group_product_id':1},
            # 'context' : ctx,
            'type': 'ir.actions.act_window'
        }
        
    #     self.ensure_one()
    #     print('Inside Action Save Wizard Keuangan Siswa')
    #     # update name
    #     self.write({
    #         'name' : 'Tagihan Siswa'
    #     })
    #     # self.ensure_one()
    #     # print(self.siswa_id.id)
    #     # print(self.tahunajaran_id.id)
    #     # self.biayas = self.siswa_id.biayas.search([('siswa_id','=',self.siswa_id.id),('tahunajaran_id','=',self.tahunajaran_id.id)])
        
    #     return {
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'siswa_keu_ocb11.wizard_keuangan_siswa',
    #         'target': 'current',
    #         'res_id': self.id,
    #         # 'domain' : [('wizard_stock_on_hand_id','=',self.id)],
    #         # 'context' : {'search_default_group_location_id':1,'search_default_group_product_id':1},
    #         # 'context' : ctx,
    #         'type': 'ir.actions.act_window'
    #     }
