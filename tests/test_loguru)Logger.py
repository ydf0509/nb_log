
import pymysql

from loguru import logger

# 创建Logger实例
log = logger.Logger()

# 添加日志处理器
log.add("logs/mylog_{time}.log", rotation="500 MB")

# 记录日志消息
log.info("This is a log message")

# 记录带有上下文信息的日志消息
log.bind(user="John").info("User logged in")

# 记录异常信息
try:
    # 一些可能引发异常的代码
    raise ValueError("Something went wrong")
except Exception as e:
    log.exception(e)