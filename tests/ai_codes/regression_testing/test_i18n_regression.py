"""
Regression test for the i18n (internationalization) changes.
Verifies that all core nb_log functionality works after translating Chinese to English.
"""
import os
import sys
import re
import logging
import tempfile
import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def test_no_chinese_in_nb_log_source():
    """Verify no Chinese characters remain in nb_log source files."""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    nb_log_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'nb_log')
    nb_log_dir = os.path.abspath(nb_log_dir)

    failures = []
    for root, dirs, files in os.walk(nb_log_dir):
        for f in files:
            if f.endswith('.py'):
                filepath = os.path.join(root, f)
                with open(filepath, encoding='utf-8') as fh:
                    for i, line in enumerate(fh, 1):
                        if chinese_pattern.search(line):
                            failures.append(f'{filepath}:{i}: {line.strip()}')

    if failures:
        print(f'FAIL: Found {len(failures)} lines with Chinese characters:')
        for f in failures:
            print(f'  {f}')
        return False
    else:
        print('PASS: No Chinese characters found in nb_log source files.')
        return True


def test_import_nb_log():
    """Verify nb_log can be imported without errors."""
    try:
        import nb_log
        print('PASS: nb_log imported successfully.')
        return True
    except Exception as e:
        print(f'FAIL: nb_log import failed: {e}')
        return False


def test_get_logger():
    """Verify basic get_logger functionality."""
    try:
        import nb_log
        logger = nb_log.get_logger('test_i18n_regression')
        logger.debug('Debug test message')
        logger.info('Info test message')
        logger.warning('Warning test message')
        logger.error('Error test message')
        print('PASS: get_logger works correctly.')
        return True
    except Exception as e:
        print(f'FAIL: get_logger failed: {e}')
        return False


def test_log_manager():
    """Verify LogManager class functionality."""
    try:
        import nb_log
        lm = nb_log.LogManager('test_log_manager_i18n')
        logger = lm.get_logger_and_add_handlers(log_level_int=logging.DEBUG)
        logger.info('LogManager test message')
        print('PASS: LogManager works correctly.')
        return True
    except Exception as e:
        print(f'FAIL: LogManager failed: {e}')
        return False


def test_log_manager_with_file():
    """Verify LogManager with file handler."""
    try:
        import nb_log
        tmp_dir = tempfile.mkdtemp()
        lm = nb_log.LogManager('test_file_i18n')
        logger = lm.get_logger_and_add_handlers(
            log_level_int=logging.DEBUG,
            log_path=tmp_dir,
            log_filename='test_i18n.log'
        )
        logger.info('File handler test message')
        print('PASS: LogManager with file handler works correctly.')
        return True
    except Exception as e:
        print(f'FAIL: LogManager with file handler failed: {e}')
        return False


def test_compatible_logger():
    """Verify CompatibleLogger works."""
    try:
        import nb_log
        from nb_log.loggers_imp.compatible_logger import CompatibleLogger
        lm = nb_log.LogManager('test_compatible_i18n', logger_cls=CompatibleLogger)
        logger = lm.get_logger_and_add_handlers()
        logger.info('CompatibleLogger test message')
        print('PASS: CompatibleLogger works correctly.')
        return True
    except Exception as e:
        print(f'FAIL: CompatibleLogger failed: {e}')
        return False


def test_direct_logger():
    """Verify direct logging functions."""
    try:
        import nb_log
        nb_log.debug('Direct debug test')
        nb_log.info('Direct info test')
        nb_log.warning('Direct warning test')
        nb_log.error('Direct error test')
        print('PASS: Direct logging functions work correctly.')
        return True
    except Exception as e:
        print(f'FAIL: Direct logging failed: {e}')
        return False


def test_check_log_level():
    """Verify log level validation with English error message."""
    try:
        from nb_log.log_manager import check_log_level
        try:
            check_log_level(999)
            print('FAIL: check_log_level should have raised ValueError.')
            return False
        except ValueError as e:
            error_msg = str(e)
            if 'Invalid log level' in error_msg:
                print('PASS: check_log_level raises English error message.')
                return True
            else:
                print(f'FAIL: Unexpected error message: {error_msg}')
                return False
    except Exception as e:
        print(f'FAIL: check_log_level test failed: {e}')
        return False


def test_formatter_template_validation():
    """Verify formatter template validation with English error message."""
    try:
        import nb_log
        try:
            nb_log.LogManager('test_fmt_i18n').get_logger_and_add_handlers(
                formatter_template='invalid'
            )
            print('FAIL: Should have raised ValueError for invalid formatter.')
            return False
        except ValueError as e:
            error_msg = str(e)
            if 'Invalid formatter_template' in error_msg:
                print('PASS: formatter_template validation has English error message.')
                return True
            else:
                print(f'FAIL: Unexpected error message: {error_msg}')
                return False
    except Exception as e:
        print(f'FAIL: formatter validation test failed: {e}')
        return False


def test_log_file_handler_type_validation():
    """Verify log_file_handler_type validation."""
    try:
        import nb_log
        try:
            nb_log.LogManager('test_handler_type_i18n').get_logger_and_add_handlers(
                log_file_handler_type=99
            )
            print('FAIL: Should have raised ValueError.')
            return False
        except ValueError as e:
            error_msg = str(e)
            if 'must be one of' in error_msg:
                print('PASS: log_file_handler_type validation has English error message.')
                return True
            else:
                print(f'FAIL: Unexpected error message: {error_msg}')
                return False
    except Exception as e:
        print(f'FAIL: handler type validation test failed: {e}')
        return False


def test_default_loggers():
    """Verify pre-built loggers exist."""
    try:
        import nb_log
        assert nb_log.simple_logger is not None, 'simple_logger is None'
        assert nb_log.default_logger is not None, 'default_logger is None'
        assert nb_log.defaul_logger is not None, 'defaul_logger backward compat is None'
        assert nb_log.default_file_logger is not None, 'default_file_logger is None'
        assert nb_log.logger_dingtalk_common is not None, 'logger_dingtalk_common is None'
        print('PASS: All pre-built loggers exist.')
        return True
    except Exception as e:
        print(f'FAIL: Pre-built loggers test failed: {e}')
        return False


def run_all_tests():
    results = []
    tests = [
        test_no_chinese_in_nb_log_source,
        test_import_nb_log,
        test_get_logger,
        test_log_manager,
        test_log_manager_with_file,
        test_compatible_logger,
        test_direct_logger,
        test_check_log_level,
        test_formatter_template_validation,
        test_log_file_handler_type_validation,
        test_default_loggers,
    ]

    for test_func in tests:
        print(f'\n--- Running {test_func.__name__} ---')
        result = test_func()
        results.append((test_func.__name__, result))

    print('\n' + '=' * 60)
    print('REGRESSION TEST SUMMARY')
    print('=' * 60)
    passed = sum(1 for _, r in results if r)
    failed = sum(1 for _, r in results if not r)
    for name, result in results:
        status = 'PASS' if result else 'FAIL'
        print(f'  [{status}] {name}')
    print(f'\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}')

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
