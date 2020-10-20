"""
ModelAdmin for the BaseConfig model.

Notes:
    There is no simple way of hiding the "Save and add another" button
    when adding a Settings instance. Since there will never be more than
    one instance for a given model we take the easy way out and simply
    hide the button in css. The alternative is something along the lines
    of https://stackoverflow.com/questions/49560378/

TODO:
    * See if using get_urls to override the changelist url to display the
      change url is better than redirecting to the change view.
    * See what happens to the admin views when the settings object gets
      deleted. The code creates the object on demand but it would be
      better if this condition was recoverable within the Django Admin.
    * Since we're overriding part of the change form why not include the
      css needed to hide the save and continue button there.

"""
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseConfigAdmin(admin.ModelAdmin):
    object_history_template = "admin/config/object_history.html"
    change_form_template = "admin/config/change_form.html"

    class Media:
        css = {"all": ("css/admin/settings.css",)}

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj is not None:
            return self.change_view(
                request, str(obj.id), form_url="", extra_context=extra_context
            )
        return super(BaseConfigAdmin, self).changelist_view(request, extra_context)

    def response_post_save_change(self, request, obj):
        list(messages.get_messages(request))
        messages.info(request, _("The settings were updated successfully."))
        post_url = reverse("admin:index", current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_changeform_initial_data(self, request):
        """
        Get the initial data for the change form.

        Notes:
            The change form is generated by modelform_factory. Although
            the defaults contains a value for the primary key it will not
            be used. To avoid generating multiple instances the primary
            key is explicitly set in the model save() method.

        """
        return self.model.get_defaults()