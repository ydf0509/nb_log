from nb_log import get_logger
import time
import random

# 创建一个logger实例
logger = get_logger('nb_log_demo', log_path='logs')

def simulate_task():
    """模拟一个任务，生成不同级别的日志"""
    # 记录一些信息日志
    logger.info('开始执行任务')
    
    # 模拟一些处理过程
    for i in range(3):
        # 记录调试信息
        logger.debug(f'正在处理第 {i+1} 步')
        
        # 随机模拟一些警告情况
        if random.random() < 0.3:
            logger.warning(f'第 {i+1} 步出现了一些警告情况')
            
        # 随机模拟一些错误情况
        if random.random() < 0.1:
            try:
                raise ValueError(f'第 {i+1} 步发生错误')
            except Exception as e:
                logger.error(f'处理过程出错: {str(e)}', exc_info=True)
        
        time.sleep(1)  # 模拟处理时间
    
    # 记录完成信息
    logger.info('任务执行完成')

if __name__ == '__main__':
    # 运行几次任务来生成不同的日志
    for _ in range(3):
        simulate_task()
        time.sleep(2)  # 任务之间的间隔
