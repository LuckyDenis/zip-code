import dataclasses
import typing

import aiohttp

from zip_code import config


@dataclasses.dataclass(frozen=True)
class CodeInfo:
    latitude: str
    longitude: str
    city: str
    city_en: str
    country_code: str
    state: str
    state_en: str



class CodeApi:
    bot_config: config.BotConfig
    BASE_URL = 'https://app.zipcodebase.com/api/v1/search'

    def __init__(self, bot_config: config.BotConfig):
        self.bot_config = bot_config

    async def get_codes_info(self, code: str) -> typing.List[CodeInfo]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                self.BASE_URL + '?' + 'codes=' + code,
                headers={
                    "apikey": self.bot_config.ZIP_CODE_API_TOKEN
                }
            )
            body = await response.json()
            codes_info = []
            for raw_code_info in body['results'][code]:
                code_info = CodeInfo(
                    latitude=raw_code_info['latitude'],
                    longitude=raw_code_info['longitude'],
                    city=raw_code_info['city'],
                    city_en=raw_code_info['city_en'],
                    country_code=raw_code_info['country_code'],
                    state=raw_code_info['state'],
                    state_en=raw_code_info['state']
                )
                codes_info.append(code_info)
            return codes_info
