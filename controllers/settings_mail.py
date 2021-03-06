# -*- coding: utf-8 -*-
"""
    This file holds the settings for email
"""

def mail_get_menu(page):
    """
        Menu for system settings pages
    """
    pages = [['mailing_lists',
              T('Mailing lists'),
              URL('mailing_lists')],
             ['templates',
              T('Templates'),
              URL('templates')],
             ['notifications',
              T('Notifications'),
              URL('notifications')],
             ]

    return os_gui.get_submenu(pages, page, horizontal=True, htype='tabs')


@auth.requires(auth.has_membership(group_id='Admins') or
               auth.has_permission('read', 'settings'))
def mailing_lists():
    """
        Show mailing lists
    """
    from openstudio.os_mailinglists import MailingLists

    response.title = T('Settings')
    response.subtitle = T('Mail')
    response.view = 'general/tabs_menu.html'

    mailing_lists = MailingLists()
    content = mailing_lists.list_formatted()

    add = os_gui.get_button('add', URL('settings_mail', 'mailing_list_add'))
    menu = mail_get_menu(request.function)

    return dict(content=content,
                add=add,
                menu=menu)


def mailing_list_get_return_url(var=None):
    """
        :return: URL to lists
    """
    return URL('settings_mail', 'mailing_lists')


@auth.requires_login()
def mailing_list_add():
    """
        Add a new mailing_list
    """
    from openstudio.os_forms import OsForms
    response.title = T('Settings')
    response.subtitle = T('Mail')
    response.view = 'general/tabs_menu.html'

    return_url = mailing_list_get_return_url()

    os_forms = OsForms()
    result = os_forms.get_crud_form_create(
        db.mailing_lists,
        return_url,
    )

    form = result['form']
    back = os_gui.get_button('back', return_url)
    menu = mail_get_menu('mailing_lists')

    content = DIV(
        H4(T('Add mailing list')),
        form
    )

    return dict(content=content,
                save=result['submit'],
                back=back,
                menu=menu)


@auth.requires_login()
def mailing_list_edit():
    """
        Edit a mailing_list
        request.vars['mlID'] is expected to be db.mailing_lists.id
    """
    from openstudio.os_forms import OsForms

    response.title = T('Settings')
    response.subtitle = T('Mail')
    response.view = 'general/tabs_menu.html'
    mlID = request.vars['mlID']

    return_url = mailing_list_get_return_url()

    os_forms = OsForms()
    result = os_forms.get_crud_form_update(
        db.mailing_lists,
        return_url,
        mlID
    )

    form = result['form']
    back = os_gui.get_button('back', return_url)
    menu = mail_get_menu('mailing_lists')

    content = DIV(
        H4(T('Edit mailing list')),
        form
    )

    return dict(content=content,
                save=result['submit'],
                back=back,
                menu=menu)


@auth.requires(auth.has_membership(group_id='Admins') or \
               auth.has_permission('delete', 'mailing_lists'))
def mailing_list_delete():
    """
        Delete a mailing list
        request.vars[mlID] is expected to be in db.mailing_lists.id
        :return: None
    """
    mlID = request.vars['mlID']

    query = (db.mailing_lists.id == mlID)
    db(query).delete()

    session.flash = T('Deleted mailing list')
    redirect(mailing_list_get_return_url())


@auth.requires(auth.has_membership(group_id='Admins') or
               auth.has_permission('read', 'settings'))
def templates():
    """
        Templates main
    """
    response.title = T('Settings')
    response.subtitle = T('Mail')
    response.view = 'settings/email_templates.html'

    header = THEAD(TR(
        TH('Template'),
        TH(T(''))
    ))

    table = TABLE(header, _class='table table-hover table-striped')

    # the templates saved in sys_email_templates sorted by Name
    query = db.sys_email_templates
    rows = db(query).select(db.sys_email_templates.id,
                            db.sys_email_templates.Name,
                            db.sys_email_templates.Title,
                            orderby=db.sys_email_templates.Name)
    for i, row in enumerate(rows):
        repr_row = list(rows[i:i + 1].render())[0]

        tr = TR(
                TD(repr_row.Title),
                os_gui.get_button(
                    'edit_custom',
                    URL('edit_template', vars={'template':row.Name}),
                    T("Edit the content of this template"),
                    title='Edit template',
                    _class='pull-right')
                )

        table.append(tr)

    content = DIV(table)
    return dict(
        content=content,
        menu=mail_get_menu(request.function),
    )


@auth.requires(auth.has_membership(group_id='Admins') or
               auth.has_permission('read', 'settings'))
