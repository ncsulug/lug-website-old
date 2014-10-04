from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from .views import ProfileView, DirectoryView, ProfileEditView, RegisterView

account_patterns = patterns('',
    # Edit Profile
    url(r'^edit-profile/$',
        ProfileEditView.as_view(template_name='profiles/edit.html'),
        name='profile_edit'),

    # Registration
    url(r'register/$',
        RegisterView.as_view(template_name='accounts/register.html'),
        name='accounts_register'),

    # Login, Logout
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='accounts_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'accounts/done.html',
         'extra_context': {'action': 'logged out'}},
        name='accounts_logout'),

    # Change Password
    url(r'^password/change/$',
        auth_views.password_change,
        {'template_name': 'accounts/password_change_form.html'},
        name='accounts_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'accounts/done.html',
         'extra_context': {'action': 'password changed'}},
        name='accounts_password_change_done'),

    # Reset Password
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'template_name': 'accounts/password_reset.html',
         'email_template_name': 'accounts/password_reset_email.txt',
         'subject_template_name': 'accounts/password_reset_subject.txt'},
        name='accounts_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'accounts/password_reset_confirm.html'},
        name='accounts_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'accounts/done.html',
         'extra_context': {'action': 'password reset'}},
        name='accounts_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'accounts/done.html',
         'extra_context': {'action': 'password reset requested'}},
        name='accounts_password_reset_done'),
)

urlpatterns = patterns('',
    # Profiles, hooray!
    url(r'^~(?P<username>[a-zA-Z0-9_@+.-]+)/$',
        ProfileView.as_view(template_name='profiles/show.html'),
        name='profile'),

    url(r'^directory/',
        DirectoryView.as_view(template_name='profiles/directory.html'),
        name='directory'),

    (r'^accounts/', include(account_patterns)),
)
