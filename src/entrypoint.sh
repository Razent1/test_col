#!/bin/bash
pip3 install fastapi aiosqlite databases starlette uvicorn aiofiles jinja2 python-multipart pydantic
uvicorn main:app --host 0.0.0.0 --port 15400