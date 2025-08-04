from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings
from django.views.generic import CreateView
from users.forms import CustomUserCreationForm
from django.conf.urls.static import static


handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'


urlpatterns = [
	path('', include('blog.urls')),
	path('admin/', admin.site.urls),
	path('auth/', include('django.contrib.auth.urls')),
	path('auth/registration/', CreateView.as_view(
			template_name='registration/registration_form.html',
			form_class=CustomUserCreationForm,
			success_url=reverse_lazy('blog:post_list'),
		),
		name='registration',
		),
	path('pages/', include('pages.urls')),
]


if settings.DEBUG:
	import debug_toolbar
	urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
