# Copyright (c) 2023, Craft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import date,datetime


from erpnext.accounts.report.sales_register.sales_register import get_mode_of_payments


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)

	output = {}

	columns = get_columns(filters)

	data = get_pos_entries(filters)

	return columns,data


def get_pos_entries(filters):
	conditions = get_conditions(filters)

	products,payments,taxes,data = [], [], [], []
	total_qty,total_amnt,total_total,total_base = 0,0,0,0


	products = frappe.db.sql("""
		SELECT CONCAT(tpii.item_code,'|',tpii.item_name) as product,sum(tpii.qty) as quantity,tpii.rate as price_unit FROM `tabPOS Invoice` tpi 
		JOIN `tabPOS Invoice Item` tpii ON tpi.name = tpii.parent 
		WHERE tpi.docstatus = 1 and {conditions}
		GROUP BY tpii.item_code 
		""".format(conditions=conditions),
		filters,
		as_dict=1,)

	if products:
		total_qty = sum(item['quantity'] for item in products)

	data.append({
		'product' : "Products",
		'quantity':total_qty,
		'bold':1
		})
	data+=products

	payments = frappe.db.sql("""
		SELECT tpii.mode_of_payment as product,sum(tpii.base_amount) as quantity, 0 as price_unit FROM `tabPOS Invoice` tpi 
		JOIN `tabSales Invoice Payment` tpii ON tpi.name = tpii.parent 
		WHERE tpi.docstatus = 1 and tpii.base_amount !=0 and {conditions}
		GROUP BY tpii.mode_of_payment  
		""".format(conditions=conditions),
		filters,
		as_dict=1,)

	if payments:
		total_amnt = sum(item['quantity'] for item in payments)

	data.append({
		'product' : "Payments",
		'quantity':total_amnt,
		'bold':1
		})
	data+=payments

	taxes = frappe.db.sql("""
		SELECT tpii.description as product,sum(tpii.total) as quantity,sum(tpii.base_total) as price_unit FROM `tabPOS Invoice` tpi 
		JOIN `tabSales Taxes and Charges` tpii ON tpi.name = tpii.parent 
		WHERE tpi.docstatus = 1 and {conditions}
		GROUP BY tpii.description  
		""".format(conditions=conditions),
		filters,
		as_dict=1,)

	if taxes:
		total_total = sum(item['quantity'] for item in taxes)
		total_base = sum(item['price_unit'] for item in taxes)

	data.append({
		'product' : "Taxes",
		'quantity':total_total,
		'price_unit':total_base,
		'bold':1
		})
	data+=taxes

	data.append([total_amnt])

	data.append([products,payments,taxes])


	return data


def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("{0} is mandatory").format(_("Company")))

	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date must be before To Date"))

	if not filters.get("from_date"):
		frappe.throw(
			_("{0} is mandatory").format(frappe.bold(_("From Date")))
		)
	if not filters.get("to_date"):
		frappe.throw(
			_("{0} is mandatory").format(frappe.bold(_("To Date")))
		)

def get_conditions(filters):

	conditions = (
		"company = %(company)s"
	)

	conditions += " AND CONCAT(posting_date,' ',posting_time) BETWEEN '%s' and '%s'" % (filters.from_date,filters.to_date)

	if filters.get("pos_profile"):
		conditions += " AND pos_profile = %(pos_profile)s"

	if filters.get("customer"):
		conditions += " AND customer = %(customer)s"

	if filters.get("is_return"):
		conditions += " AND is_return = %(is_return)s"

	if filters.get("cashier"):
		conditions += " AND owner = %(cashier)s"

	if filters.get("mode_of_payment"):
		conditions += """
			AND EXISTS(
					SELECT name FROM `tabSales Invoice Payment` sip
					WHERE parent=p.name AND ifnull(sip.mode_of_payment, '') = %(mode_of_payment)s
				)"""
	return conditions


def get_columns(filters):
	columns = [
		{
			"label": _("Product|Mode|Tax"),
			"fieldname": "product",
			"fieldtype": "Data",
			"options": "Item",
			"width": 250,
		},
		{
			"label": _("Quantity|Total|Tax Amount"),
			"fieldname": "quantity",
			"fieldtype": "Float",
			"width": 200,
		},
		{
			"label": _("Price Unit|Base Amount"),
			"fieldname": "price_unit",
			"fieldtype": "Currency",
			"options": "company:currency",
			"width": 200,
		}
	]

	return columns

