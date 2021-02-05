from starlette.responses import RedirectResponse
from data.config import database


async def search(request):
    q = request.query_params["q"]  # noqa

    db_q = f"%{q.lower()}%"

    query = """
        SELECT slug FROM Software
        WHERE slug LIKE :q
            OR aliases LIKE :q2
    """

    result = await database.fetch_val(query, {"q": db_q, "q2": db_q})

    return RedirectResponse(f"/{result}")
