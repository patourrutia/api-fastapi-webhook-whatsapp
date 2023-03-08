import asyncio


async def square(number: int) -> int:
    return number*number


async def main() -> None:
    x = await square(10)
    print(f'x={x}')

    y = await square(5)
    print(f'y={y}')

    print(f'total={x+y}')

asyncio.run(main())