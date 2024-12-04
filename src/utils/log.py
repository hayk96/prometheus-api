from pythonjsonlogger import jsonlogger
from .arguments import arg_parser
from datetime import datetime
import logging


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(
            CustomJsonFormatter,
            self).add_fields(
            log_record,
            record,
            message_dict)
        if not log_record.get("timestamp"):
            now = datetime.now().strftime("%d %b %Y %H:%M:%S")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


# class LoggerAPI:
#     def __init__(self):
#         self.msg = msg
#         self.msg = msg
#     def
#
#         logger.info(
#             msg=msg,
#             extra={
#                 "status": response.status_code,
#                 "method": request.method,
#                 "request_path": f"{request.url.path}{'?' + request.url.query if request.url.query else ''}"})


logger = logging.getLogger(__name__)
log_level_from_args = arg_parser().get("log.level")
logger.setLevel(log_level_from_args.upper())
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomJsonFormatter("%(timestamp)s %(level)s %(message)s"))
logger.addHandler(console_handler)
