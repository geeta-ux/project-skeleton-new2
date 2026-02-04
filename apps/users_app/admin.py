from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User   # THIS WORKS because models.py exists in this app

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User

    list_display = ("email", "name", "is_staff", "is_superuser", "is_admin", "has_psychometric_access")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "has_psychometric_access", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    search_fields = ("email", "name")
    actions = ["provide_psychometric_access", "revoke_psychometric_access"]

    @admin.action(description="Provide Psychometric Access")
    def provide_psychometric_access(self, request, queryset):
        queryset.update(has_psychometric_access=True)
        self.message_user(request, "Access granted to selected users.")

    @admin.action(description="Revoke Psychometric Access")
    def revoke_psychometric_access(self, request, queryset):
        queryset.update(has_psychometric_access=False)
        self.message_user(request, "Access revoked from selected users.")
