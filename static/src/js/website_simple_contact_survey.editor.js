(function () {
    'use strict';

    var website = openerp.website;
    var _t = openerp._t;

    website.snippet.options.simple_contact_snippet = website.snippet.Option.extend({
        on_prompt: function () {
            var self = this;
            return website.prompt({
                id: "simple_contact_survey",
                window_title: _t("Add a Survey"),
                select: _t("Survey List"),
                init: function (field) {
                    return website.session.model('survey.survey')
                            .call('name_search', ['',[['auth_required','!=','True'],['stage_id.id','!=','3']]], { context: website.get_context() });
                },
            }).then(function (survey_id) {
                self.$target.attr("data-id", survey_id);
                console.log(survey_id);
            });
        },
        drop_and_build_snippet: function() {
            var self = this;
            this._super();
            this.on_prompt().fail(function () {
                self.editor.on_remove();
            });
        },
        start : function () {
            var self = this;
            this.$el.find(".js_simple_contact_survey").on("click", _.bind(this.on_prompt, this));
            this._super();
        },
        
    });
})();
