import logging
from .Setting import base_dir
def setup_logger():
    # 配置日志记录器和处理器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)#全局等级设置

    # 创建文件处理器
    file_handler = logging.FileHandler( base_dir + '\\error.log',encoding = 'utf-8')
    file_handler.setLevel(logging.ERROR)#输出文件等级设置
    
    # 创建一个StreamHandler对象
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # 创建日志格式器
    formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s' )

    # 将格式器添加到文件处理器
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 将文件处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

#全局日志配置
def basicConfig():
    logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='%(asctime)s - %(filename)s:%(lineno)d \
    - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)
    
# 在模块加载时进行日志初始化
logger_error = setup_logger()

