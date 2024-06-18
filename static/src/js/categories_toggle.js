odoo.define('website_modifications.categories_toggle', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    publicWidget.registry.categoryToggle = publicWidget.Widget.extend({
        selector: '.toggle-button',
        events: {
            'click': '_onClickToggle',
        },
        start: function () {
            this._updateButtonVisibility();
            return this._super.apply(this, arguments);
        },
        _updateButtonVisibility: function () {
            var parentLi = this.$el.closest('li.parent_category');
            var buttonCategoryParent = this.$el.closest('button.btn_category_parent');
            var childrenLi = this.$el.closest('li.child_category');
            var buttonSubCategory = this.$el.closest('button.btn_subcategories');

            var hasChildCategory = parentLi.find('.child_category').length > 0;
            var hasGrandchildCategory = childrenLi.find('.grandchild_category').length > 0;

            buttonCategoryParent.toggle(hasChildCategory);
            buttonSubCategory.toggle(hasGrandchildCategory);
        },
        _toggleCategories: function (categorySelector) {
            var parentLi = this.$el.closest('li.parent_category');
            var categories = parentLi.find(categorySelector);

            if (categories.length > 0) {
                categories.toggleClass('hidden');
            }
        },
        _showChildCategories: function () {
            this._toggleCategories('.subcategories');
        },

        _showGrandchildCategories: function () {
            this._toggleCategories('.sub_subcategories');
        },
        _onClickToggle: function () {
            if (this.$el.hasClass('btn_subcategories')) {
                this._showGrandchildCategories();
            } else if (this.$el.hasClass('btn_category_parent')) {
                this._showChildCategories();
            }
            this._updateButtonVisibility();
        },
    });
});