"""
>>pytest test_cal.py -s --cov=program --cov-report term-missing
"""
import pytest

import program.calculator as cal


is_release = True

class TestCal(object):

    @classmethod
    def setup_class(cls):
        print('start')
        cls.cal = cal.Cal()

    @classmethod
    def teardown_class(cls):
        print('end')
        del cls.cal

    def setup_method(self, method):
        print('method={}'.format(method.__name__))

    def teardown_method(self, method):
        print('method={}'.format(method.__name__))

    def test_add_num_and_double(self):
        assert self.cal.add_num_and_double(1, 1) == 4
        assert self.cal.add_num_and_double(5, 4) == 18
        assert self.cal.add_num_and_double(10, 20) == 60

    @pytest.mark.skipif(is_release==True, reason="skip test!")
    def test_add_num_and_double_skip(self):
        assert self.cal.add_num_and_double(20, 10) == 60

    def test_add_num_and_double_raise(self):
        with pytest.raises(ValueError):
            self.cal.add_num_and_double('1', '1')
