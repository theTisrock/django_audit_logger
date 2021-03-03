import logging
import sys
import json
from audit_logger.model_diff import AuditModelDiff


def clear_log_handlers(logger):
    if logger.handlers:
        for h in logger.handlers[:]:
            h.close()
            logger.removeHandler(h)


class AuditLogger(object):
    """Responsibilities:
    A) encompass simple log functionality accomplished with python's builtin logger.
    B) make request data available - accomplished by accessing middleware
    C) record changes to model instances to stdout and (optionally) to a file - accomplish with model_diff.py
    D) Observing changes to models and model instances by leveraging Django signals."""

    def __init__(self, log_format: str, log_level, **kwargs):
        """
        :param log_format: set in project.settings or django.conf
        :param log_level: sets the log level for this loggger instance
        :param kwargs['file']: Optional file to write to in addition to stdout.

        The python logger underneath is a singleton. Upon instantiation, each instance removes all handlers from the
        logger, then recreates and adds new handlers.

        This is done for testing to release and read/write locks on any previously held temporary audit logging file,
        if one has been specified.
        """

        self.logger = logging.getLogger("audit_logger")
        clear_log_handlers(self.logger)
        self.logger.setLevel(level=log_level)
        self.logfile = kwargs.get('file', None)

        # initialize and add handlers to logger
        self.logger.propagate = 0  # disable duplicate logging by root logger
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(level=log_level)
        formatter = logging.Formatter(log_format)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

        if self.logfile:
            file_handler = logging.FileHandler(self.logfile, mode='a')
            file_handler.setLevel(level=log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_action(self, acting_user, request, action: str, old_record, new_record, m2ms=False):
        log_request = f"{request.method} {request.path}"
        log_actor = f"{acting_user}"
        log_action = f"{action}"

        if m2ms:
            m2m_field_name = request.path.split('/')[-2]  # -1 return ''
            changes = {m2m_field_name: [old_record, new_record]}
            if action == 'DELETED':
                m2m_field_name = request.path.split('/')[-3]
                changes = {m2m_field_name: [old_record, new_record]}
        else:
            changes = AuditModelDiff.model_instance_diff(old_record, new_record)

        log_changes = changes
        log_data = dict(actor=log_actor, request=log_request, action=log_action, changes=log_changes)

        self.logger.info(json.dumps(log_data))

        return log_data
