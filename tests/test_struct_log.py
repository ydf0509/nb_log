
import logging
import structlog

# 配置标准日志记录器
logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = structlog.get_logger()

# 使用结构化日志
logger.info("user_logged_in", user_id=123, user_name="Alice")
logger.error("user_login_failed", user_id=123, reason="Invalid password")


print(7/4)