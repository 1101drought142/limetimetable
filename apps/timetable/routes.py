from fastapi import  Request, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated


router = APIRouter(prefix='/', tags=['User'])


@app.get("/", response_class=HTMLResponse)
def index(request: Request, user: Annotated[User, Depends(manager_restriction)]):
    data = DateLogic().create_date_data(cort_id=1)
    corts = get_corts()
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval(), "corts": corts, "user": user})

@app.post("/api/server/v1/renew_table/", response_class=HTMLResponse)
def get_time_table (request: Request, request_data: GetFilteredTable):
    return  request_data.return_html_template(request, templates)

@app.post("/api/server/v1/get_create_modal_template/", response_class=HTMLResponse)
def create_modal(request: Request, request_data: GetAddNewBlockModalTemplate):
    return request_data.return_html_template(request, templates)

@app.post("/api/server/v1/get_change_modal_template/", response_class=HTMLResponse)
def change_modal(request: Request, request_data: GetChangeModalTemplate):
    return request_data.return_html_template(request, templates)


@app.post("/api/server/v1/get_create_repeatative_modal_template/", response_class=HTMLResponse)
def create_repeatative_modal(request: Request, request_data: GetAddNewRepeatativeBlockModalTemplate):
    return request_data.return_html_template(request, templates)

@app.post("/api/server/v1/get_change_repeatative_modal_template/", response_class=HTMLResponse)
def create_repeatative_modal(request: Request, request_data: GetChangeModalRepeatativeTemplate):
    return request_data.return_html_template(request, templates)

@app.post("/api/server/v1/create_raspisanie_object/", response_class=JSONResponse)
async def create_modal(request: Request, request_data: CreateNewTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html( "renew" )
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)

@app.post("/api/server/v1/delete_raspisanie_object/", response_class=JSONResponse)
async def delete_modal(request: Request, request_data: DeleteTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)    

@app.post("/api/server/v1/change_raspisanie_object/", response_class=JSONResponse)
async def update_modal(request: Request, request_data: ChangeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    

@app.post("/api/server/v1/create_repeatative_raspisanie_object/", response_class=JSONResponse)
async def create_repeatative_modal(request: Request, request_data: CreateNewRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html( "renew" )
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@app.post("/api/server/v1/change_repeatative_raspisanie_object/", response_class=JSONResponse)
async def update_modal(request: Request, request_data: ChangeRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)
    
@app.post("/api/server/v1/delete_repeatative_raspisanie_object/", response_class=JSONResponse)
async def delete_modal(request: Request, request_data: DeleteRepeatativeTimeBlockTemplate):
    creation_result = request_data.validate_data_and_do_sql()
    if (creation_result == True):
        await manager.broadcast_html("renew")
        return JSONResponse(content=jsonable_encoder({"success": True}), status_code=201)
    else:    
        return JSONResponse(content=jsonable_encoder({"success": False, "error": str(creation_result), }), status_code=422)    
    