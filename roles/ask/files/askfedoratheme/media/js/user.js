var setup_inbox = function(){
    var page = $('.inbox-forum');
    if (page.length) {
        var clearNotifs = $('.clear-messages');
        if (clearNotifs.length) {
            var inbox = new ResponseNotifs();
            inbox.decorate(clearNotifs);
        }
    }
};

var setup_badge_details_toggle = function(){
    $('.badge-context-toggle').each(function(idx, elem){
        var context_list = $(elem).parent().next('ul');
        if (context_list.children().length > 0){
            $(elem).addClass('active');
            var toggle_display = function(){
                if (context_list.css('display') == 'none'){
                    $('.badge-context-list').hide();
                    context_list.show();
                } else {
                    context_list.hide();
                }
            };
            $(elem).click(toggle_display);
        }
    });
};

var ResponseNotifs = function() {
    WrappedElement.call(this);
};
inherits(ResponseNotifs, WrappedElement);

ResponseNotifs.prototype.clearNewNotifs = function() {
    var news = $('.new');
    $('#ab-responses').fadeOut();
    this._element.fadeOut(function() {
        news.removeClass('new highlight');
    });
};

ResponseNotifs.prototype.makeHandler = function() {
    var me = this;
    return function() {
        $.ajax({
            type: 'POST',
            cache: false,
            dataType: 'json',
            url: askbot['urls']['clearNewNotifications'],
            success: function(response_data){
                if (response_data['success']) {
                    me.clearNewNotifs();
                }
            }
        });
    };
};

ResponseNotifs.prototype.decorate = function(element) {
    this._element = element;
    var btn = element.find('a');
    setupButtonEventHandlers(btn, this.makeHandler());
};

/**
* the dropdown menu with selection of reasons
* to reject posts and a button that starts menu to 
* manage the list of reasons
*/
var DeclineAndExplainMenu = function() {
    WrappedElement.call(this);
};
inherits(DeclineAndExplainMenu, WrappedElement);

DeclineAndExplainMenu.prototype.setupDeclinePostHandler = function(button) {
    var me = this;
    var reasonId = button.data('reasonId');
    var controls = this.getControls();
    var handler = controls.getModHandler('decline-with-reason', ['posts'], reasonId);
    setupButtonEventHandlers(button, handler);
};

DeclineAndExplainMenu.prototype.addReason = function(id, title) {
    var li = this.makeElement('li');
    var button = this.makeElement('a');
    li.append(button);
    button.html(title);
    button.data('reasonId', id);
    button.attr('data-reason-id', id);
    this._addReasonBtn.parent().before(li);

    this.setupDeclinePostHandler(button);
};

DeclineAndExplainMenu.prototype.removeReason = function(id) {
    var btn = this._element.find('a[data-reason-id="' + id + '"]');
    btn.parent().remove();
};

DeclineAndExplainMenu.prototype.setControls = function(controls) {
    this._controls = controls;
};

DeclineAndExplainMenu.prototype.getControls = function() {
    return this._controls;
};

DeclineAndExplainMenu.prototype.decorate = function(element) {
    this._element = element;
    //activate dropdown menu
    element.dropdown();

    var declineBtns = element.find('.decline-with-reason');
    var me = this;
    declineBtns.each(function(idx, elem) {
        me.setupDeclinePostHandler($(elem));
    });

    this._reasonList = element.find('ul');

    var addReasonBtn = element.find('.manage-reasons');
    this._addReasonBtn = addReasonBtn;

    var manageReasonsDialog = new ManageRejectReasonsDialog();
    manageReasonsDialog.decorate($('#manage-reject-reasons-modal'));
    this._manageReasonsDialog = manageReasonsDialog;
    manageReasonsDialog.setMenu(this);

    setupButtonEventHandlers(addReasonBtn, function() { manageReasonsDialog.show(); });
};

/**
* Buttons to moderate posts 
* and the list of edits
*/
var PostModerationControls = function() {
    WrappedElement.call(this);
};
inherits(PostModerationControls, WrappedElement);

/**
* displays feedback message
*/
PostModerationControls.prototype.showMessage = function(message) {
    this._notification.html(message);
    this._notification.parent().fadeIn('fast');
};

PostModerationControls.prototype.hideMessage = function() {
    this._notification.parent().hide();
};

