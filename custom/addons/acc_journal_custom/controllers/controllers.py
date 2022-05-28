# -*- coding: utf-8 -*-
# from odoo import http


# class AccountJournal(http.Controller):
#     @http.route('/account_journal/account_journal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_journal/account_journal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_journal.listing', {
#             'root': '/account_journal/account_journal',
#             'objects': http.request.env['account_journal.account_journal'].search([]),
#         })

#     @http.route('/account_journal/account_journal/objects/<model("account_journal.account_journal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_journal.object', {
#             'object': obj
#         })
