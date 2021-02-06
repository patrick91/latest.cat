from starlette.responses import RedirectResponse

from data.config import database


async def search(request):
    q = request.query_params["q"]  # noqa

    query = """
        SELECT slug FROM Software
        WHERE slug LIKE :q
            OR :q2 IN (
                select value
                from json_each(aliases)
            )
    """

    result = await database.fetch_val(query, {"q": q, "q2": q})
    print(result)
    return RedirectResponse(f"/{result}")
