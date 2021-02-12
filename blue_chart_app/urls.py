
"""
Created on Sat Dec 19 13:50:53 2020

@author: Mayuko
"""


from django.urls import path
from . import views


app_name = 'blue_chart_app'

urlpatterns = [
    
    path('', views.chapter_view.chapter_list, name='chapter_list'),
    path('siteUser/register', views.siteUser_view.siteUser_register, name='siteUser_register'),
    path('siteUser/logout', views.siteUser_view.siteUser_logout, name='siteUser_logout'),
    path('siteUser/login', views.siteUser_view.siteUser_login, name='siteUser_login'),
    path('siteUser/reference_user/login', views.siteUser_view.reference_user_login_view, name='reference_user_login'),
    path('siteUser/reference_user/logout', views.siteUser_view.reference_user_logout_view, name='reference_user_logout'),
    path('chapter/list', views.chapter_view.chapter_list, name='chapter_list'),
    path('section/list/<int:chapter_id>/', views.section_view.section_list_view, name='section_list'),
    path('problem_group/list/<int:section_id>/', views.problem_group_view.problem_group_list_view, name='problem_group_list'),
    path('problem/list/<int:problem_group_id>/', views.problem_view.problem_list_view, name='problem_list'),
    path('problem/search', views.problem_view.problem_search_view, name='problem_search'),
    path('problem/show/<int:problem_id>/', views.problem_view.problem_show_view, name='problem_show'),
    path('problem/list_with_cause_tag/<int:cause_tag_id>/<int:section_id>/', views.problem_view.problem_list_with_cause_tag_view, name='problem_list_with_cause_tag'),
    path('evaluate/register/<int:problem_id>/', views.evaluate_view.evaluate_register_view, name='evaluate_register'),
    path('evaluate/delete/<int:evaluate_id>/', views.evaluate_view.evaluate_delte_view, name='evaluate_delete'),
    path('comment_for_evaluate/register/<int:evaluate_id>/', views.comment_for_evaluate_view.comment_for_evaluate_register_view, name='comment_for_evaluate_register'),
    path('comment_for_evaluate/update/<int:comment_for_evaluate_id>/', views.comment_for_evaluate_view.comment_for_evaluate_update_view, name='comment_for_evaluate_update'),
    path('comment_for_evaluate/delte/<int:comment_for_evaluate_id>/', views.comment_for_evaluate_view.comment_for_evaluate_delete_view, name='comment_for_evaluate_delete'),
    path('evaluation/suggest/', views.evaluation_tag_view.evaluation_tag_suggest_view, name='evaluation_tag_suggest'),
    path('evaluation/search/', views.evaluation_tag_view.evaluation_tag_search_view, name='evaluation_tag_search'),
    path('answer/register/<int:problem_id>/', views.answer_view.answer_register_view, name='answer_register'),
    path('answer/update/<int:answer_id>/', views.answer_view.answer_update_view, name='answer_update'),
    path('answer/list_with_problem/<int:problem_id>/', views.answer_view.answer_list_with_problem_view, name='answer_list_with_problem'),
    path('answer/list_with_cause_tag/<int:problem_id>/<int:cause_tag_id>/<int:section_id>/', views.answer_view.answer_list_with_cause_tag_view, name='answer_list_with_cause_tag'),
    path('answer/all_list/', views.answer_view.answer_all_list_view, name='answer_all_list'),
    path('answer/show/<int:answer_id>/', views.answer_view.answer_show_view, name='answer_show'),
    path('answer/delete/<int:answer_id>/', views.answer_view.answer_delete_view, name='answer_delete'),
    path('commet_for_answer/register/<int:answer_id>/', views.comment_for_answer_view.comment_for_answer_register_view, name='comment_for_answer_register'),
    path('comment_for_answer/update/<int:comment_for_answer_id>/', views.comment_for_answer_view.comment_for_answer_update_view, name='comment_for_answer_update'),
    path('comment_for_answer/delete/<int:comment_for_answer_id>/', views.comment_for_answer_view.comment_for_answer_delete_view, name='comment_for_answer_delete'),
    path('answer_photo/register/<int:answer_id>/', views.answer_photo_view.answer_photo_register_view, name='answer_photo_register'),
    path('answer_photo/delete/<int:answer_photo_id>/', views.answer_photo_view.answer_photo_delete_view, name='answer_photo_delete'),
    path('comment_for_answer_photo/register/<int:answer_photo_id>/', views.comment_for_answer_photo_view.comment_for_answer_photo_register_view, name='comment_for_answer_photo_register'),
    path('comment_for_answer_photo/update/<int:comment_for_answer_photo_id>/', views.comment_for_answer_photo_view.comment_for_answer_photo_update_view, name='comment_for_answer_photo_update'),
    path('comment_for_answer_photo/delete/<int:comment_for_answer_photo_id>/', views.comment_for_answer_photo_view.comment_for_answer_photo_delete_view, name='comment_for_answer_photo_delete'),
    path('cause_tag/list/<int:section_id>/', views.cause_tag_view.cause_tag_list_view, name='cause_tag_list'),
    path('cause_tag/graph/', views.cause_tag_view.cause_tag_graph, name='cause_tag_graph'),
    path('cause_tag/connects_count/', views.cause_tag_view.connects_count, name='connects_count'),
    path('connect/register/<int:answer_id>/', views.connect_view.connect_register_view, name='connect_register'),
    path('connect/overcome_flag_change/<int:connect_id>/', views.connect_view.connect_is_overcome_change_view, name='connect_is_overcome_change'),
    path('connect/delete/<int:connect_id>/', views.connect_view.connect_delete_view, name='connect_delete'),
    path('comment_for_connect/register/<int:connect_id>/', views.comment_for_connect_view.comment_for_connect_register_view, name='comment_for_connect_register'),
    path('comment_for_connect/update/<int:comment_for_connect_id>/', views.comment_for_connect_view.comment_for_connect_update_view, name='comment_for_connect_update'),
    path('comemnt_for_connect/delete/<int:comemnt_for_connect_id>/', views.comment_for_connect_view.comment_for_connect_delete_view, name='comment_for_connect_delete'),
    
]