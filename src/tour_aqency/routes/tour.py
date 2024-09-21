from sqlalchemy import select, delete
import asyncio
from quart import (
    render_template,
    redirect,
    url_for,
    request,
)
from . import (
    Author,
    Tour,
    app,
    Config
)


@app.get("/tours")
async def tours():
    with Config.SESSION.begin() as session:
        smth = select(Tour)
        tours = session.scalars(smth).all()
        return await render_template(
            "index.html",
            tours=[Tour(
                id=x.id,
                created=x.created,
                content=x.content,
                author=x.author,
                title=x.title,
            )
            for x in tours   
        ],
        )
    

@app.post("/tours")
async def create_tour():
    form = await request.form
    if form:
        with Config.SESSION.begin() as session:
            tour = Tour(
                **form,
                author=Author(name="vadim"),
            )
            session.add(tour)
    
    return redirect(url_for("tours"))


@app.get("/tours/<int:index>/details")
async def tour_details(index: int):
    await asyncio.sleep(1)

    return "Hello world"


@app.get("/tours/<int:index>/delete")
async def delete_tours(index: int):
    return await render_template("delete_tour.html", index=index,)


@app.post("/tours/delete")
async def delete_tour():
    form = await request.form
    tour_id = form.get("tour_id")
    if tour_id:
        with Config.SESSION.begin() as session:
            session.execute(delete(Tour).where(Tour.id == tour_id))
    return redirect(url_for(tours.__name__))

