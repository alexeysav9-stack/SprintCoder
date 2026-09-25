from django.contrib import admin
from .models import Language, Snippet, Attempt


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'icon')


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'line_count', 'created_at')
    list_filter = ('language', 'difficulty')
    search_fields = ('title', 'code')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'snippet', 'wpm', 'cpm', 'accuracy', 'time_seconds', 'created_at')
    list_filter = ('snippet__language', 'snippet__difficulty')
    readonly_fields = ('errors_json',)
