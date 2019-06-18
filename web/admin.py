from django.contrib import admin
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from web.models import Origin, DemoUser


@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):

    def changeform_view(
            self,
            request,
            object_id=None,
            form_url='',
            extra_context=None
    ):
        extra_context = extra_context or {}

        if object_id:
            origin_obj = Origin.objects.filter(id=object_id).first()
            if origin_obj:
                extra_context['user_id'] = origin_obj.user_id
                extra_context['username'] = origin_obj.user.username if origin_obj.user else ''

        return super(OriginAdmin, self).changeform_view(
            request, object_id, form_url, extra_context
        )

    def user_count(self, obj):
        ggacUserRegisterCounts = DemoUser.objects.filter(origin=obj.id).values('origin').count()
        return ggacUserRegisterCounts
    user_count.short_description = '注册用户'

    def origin_url(self, obj):
        if obj.id is not None:
            return 'http://localhost/?origin=' + str(obj.id)
        else:
            return '(保存后可见)'
    origin_url.short_description = '渠道链接'

    readonly_fields = ('origin_url', )
    fields = ('origin_name', 'user', 'origin_url')
    list_display = ('origin_name', 'user_count', 'user')
    search_fields = ('user__username', 'user__mobile')

    change_form_template = loader.get_template('web/admin/change_form_origin.html')


@admin.register(DemoUser)
class DemoUserAdmin(admin.ModelAdmin):
    list_display = ('username',  'origin', 'is_active',)
    list_filter = ('origin__origin_name', 'groups', 'is_staff', 'is_active')
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': (
        'username', 'password', 'email',)}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
