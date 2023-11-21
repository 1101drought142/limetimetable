from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, List


from logic.datelogic import DateLogic
from logic.request_handlers import GetAddNewBlockModalTemplate, CreateNewTimeBlockTemplate, GetChangeModalTemplate, DeleteTimeBlockTemplate, ChangeTimeBlockTemplate, GetFilteredTable, GetAddNewRepeatativeBlockModalTemplate, CreateNewRepeatativeTimeBlockTemplate, GetChangeModalTemplate, ChangeRepeatativeTimeBlockTemplate, GetChangeModalRepeatativeTemplate, DeleteRepeatativeTimeBlockTemplate
from logic.utils import get_corts, get_user_or_None
from database import Users, User

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
security = HTTPBasic()

def auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> User:
    current_username_bytes = credentials.username
    current_password_bytes = credentials.password

    user = get_user_or_None(current_username_bytes, current_password_bytes)

    if (user):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        ) 

def get_user_with_restrictions(
        types : List[Users],
        user : Annotated[User, Depends(auth)],
): 
    for type in types:
        if type == user.type:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You dont have enough rules to access this resource",
        headers={"WWW-Authenticate": "Basic"},
    ) 

admin_restriction = get_user_with_restrictions(types = [Users.superuser])
manager_restriction = get_user_with_restrictions(types = [Users.manager, Users.superuser])
api_restriction = get_user_with_restrictions(types = [Users.api])

@app.get("/", response_class=HTMLResponse)
def index(request: Request, user: Annotated[User, Depends(manager_restriction)]):
    data = DateLogic().create_date_data(cort_id=1)
    corts = get_corts()
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "time_range" : DateLogic().get_date_interval(), "corts": corts, "user": user})

@app.get("/logout/")
async def logout(user: Annotated[User, Depends(manager_restriction)]):
   
   return RedirectResponse("/", status_code=302)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint( websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

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
    

# @app.get("/api/v1/order_time/", response_class=JSONResponse)
# async def get_available_time(request: Request, request_data: GetAvailableTime):
#     pass

# @app.post("/api/v1/order/", response_class=JSONResponse)
# async def api_create_object(request: Request, request_data: CreateObjectApi):
#     pass

# @app.post("/api/v1/order_payed/", response_class=JSONResponse)
# async def api_update_object_payed(request: Request, request_data: UpdateObjectPayedApi):
#     pass
