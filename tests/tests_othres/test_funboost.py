

# from funboost import boost,BoosterParams

# @boost('test_queue')
# def add_numbers(x: int, y: int) -> int:
#     return x + y

# if __name__ == '__main__':
#     # Start the consumer
#     add_numbers.consume()

#     result = add_numbers.push(3, 4)
#     print(f"The sum is: {result.result()}")
from funboost import boost, BoosterParams
from funboost.timing_job.apscheduler_use_redis_store import funboost_background_scheduler_redis_store

class MyBoosterParams(BoosterParams):
    max_retry_times: int = 3  # 设置最大重试次数为3次
    function_timeout: int = 10  # 设置超时时间为10秒

@boost(MyBoosterParams(queue_name='add_numbers_queue'))
def add_numbers(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y

if __name__ == '__main__':
    # 定义定时任务
    # Start the scheduler
    funboost_background_scheduler_redis_store.start()

    funboost_background_scheduler_redis_store.add_push_job(
        func=add_numbers,
        args=(1, 2),
        trigger='date',  # 使用日期触发器
        run_date='2025-01-16 16:03:40',  # 设置运行时间
        id='add_numbers_job'  # 任务ID
    )

    # 启动消费者
    add_numbers.consume()
