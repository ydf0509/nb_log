

def generate_error_file_name(log_filename: str):
    if log_filename is None:
        return None
    arr = log_filename.split('.')
    part1 = '.'.join(arr[:-1])
    part2 = arr[-1]
    return f'{part1}.error.{part2}'