/**
* removes entries from the moderation screen
*/
PostModerationControls.prototype.removeEntries = function(entryIds) {
    for (var i = 0; i < entryIds.length; i++) {
        var id = entryIds[i];
        var elem = this._element.find('.message[data-message-id="' + id + '"]');
        if (elem.length) {
            elem.fadeOut('fast', function() { elem.remove() });
        }
    }
};

PostModerationControls.prototype.setEntryCount = function(count) {
    this._entryCount.html(count);
};

PostModerationControls.prototype.getEntryCount = function() {
    return this.getCheckBoxes().length;
};

PostModerationControls.prototype.getCheckBoxes = function() {
    return this._element.find('.messages input[type="checkbox"]');
};

PostModerationControls.prototype.getSelectedEditIds = function() {
    var checkBoxes = this.getCheckBoxes();
    var num = checkBoxes.length;
    var idList = [];
    for (var i = 0; i < num; i++) {
        var cb = $(checkBoxes[i]);
        if (cb.is(':checked')) {
            var msg = cb.closest('.message-details');
            var msgId = msg.data('messageId');
            idList.push(msgId);
        }
    }
    return idList;
};

/**
* action - one of 'decline-with-reason', 'approve', 'block'
* items - a list of items ['posts', 'users', 'ips']
* not all combinations of action and items are supported
* optReason must be used with 'decline-with-reason' action
*/
PostModerationControls.prototype.getModHandler = function(action, items, optReason) {
    var me = this;
    return function() {
        var selectedEditIds = me.getSelectedEditIds();
        if (selectedEditIds.length == 0) {
            me.showMessage(gettext('Please select at least one item'));
            return;
        }
        //@todo: implement undo
        var postData = {
            'edit_ids': selectedEditIds,//revision ids
            'action': action,
            'items': items,//affected items - users, posts, ips
            'reason': optReason || 'none'
        };
        $.ajax({
            type: 'POST',
            cache: false,
            dataType: 'json',
            data: JSON.stringify(postData),
            url: askbot['urls']['moderatePostEdits'],
            success: function(response_data){
                if (response_data['success'] == true){
                    me.removeEntries(response_data['memo_ids']);
                    me.setEntryCount(response_data['memo_count']);
                }

                var message = response_data['message'] || '';
                if (me.getEntryCount() < 10 && response_data['memo_count'] > 9) {
                    if (message) {
                        message += '. '
                    }
                    var junk = $('#junk-mod');
                    if (junk.length == 0) {
                        junk = me.makeElement('div');
                        junk.attr('id', 'junk-mod');
                        junk.hide();
                        $(document).append(junk);
                    }
                    var a = me.makeElement('a');
                    a.attr('href', window.location.href);
                    a.text(gettext('Load more items.'));
                    junk.append(a);
                    message += a[0].outerHTML;
                }
                if (message) {
                    me.showMessage(message);
                }
            }
        });
    };
};

PostModerationControls.prototype.getSelectAllHandler = function(selected) {
    var me = this;
    return function() {
        var cb = me.getCheckBoxes();
        cb.prop('checked', selected);
    };
};

PostModerationControls.prototype.decorate = function(element) {
    this._element = element;
    this._notification = element.find('.action-status span');
    this.hideMessage();

    this._entryCount = $('.mod-memo-count');
    //approve posts button
    var button = $('.approve-posts');
    setupButtonEventHandlers(button, this.getModHandler('approve', ['posts']));

    //approve posts and users
    button = $('.approve-posts-users');
    setupButtonEventHandlers(button, this.getModHandler('approve', ['posts', 'users']));

    //decline and explain why
    var reasonsMenuElem = $('.decline-reasons-menu');
    var declineAndExplainMenu = new DeclineAndExplainMenu();
    declineAndExplainMenu.setControls(this);
    declineAndExplainMenu.decorate(reasonsMenuElem);

    //delete posts and block users
    button = element.find('.decline-block-users');
    setupButtonEventHandlers(button, this.getModHandler('block', ['posts', 'users']));

    //delete posts, block users and ips
    button = element.find('.decline-block-users-ips');
    setupButtonEventHandlers(button, this.getModHandler('block', ['posts', 'users', 'ips']));

    button = element.find('.sel-all');
    setupButtonEventHandlers(button, this.getSelectAllHandler(true));

    button = element.find('.sel-none');
    setupButtonEventHandlers(button, this.getSelectAllHandler(false));
};


/**
 * @constructor
 * manages post/edit reject reasons
 * in the post moderation view
 */
