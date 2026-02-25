import asyncio

# 协程没有返回值，那么就直接输出了，所以是不需要返回值的啦～
async def print_even_numbers():
    for i in range(10):
        if i % 2 == 0:
            await asyncio.sleep(0.5)
            print(f"Even number: {i}")


async def print_odd_numbers():
    for i in range(10):
        if i % 2 != 0:
            await asyncio.sleep(0.5)
            print(f"Odd number: {i}")


async def main():
    await asyncio.gather(
        print_even_numbers(),
        print_odd_numbers()
    )


if __name__ == "__main__":
    asyncio.run(main())
