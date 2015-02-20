from django.contrib import admin
from .models import Domain, DomainUsers, Record, UserLimit, DomainTemplate, RecordTemplate
from .forms import RecordInlineForm, DomainCreateForm

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class RecordInline(admin.TabularInline):
    model = Record
    extra = 0
    form = RecordInlineForm
    fieldsets = (
            (None, {
                'fields': [ 'name', 'type', 'content', 'ttl', 'prio', 'disabled' ]
                }),
            )

class DomainUsersInline(admin.TabularInline):
    model = DomainUsers

class DomainAdmin(admin.ModelAdmin):
    inlines = [ RecordInline, DomainUsersInline, ]
    list_display = [ 'name', 'type' ]
    fieldsets = (
            (None, {
                'fields': ( 'name', 'type' )
                }),
            ('Slave options', {
                'classes': ('collapse',),
                'fields': [ 'master' ]
                }),
            )

    add_fieldsets = (
            (None, {
                'fields': ( 'name', 'type', 'template' )
                }),
            )

    add_form = DomainCreateForm

    def get_formsets(self, request, obj=None):
        if obj:
            for _ in super(DomainAdmin, self).get_formsets(request, obj):
                yield _

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(DomainAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(DomainAdmin, self).get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change):
        obj.save()
        if 'template' in form.cleaned_data:
            template = form.cleaned_data['template']
            for rt in RecordTemplate.objects.filter(template=template):
                r, created = Record.objects.get_or_create(domain=obj, name=rt.name, type=rt.type, content=rt.content, prio=rt.prio, ttl=rt.ttl)


    

class UserLimitInline(admin.StackedInline):
    model = UserLimit
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = ( UserLimitInline, )


class RecordTemplateInline(admin.TabularInline):
    model = RecordTemplate

class DomainTemplateAdmin(admin.ModelAdmin):
    inlines = ( RecordTemplateInline, )

admin.site.register(Domain, DomainAdmin)
admin.site.register(DomainTemplate, DomainTemplateAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
