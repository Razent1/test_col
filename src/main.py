from typing import Optional
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from databases import Database
from datetime import date
from starlette.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

database = Database("sqlite:///test.db")


@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.get("/")
async def root(request: Request):
    query = "SELECT * FROM sales"
    results = await database.fetch_all(query=query)
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "date": str(date.today().strftime("%Y-%m-%d")),
                                                     "res": results})


@app.get("/error")
async def error(request: Request):
    query = "SELECT * FROM sales"
    results = await database.fetch_all(query=query)
    return templates.TemplateResponse("error.html", {"request": request,
                                                     "date": str(date.today().strftime("%Y-%m-%d")),
                                                     "res": results})


@app.get("/delete")
async def delete_page(request: Request):
    query = "SELECT * FROM sales"
    results = await database.fetch_all(query=query)
    return templates.TemplateResponse("delete.html", {"request": request,
                                                      "res": results})


@app.get("/delete_error")
async def delete_error(request: Request):
    query = "SELECT * FROM sales"
    results = await database.fetch_all(query=query)
    return templates.TemplateResponse("delete_error.html", {"request": request,
                                                            "res": results})


@app.post("/send_data")
async def send_data(request: Request,
                    total_due: Optional[float] = Form(None),
                    date_sale: Optional[date] = Form(None),
                    manager_id: Optional[int] = Form(None)):
    if total_due and date_sale and manager_id:
        query = f"""INSERT INTO sales(total_due, date_sale, manager_id) 
        VALUES ({total_due}, DATE('{date_sale}'),
          {manager_id})"""
        await database.execute(query=query)
    else:
        return RedirectResponse(url="/error", status_code=302)
    return RedirectResponse(url="/", status_code=302)


@app.post("/delete_data")
async def delete_data(request: Request,
                      order_id: Optional[int] = Form(None)):
    if order_id:
        query = f"""DELETE FROM sales WHERE {order_id} = order_id"""
        await database.execute(query=query)
    else:
        return RedirectResponse(url="/delete_error", status_code=302)
    return RedirectResponse(url="/delete", status_code=302)

