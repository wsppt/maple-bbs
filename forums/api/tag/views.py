#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: views.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-15 22:07:04 (CST)
# Last Update:星期四 2016-12-29 21:18:30 (CST)
#          By:
# Description:
# **************************************************************************
from flask import request, url_for, current_app, render_template
from flask.views import MethodView
from flask_maple.serializer import FlaskSerializer as Serializer
from flask_maple.response import HTTPResponse
from common.views import ViewListMixin
from api.topic.models import Topic
from .models import Tags
from urllib.parse import urljoin
from werkzeug.utils import escape
from werkzeug.contrib.atom import AtomFeed


class TagsListView(MethodView, ViewListMixin):
    per_page = 99

    def get(self):
        page, number = self.page_info
        tags = Tags.get_list(page, number)
        return render_template('tag/tag_list.html', tags=tags)
        # serializer = Serializer(users, many=True)
        # return HTTPResponse(HTTPResponse.NORMAL_STATUS,
        #                     **serializer.data).to_response()

    def post(self):
        return 'post'


class TagsView(MethodView):
    def get(self, name):
        tag = Tags.get(name=name)
        return render_template('tag/tag.html', tag=tag)
        # serializer = Serializer(user, many=False)
        # return HTTPResponse(
        #     HTTPResponse.NORMAL_STATUS, data=serializer.data).to_response()

    def put(self, name):
        return 'put'

    def delete(self, name):
        return 'delete'


class TagFeedView(MethodView):
    def get(self, name):
        setting = current_app.config.get('SITE')
        title = setting['title']
        introduce = setting['introduce']
        feed = AtomFeed(
            '%s·%s' % (name, title),
            feed_url=request.url,
            url=request.url_root,
            subtitle=introduce)
        topics = Topic.query.filter_by(tags__name=name).all()
        for topic in topics:
            if topic.content_type == Topic.CONTENT_TYPE_MARKDOWN:
                content = topic.content
            else:
                content = topic.content
            feed.add(topic.title,
                     content,
                     content_type='html',
                     author=topic.author.username,
                     url=urljoin(
                         request.url_root,
                         url_for(
                             'topic.topic', topicId=topic.id)),
                     updated=topic.updated_at,
                     published=topic.created_at)
        return feed.get_response()
