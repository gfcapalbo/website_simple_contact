from openerp.osv import fields, osv
from openerp.tools.translate import _

class crm_lead(osv.osv):
	_inherit = "crm.lead"
	_name = "crm.lead"

	_columns = {
		'survey_id': fields.many2one('survey.survey', "Survey"),
		'response_id': fields.many2one('survey.user_input', ondelete='set null', oldname="response"),
		}

	def action_print_survey(self, cr, uid, ids, context=None):
		context = dict(context or {})
		lead = self.browse(cr, uid, ids, context=context)[0]
		survey_obj = self.pool.get('survey.survey')
		response_obj = self.pool.get('survey.user_input')
		
		if not lead.survey_id.id:
			return survey_obj.action_print_survey(cr, uid, [lead.survey_id.id], context=context)
		else:
			response = response_obj.browse(cr, uid, lead.response_id.id, context=context)
			context.update({'survey_token': response.token})
			return survey_obj.action_print_survey(cr, uid, [lead.survey_id.id], context=context)