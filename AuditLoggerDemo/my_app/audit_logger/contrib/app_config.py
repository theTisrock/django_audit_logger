from django.db.models.signals import pre_save, pre_delete, post_save, post_delete, m2m_changed
from django.apps import AppConfig
from audit_logger import receivers


class AuditLogEnabledAppConfig(AppConfig):

    def ready(self):
        """Connect the audit logger to this app."""
        for model in self.get_models():
            # register model-level signals
            pre_save.connect(receivers.presave, sender=model, weak=False, dispatch_uid=f"{model.__name__}_presave")
            pre_delete.connect(receivers.predelete, sender=model, weak=False, dispatch_uid=f"{model.__name__}_predel")
            post_save.connect(receivers.postsave, sender=model, weak=False, dispatch_uid=f"{model.__name__}_postsave")
            post_delete.connect(receivers.postdelete, sender=model, weak=False, dispatch_uid=f"{model.__name__}_postdel")

            # register many to many fields of model - EXPERIMENTAL
            m2m_field_names = []
            for m2m in model._meta.many_to_many:
                m2m_field = getattr(model, m2m.name)
                m2m_changed.connect(receivers.m2mchanged, sender=m2m_field.through, weak=False,
                                    dispatch_uid=f"{model.__name__}_{m2m.name}")
