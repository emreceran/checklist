from odoo import models

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _split_production_order(self, qty):
        new_productions = super()._split_production_order(qty)
        for prod in new_productions:
            if self.checklist_id:
                prod.checklist_id = self.checklist_id.id
                new_lines = []
                for line in self.checklist_line_ids:
                    new_lines.append((0, 0, {
                        'name': line.name,
                        'sequence': line.sequence,
                        'required': line.required,
                        'completed': False,
                    }))
                prod.checklist_line_ids = new_lines
            print("merhaba")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
            print("*")
        return new_productions

    