


from nb_log.log_manager import LoggedException,logged_raise

try :
    1/0
except Exception as e:
    logged_raise(ZeroDivisionError('0不能是被除数'))


# def f():
#     try :
#         1/0
#     except Exception as e:
#         raise LoggedException(message='有问题',)
#
# for  i  in range(10):
#     try:
#         f()
#     except Exception as e:
#         pass
        # print(e)

# class MyEXc(Exception):
#     def __init__(self,a,b):
#         self.a = a
#         self.b =b
#
#
# raise MyEXc(1,2)
