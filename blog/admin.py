from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile, Oil, LikeOil
# Register your models here.


class UserAdminPage(UserAdmin):

  def has_delete_permission(self, request, obj=None):
    return False

  def get_actions(self, request):
      actions = super(UserAdminPage, self).get_actions(request)
      if 'delete_selected' in actions:
          del actions['delete_selected']
      return actions


class UserProfileAdmin(admin.ModelAdmin):
  fields = ["user", "role", "kudo"]
  list_display = ["user", "role", "kudo"]
  list_editable = ["role", "kudo"]
  list_filter = ["role"]
  search_fields = ["user"]

  def has_delete_permission(self, request, obj=None):
        return False

  def get_actions(self, request):
        actions = super(UserProfileAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class OilAdmin(admin.ModelAdmin):
  fields = ["date", "title", "tag", "question", "anwser", "resource"]
  list_display = ["title", "tag", "date", "contributor", "editor", "state", "kudo"]
  list_editable = ["state", "kudo"]
  list_filter = ["date", "state"]
  search_fields = ["title", "question", "anwser"]
  actions = ['approve', 'approve_with_edit', 'not_approve']

  def approve(self, request, querryset):
    rows_updated = querryset.update(state="approve", on_payroll=True)
    message_bit = "1 blog was"
    if rows_updated != 1:
      message_bit = f"{rows_updated} blogs were"
    self.message_user(request, f"{message_bit} successfully approved")
  approve.short_description = "Approve selected blogs"

  def approve_with_edit(self, request, querryset):
    rows_updated = querryset.update(state="approve with edit", on_payroll=True)
    message_bit = "1 blog was"
    if rows_updated != 1:
      message_bit = f"{rows_updated} blogs were"
    self.message_user(request, f"{message_bit} successfully approved")
  approve_with_edit.short_description = "Approve with edit selected blogs"

  def not_approve(self, request, querryset):
    rows_updated = querryset.update(state="not approve", on_payroll=False)
    message_bit = "1 blog was"
    if rows_updated != 1:
      message_bit = f"{rows_updated} blogs were"
    self.message_user(request, f"{message_bit} successfully disapproved")
  not_approve.short_description = "Disapprove selected blogs"

  def save_model(self, request, obj, form, change):
    current_user = UserProfile.objects.get(user=request.user)
    if obj.id is None:
      obj.contributor = current_user
    else:
      obj.editor = current_user

    if obj.state in ("approve", "approve with edit"):
      obj.on_payroll = True
    elif obj.state == "not approve":
      obj.on_payroll = False

    super(OilAdmin, self).save_model(request, obj, form, change)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Oil, OilAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdminPage)