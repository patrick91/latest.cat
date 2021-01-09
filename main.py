from starlette.applications import Starlette
from starlette.routing import Route

from data.config import database
from pages.home import homepage
from pages.search import search
from pages.version import version

app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
        Route("/search", search),
        Route("/{slug}", version),
    ],
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
