
def remove_placeholders(form):
    for field_name in form.fields:
        attrs = form.fields[field_name].widget.attrs
        if "placeholder" in attrs:
            del attrs["placeholder"]
