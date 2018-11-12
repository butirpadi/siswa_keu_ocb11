# -*- coding: utf-8 -*-

from flectra import models, fields, api, _

class tahunajaran(models.Model):
	_inherit = 'siswa_ocb11.tahunajaran'
	
	# biayas = fields.One2many('siswa_keu_ocb11.tahunajaran_biaya', inverse_name='tahunajaran_id' , string='Biaya-biaya')
	jenjangs = fields.One2many('siswa_keu_ocb11.tahunajaran_jenjang', inverse_name='tahunajaran_id' , string='Jenjang', ondelete='cascade')
	
	@api.model
	def create(self, vals):
		result = super(tahunajaran, self).create(vals)
	# 	# auto generate tahunajaran_jenjang
		print(str(result.name) + ' PG')
		self.env['siswa_keu_ocb11.tahunajaran_jenjang'].create({
			'name' : str(result.name) + ' PG',
			'tahunajaran_id' : result.id,
			'jenjang' : 0
		})
		print(str(result.name) + ' TK A')
		self.env['siswa_keu_ocb11.tahunajaran_jenjang'].create({
			'name' : str(result.name) + ' TK A',
			'tahunajaran_id' : result.id,
			'jenjang' : 1
		})
		print(str(result.name) + ' TK B')
		self.env['siswa_keu_ocb11.tahunajaran_jenjang'].create({
			'name' : str(result.name) + ' TK B',
			'tahunajaran_id' : result.id,
			'jenjang' : 2
		})
		return result 