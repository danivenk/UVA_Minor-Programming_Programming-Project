#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
adminviews.py defines the AdminIndexView and all ModelViews
Dani van Enk, 11823526

references:
    https://flask-admin.readthedocs.io/en/v1.0.4/quickstart/
    https://flask-admin.readthedocs.io/en/latest/api/mod_model/
    https://flask-admin.readthedocs.io/en/latest/api/mod_contrib_sqla/
"""

# used imports
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask import abort, request, redirect, url_for
from flask_login import current_user


class AdminUserIndexView(AdminIndexView):
    """
    Here the AdminUserIndexView class is defined
        it's based on the AdminIndexView class

    expose:
        index ("/") - renders the homepage of the admin part of the site;

    methods:
        is_accessible           - returns if current_user is admin;
        inaccessible_callback   - redirects to site index if inaccessible
    """

    @expose("/", methods=["GET"])
    def index(self):
        """
        defines the index template for the admin part of the site

        expose:
            - "/"

        abort:
            - if method is not in methods (405)
        """

        if request.method not in request.url_rule.methods:
            abort(405)

        return self.render("admin/index.html", user=current_user)

    def is_accessible(self):
        """
        check if current_user is admin, return true if so else false
        """

        return current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        """
        redirect to site home if user isn't admin
        """

        return redirect(url_for('index'))


class AdminView(ModelView):
    """
    Here the AdminView class is defined
        it's based on the ModelView class

    methods:
        is_accessible           - returns if current_user is admin;
        inaccessible_callback   - redirects to site index if inaccessible
    """

    # excludes from columns and forms
    column_exclude_list = ["password"]

    def is_accessible(self):
        """
        check if current_user is admin, return true if so else false
        """

        return current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        """
        redirect to site home if user isn't admin
        """

        return redirect(url_for('index'))


class NetworkView(ModelView):
    """
    Here the NetworkView class is defined
        it's based on the ModelView class

    methods:
        is_accessible           - returns if current_user is admin;
        inaccessible_callback   - redirects to site index if inaccessible
    """

    # excludes from columns
    column_exclude_list = ["stops_order"]

    def is_accessible(self):
        """
        check if current_user is admin, return true if so else false
        """

        return current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        """
        redirect to site home if user isn't admin
        """

        return redirect(url_for('index'))
