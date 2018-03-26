# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class tahunajaran(models.Model):
	_inherit = 'siswa_ocb11.tahunajaran'
	
	# biayas = fields.One2many('siswa_keu_ocb11.tahunajaran_biaya', inverse_name='tahunajaran_id' , string='Biaya-biaya')
	jenjangs = fields.One2many('siswa_keu_ocb11.tahunajaran_jenjang', inverse_name='tahunajaran_id' , string='Jenjang')
	
	@api.model
	def create(self, vals):
		result = super(tahunajaran, self).create(vals)
	# 	# auto generate tahunajaran_jenjang
		self.env['siswa_keu_ocb11.tahunajaran_jenjang'].create({
			'tahunajaran_id' : result.id,
			'jenjang' : 0
		})
		self.env['siswa_keu_ocb11.tahunajaran_jenjang'].create({
			'tahunajaran_id' : result.id,
			'jenjang' : 1
		})
		self.env['siswa_keu_ocb11.tahunajaran_jenjang'].create({
			'tahunajaran_id' : result.id,
			'jenjang' : 2
		})
		return result