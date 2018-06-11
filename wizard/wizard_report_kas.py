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
    tipe = fields.Selection([('sum', 'Summary'), ('det', 'Detail')], required=True, default='sum')


    def action_save(self):
        self.ensure_one()

        # if self.tipe == 'det':
            # set kas_ids
        kases = self.env['siswa_keu_ocb11.kas'].search([('tanggal','>=',self.awal),('tanggal','<=',self.akhir)])
        reg_kas = []
        for kas in kases:
            self.write({
                'kas_ids' : [(4,kas.id)]
            })
        kas_before = self.env['siswa_keu_ocb11.kas'].search([('tanggal','<',self.awal)])
        saldo_begining = sum(x.jumlah for x in kas_before)

        # saldo begining wth cr execute
        self.env.cr.execute("select coalesce(sum(debet),0) - coalesce(sum(kredit),0) \
                from siswa_keu_ocb11_kas \
                where tanggal < '%s'" % self.awal)
        saldo_begining = self.env.cr.fetchone()[0]
        
        kas_after = self.env['siswa_keu_ocb11.kas'].search([('tanggal','>',self.akhir)])
        saldo_ending = sum(x.jumlah for x in kas_after)
        
        saldo_current = sum(x.jumlah for x in kases)
        
        self.write({
                'saldo_begining' : saldo_begining,
                'saldo_ending' : saldo_ending,
                'saldo_current' : saldo_current,
            })     
        # else : 
        #     self.env.cr.execute("select distinct on (kas_kategori_id) \
	    #         *, (select sum(cld.jumlah) from siswa_keu_ocb11_kas cld \
		#         where kas_kategori_id = pr.kas_kategori_id \
		#         and cld.tanggal >= '" + str(self.awal) + "' \
		#         and cld.tanggal <= '" + str(self.akhir) + "' ) as total_jumlah \
        #         from siswa_keu_ocb11_kas as pr \
        #         where tanggal >= '" + str(self.awal) + "' and tanggal <= '" + str(self.akhir) + "'")
        #     sum_kas = self.env.cr.fetchall()

        #     pprint(sum_kas)

    
    def get_summary_data(self):
        self.env.cr.execute("select distinct on (kas_kategori_id) \
	            kas_kategori_id, kat.name as kategori, kat.tipe, (select sum(cld.jumlah) from siswa_keu_ocb11_kas cld \
		        where kas_kategori_id = pr.kas_kategori_id \
		        and cld.tanggal >= '" + str(self.awal) + "' \
		        and cld.tanggal <= '" + str(self.akhir) + "' ) as total_jumlah \
                from siswa_keu_ocb11_kas as pr \
                join siswa_keu_ocb11_kas_kategori as kat on pr.kas_kategori_id = kat.id \
                where tanggal >= '" + str(self.awal) + "' and tanggal <= '" + str(self.akhir) + "'")
        sum_kas = self.env.cr.fetchall()
        # print('Loop on get summary data')
        # for sk in sum_kas:
        #     pprint(sk['total_jumlah'])

        return sum_kas
    
    def get_summary_pendapatan(self):
        self.env.cr.execute("select distinct on (kas_kategori_id) \
	            kas_kategori_id, kat.name as kategori, kat.tipe, (select sum(cld.jumlah) from siswa_keu_ocb11_kas cld \
		        where kas_kategori_id = pr.kas_kategori_id \
		        and cld.tanggal >= '" + str(self.awal) + "' \
		        and cld.tanggal <= '" + str(self.akhir) + "' ) as total_jumlah, \
                tanggal \
                from siswa_keu_ocb11_kas as pr \
                join siswa_keu_ocb11_kas_kategori as kat on pr.kas_kategori_id = kat.id \
                where kat.tipe = 'in' and \
                tanggal >= '" + str(self.awal) + "' and tanggal <= '" + str(self.akhir) + "'")
        sum_pendapatan = self.env.cr.fetchall()

        return sum_pendapatan
    
    def get_summary_pengeluaran(self):
        self.env.cr.execute("select distinct on (kas_kategori_id) \
	            kas_kategori_id, kat.name as kategori, kat.tipe, (select sum(cld.jumlah) from siswa_keu_ocb11_kas cld \
		        where kas_kategori_id = pr.kas_kategori_id \
		        and cld.tanggal >= '" + str(self.awal) + "' \
		        and cld.tanggal <= '" + str(self.akhir) + "' ) as total_jumlah \
                from siswa_keu_ocb11_kas as pr \
                join siswa_keu_ocb11_kas_kategori as kat on pr.kas_kategori_id = kat.id \
                where kat.tipe = 'out' and \
                tanggal >= '" + str(self.awal) + "' and tanggal <= '" + str(self.akhir) + "'")
        sum_pengeluaran = self.env.cr.fetchall()

        return sum_pengeluaran

    def action_print_kas(self):
        self.action_save()
        return self.env.ref('siswa_keu_ocb11.report_kas_action').report_action(self)
    
    def action_print_rekap(self):
        self.action_save()

        if self.tipe == 'sum' : 
            return self.env.ref('siswa_keu_ocb11.report_rekap_kas_summary_action').report_action(self)
        else:
            return self.env.ref('siswa_keu_ocb11.report_rekap_kas_action').report_action(self)
        