var ManageRejectReasonsDialog = function(){
    WrappedElement.call(this);
    this._selected_edit_ids = null;
    this._selected_reason_id = null;
    this._state = null;//'select', 'add-new'
    this._postModerationControls = [];
    this._selectedEditDataReader = undefined;
};
inherits(ManageRejectReasonsDialog, WrappedElement);

ManageRejectReasonsDialog.prototype.setMenu = function(menu) {
    this._reasonsMenu = menu;
};

ManageRejectReasonsDialog.prototype.getMenu = function() {
    return this._reasonsMenu;
};

ManageRejectReasonsDialog.prototype.setSelectedEditDataReader = function(func) {
    this._selectedEditDataReader = func;
};

ManageRejectReasonsDialog.prototype.readSelectedEditData = function() {
    var data = this._selectedEditDataReader();
    this.setSelectedEditData(data);
    return data['id_list'].length > 0;
};

ManageRejectReasonsDialog.prototype.setSelectedEditData = function(data){
    this._selected_edit_data = data;
};

ManageRejectReasonsDialog.prototype.addPostModerationControl = function(control) {
    this._postModerationControls.push(control);
};

ManageRejectReasonsDialog.prototype.setState = function(state){
    this._state = state;
    this.clearErrors();
    if (this._element){
        this._selector.hide();
        this._adder.hide();
        if (state === 'select'){
            this._selector.show();
        } else if (state === 'add-new'){
            this._adder.show();
        }
    }
};

ManageRejectReasonsDialog.prototype.show = function(){
    $(this._element).modal('show');
};

ManageRejectReasonsDialog.prototype.hide = function(){
    $(this._element).modal('hide');
};

ManageRejectReasonsDialog.prototype.resetInputs = function(){
    if (this._title_input){
        this._title_input.reset();
    }
    if (this._details_input){
        this._details_input.reset();
    }
    var selected = this._element.find('.selected');
    selected.removeClass('selected');
};

ManageRejectReasonsDialog.prototype.clearErrors = function(){
    var error = this._element.find('.alert');
    error.remove();
};

ManageRejectReasonsDialog.prototype.makeAlertBox = function(errors){
    //construct the alert box
    var alert_box = new AlertBox();
    alert_box.setClass('alert-error');
    if (typeof errors === "string"){
        alert_box.setText(errors);
    } else if (errors.constructor === [].constructor){
        if (errors.length > 1){
            alert_box.setContent(
                '<div>' + 
                gettext('Looks there are some things to fix:') +
                '</div>'
            )
            var list = this.makeElement('ul');
            $.each(errors, function(idx, item){
                list.append('<li>' + item + '</li>');
            });
            alert_box.addContent(list);
        } else if (errors.length == 1){
            alert_box.setContent(errors[0]);
        } else if (errors.length == 0){
            return;
        }
    } else if ('html' in errors){
        alert_box.setContent(errors);
    } else {
        return;//don't know what to do
    }
    return alert_box;
};

ManageRejectReasonsDialog.prototype.setAdderErrors = function(errors){
    //clear previous errors
    this.clearErrors();
    var alert_box = this.makeAlertBox(errors);
    this._element
        .find('#reject-edit-modal-add-new .modal-body')
        .prepend(alert_box.getElement());
};

ManageRejectReasonsDialog.prototype.setSelectorErrors = function(errors){
    this.clearErrors();
    var alert_box = this.makeAlertBox(errors);
    this._element
        .find('#reject-edit-modal-select .modal-body')
        .prepend(alert_box.getElement());
};

ManageRejectReasonsDialog.prototype.setErrors = function(errors){
    this.clearErrors();
    var alert_box = this.makeAlertBox(errors);
    var current_state = this._state;
    this._element
        .find('#reject-edit-modal-' + current_state + ' .modal-body')
        .prepend(alert_box.getElement());
};

ManageRejectReasonsDialog.prototype.addSelectableReason = function(data){
    var id = data['reason_id'];
    var title = data['title'];
    var details = data['details'];
    this._select_box.addItem(id, title, details);

    askbot['data']['postRejectReasons'].push(
        {id: data['reason_id'], title: data['title']}
    );
    $.each(this._postModerationControls, function(idx, control) {
        control.addReason(data['reason_id'], data['title']);
    });
};

