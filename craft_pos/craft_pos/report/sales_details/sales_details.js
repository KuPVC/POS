// Copyright (c) 2023, Craft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Details"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.now_datetime(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"pos_profile",
			"label": __("POS Profile"),
			"fieldtype": "Link",
			"options": "POS Profile"
		},
		{
			"fieldname":"cashier",
			"label": __("Cashier"),
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"mode_of_payment",
			"label": __("Payment Method"),
			"fieldtype": "Link",
			"options": "Mode of Payment"
		},
		{
			"fieldname":"is_return",
			"label": __("Is Return"),
			"fieldtype": "Check"
		},
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.bold) {
			value = value.bold();

		}
		return value;
	}
};
