from aiohttp import ClientSession
import asyncio
import pathlib


async def fetch(url, session, year):
    async with session.get(url) as response:
        html_body = await response.read()
        return {'body': html_body, 'year': year}


async def main(start_year=2020, years_ago=5):
    tasks = []
    async with ClientSession() as session:
        for i in range(0, years_ago):
            year = start_year - i
            url = f'https://www.boxofficemojo.com/year/{year}/'
            print('year:', year)
            tasks.append(
                asyncio.create_task(
                    fetch(url, session, year)
                )
            )
        pages_content = await asyncio.gather(*tasks)
        return pages_content


results = asyncio.get_event_loop().run_until_complete(main())

output_dir = pathlib.Path().resolve() / "snapshots"
output_dir.mkdir(parents=True, exist_ok=True)

for result in results:
    current_year = result.get('year')
    html_data = result.get('body')
    output_file = output_dir / f'{current_year}.html'
    output_file.write_text(html_data.decode())
