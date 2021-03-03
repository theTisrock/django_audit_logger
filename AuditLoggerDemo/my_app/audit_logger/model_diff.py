from django.db.models import Model, NOT_PROVIDED, DateTimeField
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from django.utils.encoding import smart_text


class AuditModelDiff:
    """An independent class for getting the difference of two model instances.
    Code here is a modified for of https://github.com/jjkester/django-auditlog/blob/master/src/auditlog/diff.py"""

    @classmethod
    def track_field(cls, field):
        return not field.many_to_many

    @classmethod
    def get_fields_in_model(cls, instance: Model):
        """Returns the list of fields in the given model instance."""
        return instance._meta.fields
    
    @classmethod
    def get_field_value(cls, obj, field):
        """Gets the value of a given model instance field."""

        if isinstance(field, DateTimeField):
            # DateTimeFields are timezone-aware, so we need to convert the field to its native form before we can
            # accurately compare them for changes.
            try:
                value = field.to_python(getattr(obj, field.name, None))
                if value is not None and settings.USE_TZ and not timezone.is_naive(value):
                    value = timezone.make_naive(value, timezone=timezone.utc)
            except ObjectDoesNotExist:
                value = field.default if field.default is not NOT_PROVIDED else None
        else:
            try:
                value = smart_text(getattr(obj, field.name, None))  # deprecated in django 3.0
            except ObjectDoesNotExist:
                value = field.default if field.default is not NOT_PROVIDED else None

        return value

    @classmethod
    def model_instance_diff(cls, old, new):
        """
        Calculates the difference between two model instances. One of the instances may be 'None' (ie, a newly
        created model or deleted model). This will cause all fields with a value to have changed (from 'None').
        :param old: The old state of the model instance.
        :param new: The new state of the model instance.
        :return: A dictionary with the names of the changed fields as keys and a tuple of the old and new field values.
        """

        diff = {}

        fields = list()
        for m in [old, new]:
            if m:
                fields += AuditModelDiff.get_fields_in_model(m)
        fields = set(fields)

        for field in fields:
            old_value = AuditModelDiff.get_field_value(old, field)
            new_value = AuditModelDiff.get_field_value(new, field)

            if old_value != new_value:
                diff[field.name] = (smart_text(old_value), smart_text(new_value))

        if len(diff) == 0:
            diff = None

        return diff
