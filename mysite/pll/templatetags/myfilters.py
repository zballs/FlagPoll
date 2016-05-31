from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
	return value.as_widget(attrs={'class': arg})

@register.filter(name='placeholder')
def placeholder(field, args=None):
	if args == None:
		return field
	field.field.widget.attrs.update({"placeholder": args })
	return field

@register.filter(name='shortTimeSince')
def shortTimeSince(value):
	return value.partition(",")[0]