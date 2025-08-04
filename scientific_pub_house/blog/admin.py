from django.contrib import admin
from .models import Magazine, Post, User


class PostAdmin(admin.ModelAdmin):
	list_display = (
		'title',
		'text',
		'is_published',
		'magazine',
		'author',
		'pub_date',
		'created_at'
	)
	list_editable = (
		'is_published',
	)
	search_fields = ('title', 'text', 'pub_date')
	list_filter = ('magazine',)


class PostInline(admin.TabularInline):
	model = Post
	extra = 0


class MagazineAdmin(admin.ModelAdmin):
	inlines = (
		PostInline,
	)
	list_display = (
		'title',
		'is_published'
	)
	list_editable = (
		'is_published',
	)


class UserAdmin(admin.ModelAdmin):
	list_display = (
		'username',
		'email',
	)


admin.site.empty_value_display = 'Не задано'
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