ManageRejectReasonsDialog.prototype.startSavingReason = function(callback){

    var title_input = this._title_input;
    var details_input = this._details_input;

    var errors = [];
    if (title_input.isBlank()){
        errors.push(gettext('Please provide description.'));
    }
    if (details_input.isBlank()){
        errors.push(gettext('Please provide details.'));
    }

    if (errors.length > 0){
        this.setAdderErrors(errors);
        return;//just show errors and quit
    }

    var data = {
        title: title_input.getVal(),
        details: details_input.getVal()
    };
    var reasonIsNew = true;
    if (this._selected_reason_id){
        data['reason_id'] = this._selected_reason_id;
        reasonIsNew = false;
    }

    var me = this;

    $.ajax({
        type: 'POST',
        dataType: 'json',
        cache: false,
        url: askbot['urls']['save_post_reject_reason'],
        data: data,
        success: function(data){
            if (data['success']){
                //show current reason data and focus on it
                me.addSelectableReason(data);
                if (reasonIsNew) {
                    me.getMenu().addReason(data['reason_id'], data['title']);
                }
                if (callback){
                    callback(data);
                } else {
                    me.setState('select');
                }
            } else {
                me.setAdderErrors(data['message']);
            }
        }
    });
};

ManageRejectReasonsDialog.prototype.startEditingReason = function(){
    var data = this._select_box.getSelectedItemData();
    var title = $(data['title']).text();
    var details = data['details'];
    this._title_input.setVal(title);
    this._details_input.setVal(details);
    this._selected_reason_id = data['id'];
    this.setState('add-new');
};

ManageRejectReasonsDialog.prototype.resetSelectedReasonId = function(){
    this._selected_reason_id = null;
};

ManageRejectReasonsDialog.prototype.getSelectedReasonId = function(){
    return this._selected_reason_id;
};

ManageRejectReasonsDialog.prototype.startDeletingReason = function(){
    var select_box = this._select_box;
    var data = select_box.getSelectedItemData();
    var reason_id = data['id'];
    var me = this;
    if (data['id']){
        $.ajax({
            type: 'POST',
            dataType: 'json',
            cache: false,
            url: askbot['urls']['delete_post_reject_reason'],
            data: {reason_id: reason_id},
            success: function(data){
                if (data['success']){
                    select_box.removeItem(reason_id);
                    me.hideEditButtons();
                    me.getMenu().removeReason(reason_id);
                } else {
                    me.setSelectorErrors(data['message']);
                }
            }
        });
    } else {
        me.setSelectorErrors(
            gettext('A reason must be selected to delete one.')
        )
    }
};

ManageRejectReasonsDialog.prototype.hideEditButtons = function() {
    this._editButton.hide();
    this._deleteButton.hide();
};

ManageRejectReasonsDialog.prototype.showEditButtons = function() {
    this._editButton.show();
    this._deleteButton.show();
};

ManageRejectReasonsDialog.prototype.decorate = function(element){
    this._element = element;
    //set default state according to the # of available reasons
    this._selector = $(element).find('#reject-edit-modal-select');
    this._adder = $(element).find('#reject-edit-modal-add-new');
    if (this._selector.find('li').length > 0){
        this.setState('select');
        this.resetInputs();
    } else {
        this.setState('add-new');
        this.resetInputs();
    }

    var select_box = new SelectBox();
    select_box.decorate($(this._selector.find('.select-box')));
    select_box.setSelectHandler(function() { me.showEditButtons() });
    this._select_box = select_box;

    //setup tipped-inputs
    var reject_title_input = $(this._element).find('input');
    var title_input = new TippedInput();
    title_input.decorate($(reject_title_input));
    this._title_input = title_input;

    var reject_details_input = $(this._element).find('textarea.reject-reason-details');

    var details_input = new TippedInput();
    details_input.decorate($(reject_details_input));
    this._details_input = details_input;

    var me = this;
    setupButtonEventHandlers(
        element.find('.cancel, .modal-header .close'),
        function() {
            me.hide();
            me.clearErrors();
            me.resetInputs();
            me.resetSelectedReasonId();
            me.setState('select');
            me.hideEditButtons();
        }
    );

    setupButtonEventHandlers(
        $(this._element).find('.save-reason'),
        function(){ me.startSavingReason() }
    );

    setupButtonEventHandlers(
        element.find('.add-new-reason'),
        function(){ 
            me.resetSelectedReasonId();
            me.resetInputs();
            me.setState('add-new') ;
        }
    );

    this._editButton = element.find('.edit-this-reason');
    setupButtonEventHandlers(
        this._editButton,
        function(){
            me.startEditingReason();
        }
    );

    this._deleteButton = element.find('.delete-this-reason');
    setupButtonEventHandlers(
        this._deleteButton,
        function(){
            me.startDeletingReason();
        }
    )
};

