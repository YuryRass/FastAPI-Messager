from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router: APIRouter = APIRouter(
    prefix="/pages",
    tags=["Pages"],
)

templates = Jinja2Templates("templates")


@router.get("/chat")
def get_chat_page(request: Request):
    return templates.TemplateResponse(
        name="chat.html",
        context={"request": request},
    )
