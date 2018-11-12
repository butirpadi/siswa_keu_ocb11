from flectra import models, fields, api, _
from pprint import pprint

class wizard_keuangan_siswa(models.TransientModel):
    _name = 'siswa_keu_ocb11.wizard_keuangan_siswa'

    name = fields.Char('Name', default='0')
    siswa_id = fields.Many2one('res.partner', string="Siswa", domain=[('is_siswa','=',True)], required=True, ondelete="cascade")
    induk = fields.Char('Nomor Induk', related='siswa_id.induk')
    rombel_id = fields.Many2one('siswa_ocb11.rombel', string='Rombongan Belajar', compute='_compute_rombel_siswa', ondelete="cascade")
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]), required=True, ondelete="cascade")
    biayas = fields.One2many('siswa_keu_ocb11.siswa_biaya', related='siswa_id.biayas', string='Biaya-biaya', compute='_compute_biaya' ) 
    biayas_paid = fields.One2many('siswa_keu_ocb11.siswa_biaya',  string='Biaya Paid', compute='_compute_biaya') 
    biayas_open = fields.One2many('siswa_keu_ocb11.siswa_biaya',  string='Biaya Open', compute='_compute_biaya' ) 
    
    # # @api.depends('siswa_id','tahunajaran_id')
    # def _compute_siswa_biaya(self):
    #     self.ensure_one()
    #     print('inside compute_siswa_biaya')
    #     # paid_biayas = self.env['siswa_keu_ocb11.siswa_biaya'].search([('siswa_id','=',self.siswa_id.id),('state','=','open')])
    #     # for biy in paid_biayas:
    #     #     print(biy.biaya_id.name)
    
    @api.depends('siswa_id','tahunajaran_id')
    def _compute_biaya(self):
        self.ensure_one()
        # self.biayas = self.siswa_id.biayas.search([('tahunajaran_id','=',self.tahunajaran_id.id)])
        self.biayas_open = self.env['siswa_keu_ocb11.siswa_biaya'].search([('siswa_id','=',self.siswa_id.id),('state','=','open')])
        # self.biayas_paid = self.env['siswa_keu_ocb11.siswa_biaya'].search([('siswa_id','=',self.siswa_id.id),('state','=','paid')])
        # self.biayas_paid = self.env['siswa_keu_ocb11.siswa_biaya'].search([('siswa_id','=',self.siswa_id.id),('amount_due','<',harga)])
        self._get_paid_siswa_biaya()
    
    def _get_paid_siswa_biaya(self):
        print('inside _get_paid_siswa_biaya')
        # query = "select * from siswa_keu_ocb11_siswa_biaya where siswa_id=%d and amount_due < harga " % self.siswa_id.id
        if self.siswa_id.id:
            query = "select * from siswa_keu_ocb11_siswa_biaya where siswa_id=" + str(self.siswa_id.id) + " and amount_due < harga"
            self.env.cr.execute(query)
            siswa_biaya = self.env.cr.fetchall()
            biaya_ids = []
            if siswa_biaya:
                for sis in siswa_biaya:
                    biaya_ids.append(sis[0])
                self.biayas_paid = self.env['siswa_keu_ocb11.siswa_biaya'].search([('id','in',biaya_ids)])            


    @api.depends('siswa_id','tahunajaran_id')
    def _compute_rombel_siswa(self):
        for rec in self:
            print('inside comnpute rombel siswa')
            rombel = self.env['siswa_ocb11.rombel_siswa'].search([('tahunajaran_id','=',rec.tahunajaran_id.id),('siswa_id','=',rec.siswa_id.id)]).rombel_id
            rec.rombel_id = rombel.id
            # rec.biayas = filter(lambda x: x.tahunajaran_id == rec.tahunajaran_id.id ,rec.biayas)
            
    @api.multi 
    def action_save(self):
        self.ensure_one()
        print('Inside Action Save Wizard Keuangan Siswa')
        # update name
        self.write({
            'name' : 'Tagihan Siswa'
        })
        # self.ensure_one()
        # print(self.siswa_id.id)
        # print(self.tahunajaran_id.id)
        # self.biayas = self.siswa_id.biayas.search([('siswa_id','=',self.siswa_id.id),('tahunajaran_id','=',self.tahunajaran_id.id)])
        
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'siswa_keu_ocb11.wizard_keuangan_siswa',
            'target': 'current',
            'res_id': self.id,
            # 'domain' : [('wizard_stock_on_hand_id','=',self.id)],
            # 'context' : {'search_default_group_location_id':1,'search_default_group_product_id':1},
            # 'context' : ctx,
            'type': 'ir.actions.act_window'
        }
