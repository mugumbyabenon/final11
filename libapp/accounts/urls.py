from  django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',views.register,name='register'),
    #path('student_register/', views.student_register.as_view(), name = 'student_register'),
    path('librarain_register/', views.librarain_register, name = 'librarain_register'),
    path('login/', views.login_view, name='login'),
    path('librarain/', views.librarain, name='librarain'),
    path('student/', views.student, name='student'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uid64>/<token>', views.activate, name="activate"),
    path('resend/', views.resend),
    path('reset_r/', auth_views.PasswordResetView.as_view(template_name='passwordchange.html'), name='reset_password'),
    path('accountspassword_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='passwordreset.html'), name='password_reset_done'),
    path('accountsreset//<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='setnewpassword.html'), name='password_reset_confirm'),
    path('accountsreset/done/', auth_views.PasswordResetView.as_view(template_name='newpassword.html'), name='password_reset_complete'),
]