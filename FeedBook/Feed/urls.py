from django.urls import path
from Feed import views
urlpatterns = [
    # display all messages
    path("feed", views.home, name='home'),

    # crud operations on feeed
    path('send-message',views.create_new_message,name= 'create'),
    path('delete-message/<int:id>', views.delete_message,name='delete'),
    path('view-message/<int:id>',views.view_message,name='view'),
    path('update-message/<int:id>',views.update_message,name='update'),


    # path for adding comment
    path('add_comment',views.add_comment,name='add_comment'),


    # account related urls
    path("login", views.login_fun, name="login"),
    path("register", views.register_fun, name="register"),
    path("logout", views.logout_fun, name="logout"),
]