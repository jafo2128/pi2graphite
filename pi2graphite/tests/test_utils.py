"""
The latest version of this package is available at:
<http://github.com/jantman/webhook2lambda2sqs>

################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of webhook2lambda2sqs, also known as webhook2lambda2sqs.

    webhook2lambda2sqs is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    webhook2lambda2sqs is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with webhook2lambda2sqs.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/webhook2lambda2sqs> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""
import sys
import pytest
import json

from pi2graphite.utils import pretty_json, read_json_file
from pi2graphite.tests.support import exc_msg

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT, mock_open  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT, mock_open  # noqa

pbm = 'pi2graphite.utils'


class TestUtils(object):

    def test_pretty_json(self):
        obj = {
            'foo': 'bar',
            'baz': 12,
            'blam': [
                {'one': 2}
            ]
        }
        assert pretty_json(obj) == json.dumps(obj, sort_keys=True, indent=4)

    def test_read_json_file(self):
        val = {'foo': 'bar', 'baz': 2}
        content = json.dumps(val)
        with patch('%s.os.path.exists' % pbm, autospec=True) as mock_exist:
            mock_exist.return_value = True
            with patch('%s.open' % pbm,
                       mock_open(read_data=content), create=True) as m_open:
                res = read_json_file('/my/path')
        assert res == val
        assert mock_exist.mock_calls == [call('/my/path')]
        assert m_open.mock_calls == [
            call('/my/path', 'r'),
            call().__enter__(),
            call().read(),
            call().__exit__(None, None, None)
        ]

    def test_read_json_file_no_exist(self):
        val = {'foo': 'bar', 'baz': 2}
        content = json.dumps(val)
        with patch('%s.os.path.exists' % pbm, autospec=True) as mock_exist:
            mock_exist.return_value = False
            with patch('%s.open' % pbm,
                       mock_open(read_data=content), create=True) as m_open:
                with pytest.raises(Exception) as excinfo:
                    read_json_file('/my/path')
        assert exc_msg(excinfo.value) == 'ERROR: file /my/path does not exist.'
        assert mock_exist.mock_calls == [call('/my/path')]
        assert m_open.mock_calls == []
