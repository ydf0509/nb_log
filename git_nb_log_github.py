import subprocess

import time

def getstatusoutput(cmd):
    try:
        data = subprocess.check_output(cmd, shell=True, universal_newlines=True,
                                       stderr=subprocess.STDOUT, encoding='utf8')  # 必須設置為utf8， 不然报错了。
        exitcode = 0
    except subprocess.CalledProcessError as ex:
        data = ex.output
        exitcode = ex.returncode
    if data[-1:] == '\n':
        data = data[:-1]
    return exitcode, data

def do_cmd(cmd_strx):
    print(f'执行 {cmd_strx}')
    retx = getstatusoutput(cmd_strx)
    print(retx[0])
    # if retx[0] !=0:
    #     raise ValueError('要检查git提交')
    print(retx[1], '\n')
    return retx

t0 = time.time()

do_cmd('git pull origin')

do_cmd('git diff')

do_cmd('git add ./.')

do_cmd('git commit -m commit')


do_cmd('git push origin')
# do_cmd('git push github')

# print(subprocess.getstatusoutput('git push github'))
print(f'spend_time {time.time() - t0}')

if __name__ == '__main__':

    time.sleep(1000000)






