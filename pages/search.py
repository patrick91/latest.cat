from starlette.responses import RedirectResponse


async def search(request):
    q = request.query_params["q"]  # noqa
    return RedirectResponse(f"/{q}")
