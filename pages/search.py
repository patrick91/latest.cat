from starlette.responses import RedirectResponse


async def search(request):
    query = request.query_params["q"]  # noqa

    # TODO: find matching language

    return RedirectResponse("/python")
