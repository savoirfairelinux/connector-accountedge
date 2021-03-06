# -*- encoding: utf-8 -*-
##############################################################################
#····
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.·····
#
##############################################################################

from osv import osv, fields

class hr_expense_line(osv.osv):
    _inherit = 'hr.expense.line'
    _columns = {
        'sequence': fields.integer('N°', required=True),
    }
    _defaults = {
        'sequence': lambda obj, cr, uid, context:0
    }

    def update_sequences(self, cr, uid, expense, context=None):
        ''' Updating the sequences (line numbers) of an hr.expense
            object. '''
        num = 0
        for l in expense.line_ids:
            num = num + 1
            self.write(cr, uid, l.id, {'sequence':num})

    def unlink(self, cr, uid, ids, context=None):
        ''' Overwriting the unlink() method
            to update the line numbers of the expense
            the expense lines belong to'''
        for id in ids:
            expense = self.pool.get('hr.expense.line').browse(cr, uid, id).expense_id
            ret     = super(hr_expense_line,self).unlink(cr, uid, ids, context)
            self.update_sequences(cr, uid, expense, context)
        return ret

    def create(self, cr, user, vals, context=None):
        ''' Overwriting the create() method
            to update the line numbers of the expense
            the expense line belongs to'''
        ret = super(hr_expense_line,self).create(cr, user, vals, context)

        if ('sequence' not in vals) or (vals.get('sequence')==0):
            expense = self.pool.get('hr.expense.expense').browse(cr, user, vals['expense_id'])
            self.update_sequences(cr, user, expense, context)
        return ret

hr_expense_line()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