/**
 * @constructor
 * allows to follow/unfollow users
 */
var FollowUser = function(){
    WrappedElement.call(this);
    this._user_id = null;
    this._user_name = null;
};
inherits(FollowUser, WrappedElement);

/**
 * @param {string} user_name
 */
FollowUser.prototype.setUserName = function(user_name){
    this._user_name = user_name;
};

FollowUser.prototype.decorate = function(element){
    this._element = element;
    this._user_id = parseInt(element.attr('id').split('-').pop());
    this._available_action = element.children().hasClass('follow') ? 'follow':'unfollow';
    var me = this;
    setupButtonEventHandlers(this._element, function(){ me.go() });
};

FollowUser.prototype.go = function(){
    if (askbot['data']['userIsAuthenticated'] === false){
        var message = gettext('Please <a href="%(signin_url)s">signin</a> to follow %(username)s');
        var message_data = {
            signin_url: askbot['urls']['user_signin'] + '?next=' + window.location.href,
            username: this._user_name
        }
        message = interpolate(message, message_data, true);
        showMessage(this._element, message);
        return;
    }
    var user_id = this._user_id;
    if (this._available_action === 'follow'){
        var url = askbot['urls']['follow_user'];
    } else {
        var url = askbot['urls']['unfollow_user'];
    }
    var me = this;
    $.ajax({
        type: 'POST',
        cache: false,
        dataType: 'json',
        url: url.replace('{{userId}}', user_id),
        success: function(){ me.toggleState() }
    });
};

FollowUser.prototype.toggleState = function(){
    if (this._available_action === 'follow'){
        this._available_action = 'unfollow';
        var unfollow_div = document.createElement('div'); 
        unfollow_div.setAttribute('class', 'unfollow');
        var red_div = document.createElement('div');
        red_div.setAttribute('class', 'unfollow-red');
        //red_div.innerHTML = interpolate(gettext('unfollow %s'), [this._user_name]);
        red_div.innerHTML = interpolate(gettext('Unfollow'));
        //var green_div = document.createElement('div');
        //green_div.setAttribute('class', 'unfollow-green');
        //green_div.innerHTML = interpolate(gettext('following %s'), [this._user_name]);
        unfollow_div.appendChild(red_div);
        //unfollow_div.appendChild(green_div);
        this._element.html(unfollow_div);
    } else {
        var follow_div = document.createElement('div'); 
        //follow_div.innerHTML = interpolate(gettext('follow %s'), [this._user_name]);
        follow_div.innerHTML = interpolate(gettext('Follow'));
        follow_div.setAttribute('class', 'follow');
        this._available_action = 'follow';
        this._element.html(follow_div);
    }
};

/**
 * @constructor
 * @param {string} name
 */
var UserGroup = function(name){
    WrappedElement.call(this);
    this._name = name;
    this._content = null;
};
inherits(UserGroup, WrappedElement);

UserGroup.prototype.getDeleteHandler = function(){
    var group_name = this._name;
    var me = this;
    var groups_container = me._groups_container;
    return function(){
        var data = {
            user_id: askbot['data']['viewUserId'],
            group_name: group_name,
            action: 'remove'
        };
        $.ajax({
            type: 'POST',
            dataType: 'json',
            data: data,
            cache: false,
            url: askbot['urls']['edit_group_membership'],
            success: function(){
                groups_container.removeGroup(me);
            }
        });
    };
};

UserGroup.prototype.setContent = function(content){
    this._content = content;
};

UserGroup.prototype.getName = function(){
    return this._name;
};

UserGroup.prototype.setGroupsContainer = function(container){
    this._groups_container = container;
};

UserGroup.prototype.decorate = function(element){
    this._element = element;
    this._name = $.trim(element.find('a').html());
    var deleter = new DeleteIcon();
    deleter.setHandler(this.getDeleteHandler());
    //deleter.setContent(gettext('Remove'));
    this._element.find('td:last').append(deleter.getElement());
    this._delete_icon = deleter;
};

UserGroup.prototype.createDom = function(){
    var element = this.makeElement('tr');
    element.html(this._content);
    this._element = element;
    this.decorate(element);
};

