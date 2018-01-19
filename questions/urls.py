
from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hot/$', views.hot_questions, name='hot'),
    url(r'^tag/(?P<tag>\w+)', views.questions_by_tag, name='tag'),
    url(r'^question/(?P<question_number>\d+)', views.single_question, name='question'),
    url(r'^login/$', views.signin, name='signin'),
    url(r'^register/$', views.signup, name='signup'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^create-author/$', views.create_author, name="create-author"),
    url(r'^create-answer/$', views.create_answer, name="create-answer"),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^vote/$', views.vote),
    url(r'^logout/$', views.log_out, name="logout")
]