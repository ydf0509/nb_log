


from pathlib import Path

from chained_mode_time_tool import DatetimeConverter



# (Path('/pythonlogs') / Path(f'{DatetimeConverter().date_str}.0002.tn.log')).touch()


for f in Path('/pythonlogs').glob('????-??-??.????.tn.log'):
    print(f.name)
    print(f.stat().st_mtime)

print(Path('/pythonlogs/2023-07-09.0002.tn.log').stat())


print(int('002'))