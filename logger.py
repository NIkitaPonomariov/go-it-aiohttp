from aiofile import AIOFile

class Logger:
    def __init__(self, filepath: str):
        self.filepath = filepath

    async def log(self, message: str) -> None:
        async with AIOFile(self.filepath, 'a') as file:
            await file.write(f"{message}\n")
