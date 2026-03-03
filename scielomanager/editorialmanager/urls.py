# coding: utf-8
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name="editorial.index"),

    # Journal related urls
    re_path(r'^journal/detail/(?P<journal_id>\d+)/$', views.journal_detail, name="editorial.journal.detail"),
    re_path(r'^journal/(?P<journal_id>\d+)/edit/$', views.edit_journal, name="editorial.journal.edit"),

    # Editorial Manager
    re_path(r'^board/(?P<journal_id>\d+)/$', views.board, name="editorial.board"),
    re_path(r'^board/(?P<journal_id>\d+)/move/$', views.board_move_block, name="editorial.board.move"),
    re_path(r'^board/(?P<journal_id>\d+)/members/(?P<issue_id>\d+)/add/$', views.add_board_member, name="editorial.board.add"),
    re_path(r'^board/(?P<journal_id>\d+)/members/(?P<member_id>\d+)/edit/$', views.edit_board_member, name="editorial.board.edit"),
    re_path(r'^board/(?P<journal_id>\d+)/members/(?P<member_id>\d+)/delete/$', views.delete_board_member, name="editorial.board.delete"),
    re_path(r'^board/(?P<journal_id>\d+)/roles/$', views.list_role_type, name="editorial.role.list"),
    re_path(r'^board/(?P<journal_id>\d+)/roles/add/$', views.add_role_type, name="editorial.role.add"),
    re_path(r'^board/(?P<journal_id>\d+)/roles/(?P<role_id>\d+)/edit/$', views.edit_role_type, name="editorial.role.edit"),
    re_path(r'^board/(?P<journal_id>\d+)/roles/(?P<role_id>\d+)/translate/$', views.translate_role_type, name="editorial.role.translate"),

    # Export board members CSV
    re_path(r'^board/(?P<journal_id>\d+)/export/csv/$', views.export_csv, name="editorial.export.csv.journal"),
    re_path(r'^board/(?P<journal_id>\d+)/export/csv/(?P<issue_id>\d+)/$', views.export_csv, name="editorial.export.csv.issue"),
]