UserGroup.prototype.dispose = function(){
    this._delete_icon.dispose();
    this._element.remove();
};

/**
 * @constructor
 */
var GroupsContainer = function(){
    WrappedElement.call(this);
};
inherits(GroupsContainer, WrappedElement);

GroupsContainer.prototype.decorate = function(element){
    this._element = element;
    var groups = [];
    var group_names = [];
    var me = this;
    //collect list of groups
    $.each(element.find('tr'), function(idx, li){
        var group = new UserGroup();
        group.setGroupsContainer(me);
        group.decorate($(li));
        groups.push(group);
        group_names.push(group.getName());
    });
    this._groups = groups;
    this._group_names = group_names;
};

GroupsContainer.prototype.addGroup = function(group_data){
    var group_name = group_data['name'];
    if ($.inArray(group_name, this._group_names) > -1){
        return;
    }
    var group = new UserGroup(group_name);
    group.setContent(group_data['html']);
    group.setGroupsContainer(this);
    this._groups.push(group);
    this._group_names.push(group_name);
    this._element.append(group.getElement());
};

GroupsContainer.prototype.removeGroup = function(group){
    var idx = $.inArray(group, this._groups);    
    if (idx === -1){
        return;
    }
    this._groups.splice(idx, 1);
    this._group_names.splice(idx, 1);
    group.dispose();
};

var GroupAdderWidget = function(){
    WrappedElement.call(this);
    this._state = 'display';//display or edit
};
inherits(GroupAdderWidget, WrappedElement);

/**
 * @param {string} state
 */
GroupAdderWidget.prototype.setState = function(state){
    if (state === 'display'){
        this._element.html(gettext('add group'));
        this._input.hide();
        this._input.val('');
        this._button.hide();
    } else if (state === 'edit'){
        this._element.html(gettext('cancel'));
        this._input.show();
        this._input.focus();
        this._button.show();
    } else {
        return;
    }
    this._state = state;
};

GroupAdderWidget.prototype.getValue = function(){
    return this._input.val();
};

GroupAdderWidget.prototype.addGroup = function(group_data){
    this._groups_container.addGroup(group_data);
};

GroupAdderWidget.prototype.getAddGroupHandler = function(){
    var me = this;
    return function(){
        var group_name = me.getValue();
        var data = {
            group_name: group_name,
            user_id: askbot['data']['viewUserId'],
            action: 'add'
        };
        $.ajax({
            type: 'POST',
            dataType: 'json',
            data: data,
            cache: false,
            url: askbot['urls']['edit_group_membership'],
            success: function(data){
                if (data['success'] == true){
                    me.addGroup(data);
                    me.setState('display');
                } else {
                    var message = data['message'];
                    showMessage(me.getElement(), message, 'after');
                }
            }
        });
    };
};

GroupAdderWidget.prototype.setGroupsContainer = function(container){
    this._groups_container = container;
};

GroupAdderWidget.prototype.toggleState = function(){
    if (this._state === 'display'){
        this.setState('edit');
    } else if (this._state === 'edit'){
        this.setState('display');
    }
};

GroupAdderWidget.prototype.decorate = function(element){
    this._element = element;
    var input = this.makeElement('input');
    input.attr('type', 'text');
    this._input = input;

    var groupsAc = new AutoCompleter({
        url: askbot['urls']['getGroupsList'],
        minChars: 1,
        useCache: false,
        matchInside: false,
        maxCacheLength: 100,
        delay: 10
    });
    groupsAc.decorate(input);

    var button = this.makeElement('button');
    button.html(gettext('add'));
    this._button = button;
    element.before(input);
    input.after(button);
    this.setState('display');
    setupButtonEventHandlers(button, this.getAddGroupHandler());
    var me = this;
    setupButtonEventHandlers(
        element,
        function(){ me.toggleState() }
    );
};

/**
 * @constructor
 * allows editing user groups
 */
var UserGroupsEditor = function(){
    WrappedElement.call(this);
};
inherits(UserGroupsEditor, WrappedElement);

UserGroupsEditor.prototype.decorate = function(element){
    this._element = element;
    var add_link = element.find('#add-group');
    var adder = new GroupAdderWidget();
    adder.decorate(add_link);

    var groups_container = new GroupsContainer();
    groups_container.decorate(element.find('#groups-list'));
    adder.setGroupsContainer(groups_container);
    //todo - add group deleters
};

