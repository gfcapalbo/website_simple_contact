(function () {
	'use strict';

	var website = openerp.website;

	website.snippet.animationRegistry.simple_contact_click = website.snippet.Animation.extend({
		selector: ".js_simple_contact",
		
		on_click : function () {
			var self = this;
			
			//reads out form
			var $email = this.$target.find(".js_lead_email");
			var $name = this.$target.find(".js_lead_name");
			var survey_id = this.$target.attr("data-id");
			console.log($name.val());
			
			//validates email address
			if ($name.val() == "" || !$email.val().match(/.+@.+/)) {
				this.$target.addClass('has-error');
				return false;
			}
			this.$target.removeClass('has-error');

			//creates lead and redicts to survey
			openerp.jsonRpc('/simplecontact/confirm', 'call', {
				'lead_email': $email.length ? $email.val() : false,
				'lead_name': $name.length ? $name.val(): false,
				'survey_id': survey_id.length ? survey_id : false,
			}).done(function(result) {
					openerp.jsonRpc('/simplecontact/action_create_token', 'call', {
						'lead_new' : result,
						'survey_id' : survey_id.length ? survey_id : false,
					}).done(function(url) {
						window.open(url,"_self");
					})
				});

		},


		start : function () {
			//binds button to function
			var self = this;
			this.$target.find(".js_simple_contact_btn").on("click", _.bind(this.on_click, this));
			this._super();
		},
		
	});

	
})();