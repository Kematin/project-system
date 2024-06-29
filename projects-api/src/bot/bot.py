import io
import os
import zipfile

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger
from pydantic import UUID4

from bot.auth import authenticate
from config import config
from database import AsyncSessionLocal, Database, Project


# dependency
async def get_db():
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        await db.close()


bot_router = APIRouter(tags=["Bot"])


@bot_router.get("/projects")
@logger.catch(exclude=HTTPException)
async def retrieve_projects(
    category: str | None = None, db=Depends(get_db), _=Depends(authenticate)
):
    project_database = Database(Project, db)
    projects = await project_database.get_all()
    projects = [project for project in projects if not project.is_blocked]
    if category is None:
        logger.info("Get all projects (FOR BOT).")
        return {"projects": projects}
    elif category not in config.CATEGORIES:
        logger.warning("Invalid category for projects (FOR BOT)")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category."
        )
    else:
        projects = [
            project
            for project in projects
            if project.category == config.CATEGORIES[category]
        ]
        logger.info(f"Get projects with type: {category} (FOR BOT)")
        return {"projects": projects}


@bot_router.get("/projects/{project_id}")
@logger.catch(exclude=HTTPException)
async def retrieve_project(
    project_id: UUID4, db=Depends(get_db), _=Depends(authenticate)
):
    project_database = Database(Project, db)
    project = await project_database.get(project_id)
    if project:
        logger.info(f"Get project {project_id} (FOR BOT).")
        return {"project": project}
    else:
        logger.warning(f"Project with id {project_id} not found (FOR BOT).")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )


@bot_router.post("/project/{project_id}")
@logger.catch(exclude=HTTPException)
async def change_blocked_state_project(
    project_id: UUID4, is_blocked: bool, db=Depends(get_db), _=Depends(authenticate)
):
    project_database = Database(Project, db)
    res = await project_database.update(project_id, {"is_blocked": is_blocked})
    if res:
        logger.info(f"Set is_blocked: {is_blocked} for project {project_id} (FOR BOT)")
        return {"message": "successfull"}
    else:
        logger.warning(f"Project with id {project_id} not found (FOR BOT).")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )


@bot_router.get("/files/{project_id}")
@logger.catch(exclude=HTTPException)
async def retrieve_project_file(
    project_id: UUID4, type: str, db=Depends(get_db), _: str = Depends(authenticate)
):
    project_database = Database(Project, db)
    project = await project_database.get(project_id)
    if not project:
        logger.warning(f"Project with id {project_id} not found (FOR BOT).")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found.",
        )
    if type not in config.FILE_TYPES:
        logger.warning(f"Specified file type is not valid {project_id} (FOR BOT)")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Specified file type is not valid",
        )
    media_type = config.MEDIA_TYPES[type]
    if type != "doc" and type != "cover":
        if not project.__dict__[config.PROJECT_FIELDS[type]]:
            logger.warning(f"No {type} for project {project_id} (FOR BOT)")
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Project dont have this type",
            )
    if type != "product":
        filename = config.FILE_TYPES[type]
        logger.info(f"Return {type} for project {project_id} (FOR BOT)")
        return FileResponse(
            path=f"projects/{project_id}/{filename}", media_type=media_type
        )
    else:
        file_dir = f"projects/{project_id}/product"
        files = os.listdir(file_dir)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a") as zip_file:
            for file in files:
                file_path = os.path.join(file_dir, file)
                zip_file.write(file_path, arcname=file)
        zip_buffer.seek(0)

        logger.info(f"Return product zip for project {project_id} (FOR BOT)")
        return StreamingResponse(
            io.BytesIO(zip_buffer.getvalue()),
            media_type=media_type,
            headers={"Content-Disposition": "attachment;filename=project.zip"},
        )
