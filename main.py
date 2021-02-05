from starlette.applications import Starlette
from starlette.routing import Route

from data.config import database
from pages.home import homepage
from pages.search import search
from pages.version import fetch_latest

app = Starlette(
    debug=False,
    routes=[
        Route("/", homepage),
        Route("/search", search),
        Route("/{slug}", fetch_latest),
        Route("/{slug}/{version}", fetch_latest),
    ],
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
