from components.cat import cat
from butter.render import render
import butter

from components.logo import logo

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route


async def homepage(request):
    content = butter.html() > [
        butter.head()
        > [
            butter.link(rel="preconnect", href="https://fonts.gstatic.com"),
            butter.link(
                href="https://fonts.googleapis.com/css2?family=Inconsolata:wght@500&display=swap",
                rel="stylesheet",
            ),
            butter.style()
            > """
            input::-webkit-input-placeholder {
                color: currentColor;
                opacity: 0.8;
            }
            input:-moz-placeholder {
                color: currentColor;
                opacity: 0.8;
            }
            input::-moz-placeholder {
                color: currentColor;
                opacity: 0.8;
            }
            input:-ms-input-placeholder {
                color: currentColor;
                opacity: 0.8;
            }
            """,
        ],
        butter.body(style="background: #D36582; padding: 50px;")
        > [
            butter.div()
            > [
                logo(),
                butter.h1(
                    style="font-family: inconsolata; color: #253C78; margin-top: 30px;"
                )
                > "find the latest version of your favourite software ✨",
                butter.form()
                > [
                    butter.span(
                        contenteditable="",
                        style=(
                            "font-family: inconsolata; font-size: 40px; background: none; border: none; "
                            "border-bottom: 4px solid currentColor; outline: none; color: #253C78; margin-top: 30px; "
                            "width: 200px;"
                        ),
                    )
                    > "python",
                    butter.button(style="border: none; background: none; font-size: 40px; cursor: pointer; margin-left: 20px;") > "👉",
                ],
            ],
            cat(style="position: absolute; bottom: 0; right: 0;"),
        ],
    ]

    return HTMLResponse(render(content))


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
    ],
)
