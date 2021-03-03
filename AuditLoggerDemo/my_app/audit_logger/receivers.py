# These are the signals handlers that fetch and feed old and new instance data to the python logger.

from audit_logger.logger import AuditLogger
from django.conf import settings
from audit_logger.middleware import get_latest_request

audit_log_format = settings.AUDIT_LOG_FORMAT
audit_log_level = settings.AUDIT_LOG_LEVEL


audit = AuditLogger(audit_log_format, audit_log_level)


def _current_user():
    request = get_latest_request()
    return request.user if hasattr(request, 'user') else None


class Receivers:
    old_instance = None  # closure function
    old_m2m_instances = None


def _capture_old_instances(sender, instance):
    try:
        old = sender.objects.get(pk=instance.id)
    except sender.DoesNotExist:
        old = None

    def _closure():
        return old

    Receivers.old_instance = _closure


def presave(sender, instance, raw, using, update_fields, **kwargs):
    _capture_old_instances(sender, instance)


def predelete(sender, instance, using, **kwargs):
    _capture_old_instances(sender, instance)


def postdelete(sender, instance, using, **kwargs):
    request = get_latest_request()

    if not request:
        return ''

    actor = _current_user()
    old = Receivers.old_instance()

    try:
        new = sender.objects.get(pk=instance.id)  # not expected, could be used to verify
    except sender.DoesNotExist:
        new = None  # expected

    message = audit.log_action(actor, request, "DELETED", old, new)

    return message


def postsave(sender, instance, created, raw, using, update_fields, **kwargs):
    request = get_latest_request()

    if not request:
        return ''

    actor = _current_user()
    old = Receivers.old_instance()
    new = sender.objects.get(pk=instance.id)
    action = "CREATED" if created else "UPDATED"

    message = audit.log_action(actor, request, action, old, new)

    return message


# https://docs.djangoproject.com/en/3.1/ref/signals/#django.db.models.signals.m2m_changed
def m2mchanged(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    """Dependent upon url structure Ex, /applications/1/exceptions/ yields 'exceptions' as the target m2m field"""
    actor = _current_user()
    request = get_latest_request()

    if not request:
        return ''

    if action in ['pre_add', 'post_add']:
        m2m_field_name = request.path.split('/')[-2]
    else:
        m2m_field_name = request.path.split('/')[-3]

    m2m_field_target = getattr(instance, m2m_field_name, None)

    # guard for mismatched path (the m2m field name) in the request during testing
    if not m2m_field_target:
        return ''

    if action in ['pre_remove', 'pre_add']:
        _capture_old_instances(m2m_field_target)

    elif action in ['post_remove', 'post_add']:
        new_m2m_instances = [str(row) for row in m2m_field_target.all()]
        old_m2m_instances = Receivers.old_m2m_instances()

        if action == 'post_remove':
            audit.log_action(actor, request, "DELETED", old_m2m_instances, new_m2m_instances, m2ms=True)
        else:
            audit.log_action(actor, request, "CREATED", old_m2m_instances, new_m2m_instances, m2ms=True)

