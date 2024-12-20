from typing import List, Optional
from bson import ObjectId
from fastapi import *

from .models import *
from ..errors import *
from ..schemas import BaseResponses

router = APIRouter()


class RoomResponses(BaseResponses):
    data: Optional[List[Room]]


@router.get("/", response_model=RoomResponses)
async def get_rooms(
        request: Request,
        name: str = Query(default=None),
        address: str = Query(default=None),
        telephone: str = Query(default=None)
):
    str_time = time.perf_counter()
    try:
        query = {key: value for key, value in {
            "name": name, "effective": address, "telephone": telephone
        }.items() if value}
        ds = await room_repository.find_many(query=query, request=request)

        result = []
        for d in ds:
            result.append(Room.from_mongo(d))

        return RoomResponses(
            data=result,
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return handle_error(e, str_time)


@router.get("/<id>", response_model=RoomResponses)
async def get_room(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return RoomResponses(
                status=400,
                detail="Invalid ID format",
                used_time=(time.perf_counter() - str_time) * 1000,
                data=None
            )
        d = await room_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return RoomResponses(
            data=[Room.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.post("/", response_model=RoomResponses, responses={
    409: {
        "description": "Resource maybe created. But can't found it.",
    }
})
async def create_room(request: Request, data: RoomInput):
    str_time = time.perf_counter()
    try:
        _id = await room_repository.insert_one(data.model_dump(), request=request)
        d = await room_repository.find_one(query={"_id": ObjectId(_id)})
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return RoomResponses(
            data=[Room.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.delete("/<id>", response_model=RoomResponses)
async def delete_room(
        request: Request,
        id: str
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        d = await room_repository.delete_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_resource_not_found_error(str_time)

        return RoomResponses(
            data=None,
            used_time=(time.perf_counter() - str_time) * 1000,
            detail=f"Successfully. [{d}] Resource(s) deleted."
        )
    except Exception as e:
        return handle_error(e, str_time)


@router.put("/<id>", response_model=RoomResponses, responses={
    409: {
        "description": "Resource maybe changed. But can't found it.",
    }
})
async def put_room(
        request: Request,
        id: str,
        data: RoomInput
):
    str_time = time.perf_counter()
    try:
        if not ObjectId.is_valid(id):
            return handle_invalid_id_format_error(str_time)
        await room_repository.update_one(query={"_id": ObjectId(id)}, update=data.model_dump(),
                                           request=request)
        d = await room_repository.find_one(query={"_id": ObjectId(id)}, request=request)
        if not d:
            return handle_after_write_resource_not_found_error(str_time)
        return RoomResponses(
            data=[Room.from_mongo(d)],
            used_time=(time.perf_counter() - str_time) * 1000
        )
    except Exception as e:
        return handle_error(e, str_time)