def edit_template():
    """
        Page to edit an email_template
    """
    from openstudio.os_forms import OsForms

    response.title = T('Settings')
    response.subtitle = T('Mail')
    response.view = 'settings/email_templates.html'

    template = request.vars['template']

    row = db.sys_email_templates(Name=template)
    template_content = row.TemplateContent
    form = SQLFORM.factory(
        Field("email_template", 'text',
              default=template_content,
              label=T("Template content")),
        submit_button=T("Save"),
        separator=' ',
        formstyle='bootstrap3_stacked')

    form_element = form.element('#no_table_email_template')
    form_element['_class'] += ' tmced'

    os_forms = OsForms()
    result = os_forms.set_form_id_and_get_submit_button(form, 'MainForm')
    form = result['form']
    submit = result['submit']
    if form.accepts(request.vars, session):
        # check smtp_signature
        email_template = request.vars['email_template']
        query = (db.sys_email_templates.Name == template)
        db(query).update(TemplateContent=email_template)

        # User feedback
        session.flash = T('Saved')

        # reload so the user sees how the values are stored in the db now
        redirect(URL(vars={'template': template}))


    back = os_gui.get_button('back', URL('templates'))
    # submenu = email_templates_get_menu(template)
    content = DIV(
        H4(T("Edit template: {name}".format(name=row.Title))),
        form
    )

    return dict(content=content,
                back=back,
                menu=mail_get_menu('templates'),
                save=submit)


@auth.requires(auth.has_membership(group_id='Admins') or
               auth.has_permission('read', 'settings'))
def notifications():
    """
        Shows a page with the Notifications options
    """
    response.title = T('Settings')
    response.subtitle = T('Mail')
    response.view = 'general/tabs_menu.html'

    header = THEAD(TR(
        TH(db.sys_notifications.Notification.label),
        TH(db.sys_notifications.NotificationTitle.label),
        TH(T('Subscribers'))
    ))

    table = TABLE(header, _class='table table-hover table-striped')

    query = (db.sys_notifications.id > 0)

    rows = db(query).select(db.sys_notifications.id,
                            db.sys_notifications.Notification,
                            db.sys_notifications.NotificationTitle,
                            orderby=db.sys_notifications.Notification)

    for i, row in enumerate(rows):
        repr_row = list(rows[i:i + 1].render())[0]
        emails = notifications_get_email_list(row.id)

        tr = TR(
            TD(repr_row.Notification),
            TD(repr_row.NotificationTitle),
            TD(emails))

        table.append(tr)

    content = DIV(table)

    menu = mail_get_menu(request.function)

    return dict(content=content, menu=menu)


def notifications_get_email_list(sys_notifications_id):
    """
    :param sys_notifications_id: db.sys_notifications.id
    :return: List of email addresses for a notification
    """
    query = (db.sys_notifications_email.sys_notifications_id == sys_notifications_id)
    rows = db(query).select(db.sys_notifications_email.id,
                            db.sys_notifications_email.sys_notifications_id,
                            db.sys_notifications_email.Email,
                            orderby=~db.sys_notifications_email.id)
    addresses = DIV()
    for i, row in enumerate(rows):
        repr_row = list(rows[i:i + 1].render())[0]

        delete = ''
        if auth.has_membership(group_id='Admins'):
            confirm_msg = T("Unsubscribe this email from this notification?")
            onclick_del = "return confirm('" + confirm_msg + "');"
            delete = A(os_gui.get_fa_icon('fa-times'),
                       _href=URL('notifications_email_delete', vars={'sneID': repr_row.id}),
                       _onclick=onclick_del,
                       _class='text-red')

        address = DIV(repr_row.Email, ' ', delete)
        addresses.append(address)

    if (auth.has_membership(group_id='Admins') or
            auth.has_permission('read', 'settings')):
        add_url = URL('notifications_email_add', vars={'snID': sys_notifications_id})
        add = A(SPAN(os_gui.get_fa_icon('fa-plus')),
                _href=add_url)
        addresses.append(add)

    return addresses


@auth.requires_login()
def notifications_email_delete():
    sneID = request.vars['sneID']

    query = (db.sys_notifications_email.id == sneID)
    db(query).delete()

    session.flash = T('Removed email from notification')
    redirect(URL('notifications'))


@auth.requires_login()
def notifications_email_add():
    """
    Subscribe email address to notification
    """
    from openstudio.os_forms import OsForms
    response.title = T('Settings')
    response.subtitle = T('Mail')
    response.view = 'general/tabs_menu.html'

    snID = request.vars['snID']

    return_url = URL('notifications')

    db.sys_notifications_email.sys_notifications_id.default = snID
    os_forms = OsForms()
    result = os_forms.get_crud_form_create(
        db.sys_notifications_email,
        return_url,
    )

    form = result['form']
    back = os_gui.get_button('back', return_url)
    menu = mail_get_menu(request.function)

    row = db.sys_notifications(snID)

    content = DIV(
        H4(T('Add Email to '),
           row.Notification),
        form
    )

    return dict(content=content,
                save=result['submit'],
                back=back,
                menu=menu)

