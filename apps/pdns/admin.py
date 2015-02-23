from django.contrib import admin
from .models import Domain, DomainUsers, Record, UserLimit, DomainTemplate, RecordTemplate
from .forms import RecordInlineForm, DomainCreateForm

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


def remove_from_fieldsets(fieldsets, fields):
    for fieldset in fieldsets:
        for field in fields:
            if field in fieldset[1]['fields']:
                new_fields = []
                for new_field in fieldset[1]['fields']:
                    if not new_field in fields:
                        new_fields.append(new_field)

                fieldset[1]['fields'] = tuple(new_fields)
                break

    return fieldsets


class RecordInline(admin.TabularInline):
    model = Record
    extra = 0
    form = RecordInlineForm
    fieldsets = (
            (None, {
                'fields': [ 'name', 'type', 'content', 'ttl', 'prio', 'add_ptr', 'disabled' ]
                }),
            )

class DomainUsersInline(admin.TabularInline):
    model = DomainUsers

class DomainAdmin(admin.ModelAdmin):
    inlines = [ RecordInline, ]
    list_display = [ 'name', 'type' ]
    fieldsets = (
            (None, {
                'fields': ( 'name', 'type', 'users' )
                }),
            ('Slave options', {
                'classes': ('collapse',),
                'fields': [ 'master' ]
                }),
            )

    add_fieldsets = (
            (None, {
                'fields': ( 'name', 'type', 'template', 'users' )
                }),
            )

    add_form = DomainCreateForm

    def get_formsets(self, request, obj=None):
        if obj:
            for _ in super(DomainAdmin, self).get_formsets(request, obj):
                yield _


    def get_fieldsets(self, request, obj=None):
        fieldsets = super(DomainAdmin, self).get_fieldsets(request, obj)
        if not obj:
            fieldsets = self.add_fieldsets
        if not request.user.is_superuser:
            fieldsets = remove_from_fieldsets(fieldsets, ['users'])
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(DomainAdmin, self).get_form(request, obj, **defaults)

    def save_related(self, request, form, formsets, change):
        super(DomainAdmin, self).save_related(request, form, formsets, change)
        form.instance.users.add(request.user)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if instance.type == 'A':
                ptr_dom = u'%s.in-addr.arpa' % '.'.join(reversed(instance.content.split('.')[0:3]))
                ptr_full = u'%s.in-addr.arpa' % '.'.join(reversed(instance.content.split('.')))
                try:
                    domptr = Domain.objects.get(name=ptr_dom)
                except:
                    domptr = False

                if domptr:
                    ptr_record, created = Record.objects.get_or_create(domain=domptr, name=ptr_full, type='PTR', content=instance.name)


        formset.save()

    def save_model(self, request, obj, form, change):
        super(DomainAdmin, self).save_model(request, obj, form, change)
        if 'template' in form.cleaned_data:
            template = form.cleaned_data['template']
            for rt in RecordTemplate.objects.filter(template=template):
                r, created = Record.objects.get_or_create(domain=obj, name=rt.name.replace('[ZONE]',obj.name), type=rt.type, content=rt.content.replace('[ZONE]',obj.name), prio=rt.prio, ttl=rt.ttl)

    def get_queryset(self, request):
        qs = super(DomainAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(users=request.user)

    

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
