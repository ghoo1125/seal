from asyncio import coroutine

import pytest
from fastapi import Request, status

from seal.server import line_post


@pytest.mark.asyncio
async def test_line_post(mocker):
    mock_request = mocker.patch("fastapi.Request")
    mock_request.body = mocker.Mock(side_effect=coroutine(
        lambda: bytes('{"destination": "xxx", "events": []}', 'utf-8')))
    mocker.patch("seal.server.parser.parse", return_value=[])

    actual = await line_post(mock_request, None)
    assert actual.status_code == status.HTTP_200_OK

# for debug mode
if __name__ == "__main__":
    pytest.main()
