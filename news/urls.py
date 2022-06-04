from django.contrib.auth import views
from django.urls import path, include
from .views import *

urlpatterns = [
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('logout/', logout_user, name='logout'),
    path('send_mes/', send_mes, name='send_mes'),
    # path('', index, name='home'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', HomeNews.as_view(), name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', NewsCategory.as_view(), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', AddNews.as_view(), name='add_news'),
]
