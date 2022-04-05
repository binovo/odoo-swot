odoo.define('swot_group.update_kanban', function (require) {
'use strict';

var core = require('web.core');
var Dialog = require('web.Dialog');
var KanbanRecord = require('web.KanbanRecord');

var QWeb = core.qweb;
var _t = core._t;

KanbanRecord.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     * @private
     */
    _openRecord: function () {
        if (this.modelName === 'swot.group' && this.$(".o_swot_group_kanban_boxes a").length) {
            this.$('.o_swot_group_kanban_boxes a').first().click();
        } else {
            this._super.apply(this, arguments);
        }
    },

});
});
