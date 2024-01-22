from fastapi import FastAPI
from db import get_async_pool
import os
import asyncio
import aiofiles

app = FastAPI()

pool = get_async_pool()


@app.post("")
async def create_todo(todo):
    async with pool.connection() as conn:
        await conn.execute(
            "insert into todos (name, completed) values (%s, %s)",
            [todo.name, todo.completed],
        )



async def read_and_execute(file_path):
    async with aiofiles.open(file_path, 'r') as file:
        content = await file.read()
        print(f"File: {file_path}\nContent:\n{content}\n{'=' * 30}")
        async with pool.connection() as conn:
            await conn.execute()


@app.on_event("startup")
async def migrate(directory_path):
    files = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)

    tasks = []
    for file in files:
        tasks.append(read_and_execute(file))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    directory_path = "/home/user/PycharmProjects/orderme/src/migrations"
    asyncio.run(main(directory_path))

def outer(s):
    def inner():
        print(s)

    return inner

a = outer(5)
