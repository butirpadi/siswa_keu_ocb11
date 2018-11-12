# -*- coding: utf-8 -*-

from flectra import models, fields, api, exceptions, _
from flectra.addons import decimal_precision as dp
from datetime import datetime
from pprint import pprint

class keuangan_dashboard_tahunajaran_rel(models.Model):
    _name = 'siswa_keu_ocb11.keuangan_dashboard_tahunajaran_rel'

    dashboard_id = fields.Many2one('siswa_keu_ocb11.keuangan_dashboard')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran')
    amount_due = fields.Float('Amount Due') 