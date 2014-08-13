from openerp import SUPERUSER_ID
from openerp.addons.web import http
from openerp.addons.web.http import request


class SimpleContact(http.Controller):

	@http.route(['/simplecontact/confirm'], type='json', auth="public", website=True)
	def simple_contact_confirm(self,lead_email = None, lead_name= None, survey_id= None, **post):
		cr, uid, context = request.cr, SUPERUSER_ID, request.context
		survey_obj = request.registry.get("survey.survey")

		survey_name = survey_obj.browse(cr, uid,[int(survey_id)], context=context).display_name
		survey_link = survey_obj.browse(cr, uid,[int(survey_id)],context=context).public_url
		
		#prepares fields of new lead
		post = {
			'description' : "",
			'email_from' : lead_email,
			'name' : survey_name + " from " + lead_name,
			'contact_name' : lead_name,
		}

		#prepares description of new lead
		environ = request.httprequest.headers.environ
		post['description'] = "%s\n-----------------------------\nIP: %s\nUSER_AGENT: %s\nACCEPT_LANGUAGE: %s\nREFERER: %s" % (
			post['description'],
			environ.get("REMOTE_ADDR"),
			environ.get("HTTP_USER_AGENT"),
			environ.get("HTTP_ACCEPT_LANGUAGE"),
			environ.get("HTTP_REFERER"))

		lead_new = request.registry['crm.lead'].create(request.cr, SUPERUSER_ID, post, request.context)
		#returns lead id
		return lead_new

	@http.route(['/simplecontact/action_create_token'], type='json', auth="public", website=True)
	def action_create_token(self,lead_new= None, survey_id = None):
		cr, uid, context = request.cr, SUPERUSER_ID, request.context
		survey_obj = request.registry.get('survey.survey')
		lead_obj = request.registry.get('crm.lead')
		response_obj = request.registry.get('survey.user_input')

		#Creates unique link to leads survey
		response_id = response_obj.create(cr, request.uid, {'survey_id': survey_id}, context=context)
		response = response_obj.browse(cr, request.uid, [response_id], context=context)[0]
		trail = "/" + response.token
		url = survey_obj.browse(cr, request.uid,[int(survey_id[0])],context=context).public_url + trail
		
		#adds matching survey to new lead
		data = {
			'response_id': response_id,
			'survey_id': survey_id,
		}

		lead_obj.write(cr, uid, [int(lead_new)], data)
		return  url
		