/**
 * controls that set up automatic tweeting to the user account
 */
var Tweeting = function() {
    WrappedElement.call(this);
};
inherits(Tweeting, WrappedElement);

Tweeting.prototype.getStartHandler = function() {
    var url = this._startUrl;
    return function() {
        window.location.href = url;
    };
};

Tweeting.prototype.getMode = function() {
    return this._modeSelector.val();
};

Tweeting.prototype.getModeSelectorHandler = function() {
    var me = this;
    var url = this._changeModeUrl;
    return function() {
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: url,
            data: {'mode': me.getMode() },
            cache: false
        });
    };
};

Tweeting.prototype.getAccount = function() {
    return this._accountSelector.val();
};

Tweeting.prototype.getAccountSelectorHandler = function() {
    var selectAccountUrl = this._changeModeUrl;
    var startUrl = this._startUrl;
    var me = this;
    return function() {
        var account = me.getAccount();
        if (account === 'existing-handle') {
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: selectAccountUrl,
                data: {'mode': 'share-my-posts' },
                cache: false
            });
        } else if (account === 'new-handle') {
            window.location.href = startUrl;
        }
    }
};

Tweeting.prototype.decorate = function(element) {
    this._element = element;
    this._changeModeUrl = element.data('changeModeUrl');
    this._startUrl = element.data('startUrl');
    if (element.hasClass('disabled')) {
        this._startButton = element.find('.start-tweeting');
        setupButtonEventHandlers(this._startButton, this.getStartHandler());
    } else if (element.hasClass('inactive')) {
        //decorate choose account selector
        this._accountSelector = element.find('select');
        this._accountSelector.change(this.getAccountSelectorHandler());
    } else if (element.hasClass('enabled')) {
        //decorate choose mode selector
        this._modeSelector = element.find('select');
        this._modeSelector.change(this.getModeSelectorHandler());
    }
};

var UserQuestionsPaginator = function() {
    Paginator.call(this);
};
inherits(UserQuestionsPaginator, Paginator);

UserQuestionsPaginator.prototype.renderPage = function(data) {
    $('.users-questions').html(data['questions']);
    $('.timeago').timeago();
};

UserQuestionsPaginator.prototype.getPageDataUrl = function(pageNo) {
    var userId = askbot['data']['viewUserId'];
    var pageSize = askbot['data']['userPostsPageSize'];
    var url = QSutils.patch_query_string('', 'author:' + userId);
    url = QSutils.patch_query_string(url, 'sort:votes-desc');
    url = QSutils.patch_query_string(url, 'page:' + pageNo);
    url = QSutils.patch_query_string(url, 'page-size:'+ pageSize);
    return askbot['urls']['questions'] + url;
};

var UserAnswersPaginator = function() {
    Paginator.call(this);
};
inherits(UserAnswersPaginator, Paginator);

UserAnswersPaginator.prototype.renderPage = function(data) {
    $('.users-answers').html(data['html']);
    $('.timeago').timeago();
};

UserAnswersPaginator.prototype.getPageDataUrl = function() {
    return askbot['urls']['getTopAnswers'];
};

UserAnswersPaginator.prototype.getPageDataUrlParams = function(pageNo) {
    return {
        user_id: askbot['data']['viewUserId'],
        page_number: pageNo
    }
};

(function(){
    var fbtn = $('.follow-user-toggle');
    if (fbtn.length === 1){
        var follow_user = new FollowUser();
        follow_user.decorate(fbtn);
        follow_user.setUserName(askbot['data']['viewUserName']);
    }
    if (askbot['data']['userId'] !== askbot['data']['viewUserId']) {
        if (askbot['data']['userIsAdminOrMod']){
            var group_editor = new UserGroupsEditor();
            group_editor.decorate($('#user-groups'));
        } else {
            $('#add-group').remove();
        }
    } else {
        $('#add-group').remove();
    }

    var tweeting = $('.auto-tweeting');
    if (tweeting.length) {
        var tweetingControl = new Tweeting();
        tweetingControl.decorate(tweeting);
    }
    
    var qPager = $('.user-questions-pager');
    if (qPager.length) {
        var qPaginator = new UserQuestionsPaginator();
        qPaginator.decorate(qPager);
    }

    var aPager = $('.user-answers-pager');
    if (aPager.length) {
        var aPaginator = new UserAnswersPaginator();
        aPaginator.decorate(aPager);
    }

})();
