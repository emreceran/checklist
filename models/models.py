# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ManufacturingChecklist(models.Model):
    _name = "manufacturing.checklist"
    _description = "Manufacturing Custom checklist"

    sequence = fields.Integer(string="Sıra")
    name = fields.Char(string="Ad")
    description = fields.Char(string="Açıklama")


class ManufacturingChecklistLine(models.Model):
    _name = "manufacturing.checklist.line"
    _description = "MRP Custom checklist Line"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(string="Sıra")
    name = fields.Char(string="Ad")
    checklist_id = fields.Many2one('manufacturing.checklist', string="Ad")
    mrp_id = fields.Many2one("mrp.production", string="Üretim Emri")
    description = fields.Char(string="Açıklama")
    date = fields.Date(default=fields.Date.today, string="Tarih")
    date_finished = fields.Date(string="Onay Tarihi", readonly=True, tracking=True)
    state = fields.Selection([
        ('new', 'Yeni'),
        ('complete', 'Tamamlandı'),
        ('cancel', 'İptal')], string='Durum', tracking=True,
        copy=False, default="new")

    @api.onchange('checklist_id')
    def _onchange_checklist_id(self):
        for checklist in self:
            description = ''
            if checklist.checklist_id:
                description = checklist.checklist_id.description
            checklist.update({
                'description': description
            })

    def action_complete(self):
        completion_time = fields.Datetime.now()
        user_name = self.env.user.name
        for rec in self:
            rec.state = 'complete'
            satir_ismi = rec.checklist_id.name
            rec.date_finished = completion_time
            checklist_len = len(rec.mrp_id.checklist_line_ids)
            completed_progress = len(rec.mrp_id.checklist_line_ids.filtered(lambda x: x.state == 'complete'))
            rec.mrp_id.write({
                'checklist_progress': (completed_progress * 100) / (checklist_len or 1)
            })

            # Chatter'a mesaj gönder
            # _() fonksiyonu ile mesajı çevrilebilir hale getirebiliriz
            message_body = _(" %s Kalite kontrolü %s tarafından  %s tarihinde onaylandı.") % (satir_ismi, user_name, fields.Datetime.to_string(completion_time))
            rec.mrp_id.message_post(body=message_body)

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
            checklist_len = len(rec.mrp_id.checklist_line_ids)
            completed_progress = len(rec.mrp_id.checklist_line_ids.filtered(lambda x: x.state == 'complete'))
            rec.mrp_id.write({
                'checklist_progress': (completed_progress * 100) / (checklist_len or 1)
            })


class ManufacturingChecklistTemplate(models.Model):
    _name = "manufacturing.checklist.template"
    _description = "Manufacturing Custom Checklist Template"
    _rec_name = "template_name"

    sequence = fields.Integer(string="Sıra")
    template_name = fields.Char(string="Ad")
    checklist_ids = fields.Many2many('manufacturing.checklist', string="Kalite Kontrol Soruları")


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    checklist_progress = fields.Integer(string='Kalite Kontrol İlerlemesi', store=True, default=0)
    checklist_template = fields.Many2many('manufacturing.checklist.template', string='Kalite Kontrol Listeleri')
    checklist_line_ids = fields.One2many('manufacturing.checklist.line', 'mrp_id', string='Kalite Kontrol')

    @api.onchange('checklist_template')
    def onchange_checklist_template(self):

        if self.checklist_template:
            custom_checklist = []
            for template in self.checklist_template:
                for checklist in template.checklist_ids:
                    custom_checklist.append((0, 0, {
                        'checklist_id': checklist._origin.id,
                        'description': checklist.description,
                        'mrp_id': self.id,
                    }))
                    self.update({'checklist_line_ids': False})
            self.update({"checklist_line_ids": custom_checklist})
        else:
            self.update({'checklist_line_ids': False})
