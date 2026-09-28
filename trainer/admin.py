from django.contrib import admin
from .models import Language, Snippet, Attempt, UserProfile, SiteVisit

admin.site.site_header = "SprintCoder — Панель управления"
admin.site.site_title = "SprintCoder Admin"
admin.site.index_title = "Управление платформой и базой знаний"


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'icon')


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'imported_by', 'line_count', 'created_at')
    list_filter = ('language', 'difficulty', 'imported_by')
    search_fields = ('title', 'code')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'snippet', 'wpm', 'cpm', 'accuracy', 'time_seconds', 'created_at')
    list_filter = ('snippet__language', 'snippet__difficulty')
    readonly_fields = ('errors_json',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_import_at')
    search_fields = ('user__username',)
    readonly_fields = ('last_import_at',)


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'path', 'user', 'device_type', 'browser', 'ip_address', 'status_code')
    list_filter = ('device_type', 'browser', 'status_code', 'timestamp')
    search_fields = ('path', 'ip_address', 'user__username', 'user_agent')
    readonly_fields = (
        'timestamp', 'path', 'ip_address', 'user', 'session_key',
        'user_agent', 'device_type', 'browser', 'referer', 'status_code'
    )
    date_hierarchy = 'timestamp'

