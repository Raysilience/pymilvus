import datetime

import pytest
from pymilvus.client.check import check_pass_param
from pymilvus.client.utils import mkts_from_unixtime, mkts_from_datetime, mkts_from_hybridts, \
    hybridts_to_unixtime


class TestCheckPassParam:
    def test_check_pass_param_valid(self):
        a = [[i * j for i in range(20)] for j in range(20)]
        check_pass_param(search_data=a)

        import numpy as np
        a = np.float32([[1, 2, 3, 4], [1, 2, 3, 4]])
        check_pass_param(search_data=a)

    def test_check_param_invalid(self):
        with pytest.raises(Exception):
            a = {[i * j for i in range(20) for j in range(20)]}
            check_pass_param(search_data=a)

        with pytest.raises(Exception):
            a = [{i * j for i in range(40)} for j in range(40)]
            check_pass_param(search_data=a)


class TestGenTS:
    def test_mkts1(self):
        ts = 426152581543231492
        msecs = 1000
        timestamp = hybridts_to_unixtime(ts)
        t1 = mkts_from_hybridts(ts, milliseconds=msecs)
        t2 = mkts_from_unixtime(timestamp, msecs)
        timestamp1 = hybridts_to_unixtime(t1)
        timestamp2 = hybridts_to_unixtime(t2)

        assert timestamp1 == timestamp2

        dtime = datetime.datetime.fromtimestamp(timestamp)
        t3 = mkts_from_datetime(dtime, milliseconds=msecs)
        timestamp3 = hybridts_to_unixtime(t3)
        assert timestamp1 == timestamp3

    def test_mkts2(self):
        ts = 426152581543231492
        delta = datetime.timedelta(milliseconds=1000)
        timestamp = hybridts_to_unixtime(ts)
        t1 = mkts_from_hybridts(ts, delta=delta)
        t2 = mkts_from_unixtime(timestamp, delta=delta)
        timestamp1 = hybridts_to_unixtime(t1)
        timestamp2 = hybridts_to_unixtime(t2)

        assert timestamp1 == timestamp2

        dtime = datetime.datetime.fromtimestamp(timestamp)
        t3 = mkts_from_datetime(dtime, delta=delta)
        timestamp3 = hybridts_to_unixtime(t3)
        assert timestamp1 == timestamp3