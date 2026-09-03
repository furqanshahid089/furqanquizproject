from django.contrib import admin

from .models import Category, Subcategory, Question, QuizResult, QuizAnswer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'display_order')
    list_filter = ('category',)
    search_fields = ('name',)
    list_select_related = ('category',)
    ordering = ('category', 'display_order', 'name')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'category', 'subcategory', 'answer')
    list_filter = ('category', 'subcategory')
    search_fields = ('question',)
    list_select_related = ('category',)


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 0
    can_delete = False
    readonly_fields = (
        'question',
        'selected_answer',
        'is_correct'
    )


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'category',
        'subcategory',
        'score',
        'total_questions',
        'percentage',
        'completed_at'
    )
    list_filter = ('category', 'completed_at')
    search_fields = ('user__username', 'category__name')
    readonly_fields = (
        'user',
        'category',
        'subcategory',
        'score',
        'total_questions',
        'percentage',
        'completed_at'
    )
    inlines = [QuizAnswerInline]
