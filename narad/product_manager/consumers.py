import asyncio
from datetime import datetime

from celery.result import AsyncResult
from channels.generic.http import AsyncHttpConsumer


class ServerSentEventsConsumer(AsyncHttpConsumer):

    state_messages = {
        "PENDING": "Uploading of products is about to start...",
        "STARTED": "Uploading of products is started...",
        "PROGRESS": "Uploading of products is progress...",
        "SUCCESS": "Uploading of products is completed...",
        "FAILURE": "Failed to upload given produces...",
        "RETRY": "Once again trying to upload products..."
    }

    async def handle(self, body):
        send_events = True
        task_id = self.scope["url_route"]["kwargs"]["task_id"]
        task = AsyncResult(task_id)
        await self.send_headers(
            headers=[
                (b"Cache-Control", b"no-cache"),
                (b"Content-Type", b"text/event-stream"),
                (b"Transfer-Encoding", b"chunked"),
            ]
        )
        body = ''
        body += ':' + (' ' * 2048) + '\n\n'
        body += 'event: stream-open\ndata:\n\n'
        await self.send_body(body.encode("utf-8"), more_body=True)
        while send_events:
            message = self.state_messages.get(task.state)
            if task.state in ['SUCCESS', 'FAILURE']:
                body += f'event: completed\ndata: {message}\n\n'
                send_events = False
                await self.send_body(body.encode("utf-8"))
            else:
                body += f'event: message\ndata: {message}\n\n'
                await self.send_body(body.encode("utf-8"), more_body=True)
                await asyncio.sleep(1)
