from __future__ import annotations

from fastapi import Response


def get_response(url: str, status_code: int):
    return Response(
        status_code=status_code,
        content=f"""<?xml version="1.0" encoding="UTF-8"?>
<Error>
<Code></Code>
<Message>This is a mock error message</Message>
<Resource>{url}</Resource>
<RequestId>4442587FB7D0A2F9</RequestId>
</Error>""",
        headers={
            "Content-Type": "application/xml",
        },
    )
