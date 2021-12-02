from bs4 import BeautifulSoup

import stuff.network as network

API_HEADERS = {"X-Schema-Version": "latest"}

GUILD_HALLS = [
    "Lost Precipice",
    "Gilded Hollow",
    "Windswept Haven",
]

GUILD_PUZZLES = [
    "Angvar's Trove",
    "Scratch Sentry Defense",
    "Eye of the North",
    "Blightwater Shatterstrike",
    "Branded for Termination",
    "Save Our Supplies",
    "Langmar Estate",
    "Southsun Crab Toss",
    "Proxemics Lab",
    "The Omphalos Chamber",
    "Deep Trouble",
    "Cragstead",
    "North Nolan Hatchery",
    "Codebreaker",
    # RAIDS + AERODROME
    "Lion's Arch Aerodrome",
    "Bastion of the Penitent",
    "Stronghold of the Faithful",
    "Salvation Pass",
    "Spirit Vale",
    "The Key of Ahdashim",
]

SKIP_MAP_IDS = [
    828,
    334,
    374,
    376,
    964,
    1161,
    1326,
    1327,
    1212,
    1219,
    1227,
    1242,
    1255,
    1257,
    1266,
    1300,
    1318,
    1380,
    1382,
    372,
    373,
    460,
    833,
    827,
    1194,
    330,
    335,
    336,
    378,
    830,
    905,
    914,
    924,
    1073,
    1193,
    1246,
    1369,
    646,
    647,
    648,
    649,
    650,
    651,
    1392,
    1407,
    138,
    250,
    276,
    288,
    447,
    516,
    523,
    558,
    658,
    677,
    685,
    693,
    700,
    703,
    758,
    787,
    797,
    922,
    1002,
    1006,
    1009,
    1019,
    1153,
    1095,
    1158,
    1169,
]


async def crawl_map_data() -> dict:
    urls: dict = {
        "https://api.guildwars2.com/v2/continents/1/floors/1": True,
        "https://api.guildwars2.com/v2/continents/1/floors/49": True,
        "https://api.guildwars2.com/v2/quests?ids=all": True,
    }

    results: list = await network.get_responses(headers=API_HEADERS, urls=urls)
    regions: dict = results[0].get("regions")
    regions_cd: dict = results[1].get("regions")
    stories: list = results[2]
    regions.pop("12")
    regions["12"] = regions_cd["12"]
    story_names: list = []

    for story in stories:
        story_name = story.get("name")

        if story_name is not None:
            story_names.append(story_name.lower())

    ret: dict = {}

    for region_id, region in regions.items():
        region_name: str = region.get("name")
        maps: dict = region.get("maps")

        if region_name is None or maps is None:
            continue

        for map_id, map_data in maps.items():
            map_name: str = map_data.get("name")

            if int(map_id) in SKIP_MAP_IDS or map_name.lower() in story_names or map_name in GUILD_PUZZLES:
                continue
            elif "(Home)" in map_name or map_name == "???" or "Strike Mission:" in map_name:
                continue

            is_guild_hall: bool = False

            for guild_hall in GUILD_HALLS:
                if guild_hall in map_name:
                    is_guild_hall = True
                    break

            if is_guild_hall:
                continue

            points: dict = map_data.get("points_of_interest")

            if map_name is None or points is None:
                continue

            for point_id, point in points.items():
                try:
                    point_type: str = point["type"]
                    point_name: str = point["name"]
                    point_chat_link: str = point["chat_link"]
                except Exception:
                    continue

                if point_type == "waypoint":
                    ret[point_name] = point_chat_link

    return ret
