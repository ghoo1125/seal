from typing import List, Optional

from fastapi import Body, FastAPI, Header, Request, status
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import Event, MessageEvent, TextSendMessage
from pydantic import BaseModel, validator

app = FastAPI()

# TODO hide tokens
LINE_CHANNEL_ACCESS_TOKEN = 'qS5Edsqzf0bglFdlcUpYMa/qqYErgkE+k4AMzB6aMFUZw/QgYUMxgyVI0t+ldHy8OpaDncrg+DPFn7wMyVfEhDq/9ywqYlQFLWFIqckoBhPDqUv0OnImNpcS3x2WdwOL94HKP7yfm7b2iA2PQ56mpQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'eebfd0d4235b4b810559a217471546f2'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)


@app.post("/seal")
async def line_post(request: Request, x_line_signature: Optional[str] = Header(None)):
body = (await request.body()).decode('utf-8')

    try:
        events = parser.parse(body, x_line_signature)
    except InvalidSignatureError:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN)
    except LineBotApiError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

    for event in events:
        if isinstance(event, MessageEvent):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )

    return JSONResponse(status_code=status.HTTP_200_OK)
