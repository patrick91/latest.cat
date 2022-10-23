from typing import Any

from prisma import Prisma
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL

from api.schema import schema

database = Prisma()


class MyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Request | WebSocket,
        response: Response | None = None,
    ) -> Any:
        return {"request": request, "response": response, "db": database}


graphql_app = MyGraphQL(schema)

app = Starlette(on_startup=[database.connect], on_shutdown=[database.disconnect])
app.add_route("/graphql", graphql_app)
