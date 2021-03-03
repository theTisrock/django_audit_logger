from django.apps import AppConfig
from audit_logger.contrib.app_config import AuditLogEnabledAppConfig


class TodoListConfig(AuditLogEnabledAppConfig):
    name = 'todo_list'
