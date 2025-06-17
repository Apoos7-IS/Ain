from odoo import models, fields, api

class Students(models.Model):
    _name = 'students'

    name = fields.Char(string="Name")
    phone = fields.Char(string="Phone")
    registration = fields.Char(string="Registration")
    level = fields.Char(string="Level")
    major = fields.Char(string="Major")
    collage = fields.Char(string="Collage")