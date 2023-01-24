import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class Result:
    original_link: str
    bypassed_link: str

class OuoBypasser:
    BASE_URL = 'https://www.google.com/recaptcha/api2/'
    PARAMS = 'ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        self.tasks = []
        self.results = []
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    async def solve_captcha(self):
        _params = dict(pair.split('=') for pair in self.PARAMS.split('&'))
        async with self.session.get(f'{self.BASE_URL}anchor', params = self.PARAMS, headers = self.headers) as resp:
            c = re.findall(r'"recaptcha-token" value="(.*?)"', await resp.text())[0]

        async with self.session.post(f'{self.BASE_URL}reload', data = f'v={_params["v"]}&reason=q&c={c}&k={_params["k"]}&co={_params["co"]}', params = f'k={_params["k"]}', headers = self.headers) as resp:
            return re.findall(r'"rresp","(.*?)"', await resp.text())[0]

    async def bypass(self, url):
        url = url.replace('ouo.press', 'ouo.io')
        _id = url.split('/')[-1]
        next_url = f'https://ouo.io/go/{_id}'

        async with self.session.get(url) as resp:
            contents = await resp.text()
            for _ in range(2):
                if resp.headers.get('Location'):
                    break

                soup = BeautifulSoup(contents, 'lxml')
                inputs = soup.form.findAll("input", {"name": re.compile(r"token$")})
                data = { _input.get('name'): _input.get('value') for _input in inputs }
                data['x-token'] = await self.solve_captcha()

                async with self.session.post(
                    next_url,
                    data = data,
                    headers = self.headers,
                    allow_redirects = False
                    ) as resp:
                        await resp.text()
                        next_url = f'https://ouo.io/xreallcygo/{_id}'

            self.results.append(Result(
                original_link = url,
                bypassed_link = resp.headers.get('Location')
            ))

    async def add_task(self, url):
        self.tasks.append(
            self.bypass(url)
        )

    async def run(self):
        await asyncio.gather(*self.tasks)