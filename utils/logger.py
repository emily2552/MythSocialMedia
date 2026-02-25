import logging

# 创建全局 logger
logger = logging.getLogger("global_logger")
logger.setLevel(logging.DEBUG)  # 设定最低级别为 DEBUG

# 创建控制台 handler 并设置级别
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 日志输出格式（可根据需要调整）

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - "
    "%(filename)s:%(lineno)d - %(funcName)s() - %(message)s"
)
ch.setFormatter(formatter)

# 避免重复添加 handler
if not logger.handlers:
    logger.addHandler(ch)

# 也可以在这里配置日志写入文件，例如：
# fh = logging.FileHandler("app.log")
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# logger.addHandler(fh)
