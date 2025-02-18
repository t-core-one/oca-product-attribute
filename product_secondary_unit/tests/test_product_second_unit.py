# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProductSecondaryUnit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.product_uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.product_uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product = cls.env["product.template"].create(
            {
                "name": "test",
                "uom_id": cls.product_uom_kg.id,
                "uom_po_id": cls.product_uom_kg.id,
                "secondary_uom_ids": [
                    (
                        0,
                        0,
                        {
                            "code": "A",
                            "name": "unit-700",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 0.7,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "code": "B",
                            "name": "unit-900",
                            "uom_id": cls.product_uom_unit.id,
                            "factor": 0.9,
                        },
                    ),
                ],
            }
        )
        cls.secondary_unit = cls.env["product.secondary.unit"].search(
            [("product_tmpl_id", "=", cls.product.id)], limit=1
        )

    def test_product_secondary_unit_name(self):
        self.assertEqual(self.secondary_unit.name_get()[0][1], "unit-700-0.7")

    def test_product_secondary_unit_search(self):
        args = [
            (
                "product_tmpl_id.product_variant_ids",
                "in",
                self.product.product_variant_ids.ids,
            )
        ]
        name_get = self.env["product.secondary.unit"].name_search(name="A", args=args)
        self.assertEqual(len(name_get), 1)
        name_get = self.env["product.secondary.unit"].name_search(name="X", args=args)
        self.assertEqual(len(name_get), 0)
