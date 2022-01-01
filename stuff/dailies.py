from datetime import datetime, timedelta

import stuff.network as network

API_HEADERS: dict = {"X-Schema-Version": "latest"}
EASY_DAILIES: list = ["Forager", "Miner", "Lumberer", "Vista"]
PVP_DAILIES: list = ["Top Stats", "Player Kills", "Rank Points", "Reward Earner"]

BOUNTY_WAYPOINTS: dict = {
    "Crystal Oasis": "[&BLsKAAA=]",
    "Desert Highlands": "[&BGsKAAA=]",
    "Elon Riverlands": "[&BCgKAAA=]",
    "Desolation": "[&BNwKAAA=]",
    "Vabbian": "[&BNAKAAA=]"
}

EASY_WAYPOINTS = {
    "Ascalon": {
        "Forager": "[&BMcDAAA=] (South)",
        "Lumberer": "[&BB0CAAA=]",
        "Miner": "[&BEsBAAA=] (North / South)",
        "Vista": "[&BKYDAAA=]"
    },
    "Kryta": {
        "Forager": "[&BPoAAAA=] (South)",
        "Lumberer": "[&BKgAAAA=] (East), [&BMMAAAA=] (Southwest)",
        "Miner": "[&BBIAAAA=] (North), [&BJMBAAA=] (East), [&BPMAAAA=] (North)",
        "Vista": "[&BPoAAAA=], [&BPgAAAA=]"
    },
    "Maguuma Jungle": {
        "Forager": "[&BEIAAAA=] (North), [&BEABAAA=] (Northwest)",
        "Lumberer": "[&BNACAAA=]",
        "Miner": "[&BGMAAAA=] (West)",
        "Vista": "[&BLcEAAA=], [&BLoEAAA=]",
    },
    "Shiverpeaks": {
        "Forager": "[&BH0JAAA=] (Winterberry Farm), [&BOYAAAA=] (North), [&BEwCAAA=] (West)",
        "Lumberer": "[&BEUCAAA=], [&BEsCAAA=]",
        "Miner": "[&BFECAAA=] (West), [&BL8AAAA=] (South)",
        "Vista": "[&BI4DAAA=]",
    },
    "Orr": {
        "Forager": "[&BO8JAAA=] (North), [&BFgGAAA=] (South)",
        "Lumberer": "[&BKYCAAA=] (West), [&BO8JAAA=]",
        "Miner": "[&BKgCAAA=] (North), [&BFgGAAA=] (South)",
        "Vista": "[&BO4CAAA=], [&BO8JAAA=]",
    },
    "Maguuma Wastes": {
        "Forager": "[&BIYHAAA=] (North)",
        "Lumberer": "[&BH8HAAA=], [&BHoHAAA=]",
        "Miner": "[&BH8HAAA=] (West), [&BHoHAAA=] (South)",
        "Vista": "[&BH8HAAA=]",
    },
    "Heart of Maguuma": {
        "Forager": "[&BOAHAAA=] (NE, Flax farm at bottom level)",
        "Lumberer": "[&BGwIAAA=], [&BHgJAAA=]",
        "Miner": "[&BEEJAAA=], [&BPUHAAA=]",
        "Vista": "[&BOAHAAA=], [&BGwIAAA=] (West)",
    },
    "Desert": {
        "Forager": "",
        "Lumberer": "[&BJ0KAAA=]",
        "Miner": "Griffon Sanctuary, [&BFMKAAA=] (East, destroy Brand Battleshards)",
        "Vista": "Griffon Sanctuary, [&BLsKAAA=], [&BEAKAAA=]",
    }
}

PSNA = [
    "[&BIcHAAA=] [&BEwDAAA=] [&BNIEAAA=] [&BKYBAAA=] [&BIMCAAA=] [&BA8CAAA=]",
    "[&BH8HAAA=] [&BEgAAAA=] [&BKgCAAA=] [&BBkAAAA=] [&BGQCAAA=] [&BIMBAAA=]",
    "[&BH4HAAA=] [&BMIBAAA=] [&BP0CAAA=] [&BKYAAAA=] [&BDgDAAA=] [&BPEBAAA=]",
    "[&BKsHAAA=] [&BE8AAAA=] [&BP0DAAA=] [&BIMAAAA=] [&BF0GAAA=] [&BOcBAAA=]",
    "[&BJQHAAA=] [&BMMCAAA=] [&BJsCAAA=] [&BNUGAAA=] [&BHsBAAA=] [&BNMAAAA=]",
    "[&BH8HAAA=] [&BLkCAAA=] [&BBEDAAA=] [&BJIBAAA=] [&BEICAAA=] [&BBABAAA=]",
    "[&BIkHAAA=] [&BDoBAAA=] [&BO4CAAA=] [&BC0AAAA=] [&BIUCAAA=] [&BCECAAA=]"
]


async def get_daily_ids() -> tuple:
    response: dict = await network.get_response(headers=API_HEADERS, url="https://api.guildwars2.com/v2/achievements/daily")
    dailies: dict = response.get("pve") + response.get("wvw") + response.get("pvp")
    daily_ids: str = ""
    daily_ids_core: str = ""

    for daily in dailies:
        required_access = daily.get("required_access")
        max_level: int = daily["level"]["max"]

        if required_access is None or required_access["condition"] == "HasAccess":
            if max_level == 80:
                daily_ids += f"{str(daily['id'])},"
        else:
            daily_ids_core += f"{str(daily['id'])},"

    return daily_ids, daily_ids_core


async def parse_daily(name: str) -> tuple:
    if name == "WvW Big Spender":
        return name, "Spend 30 Badges of Honor at guild hall vendor."

    if "PvP" in name or name == "Top Stats":
        task: str = name.replace("PvP", "").strip()
        if task in PVP_DAILIES:
            return name, "PvP - Game Browser (last tab)"
        return None, None

    if "Bounty Hunter" in name:
        map_name: str = name.replace("Bounty Hunter", "").strip()
        waypoint = BOUNTY_WAYPOINTS.get(map_name)
        return name, waypoint

    tasks: list = [t for t in EASY_DAILIES if t in name]

    if len(tasks) < 1:
        return None, None

    task: str = tasks[0]
    area: str = name.replace(task, "").strip()

    try:
        waypoint = EASY_WAYPOINTS[area][task]
    except KeyError:
        print(f"Invalid task or area: {task} {area}")
        waypoint = None

    return name, waypoint


def get_psna():
    now = datetime.today()
    today = now - timedelta(hours=16, minutes=0)
    weekday = today.weekday()
    return PSNA[weekday]


async def get_dailies() -> dict:
    daily_ids, daily_ids_core = await get_daily_ids()

    urls: dict = {
        f"https://api.guildwars2.com/v2/achievements?ids={daily_ids[:-1]}": True,
        f"https://api.guildwars2.com/v2/achievements?ids={daily_ids_core[:-1]}": True,
    }

    results: list = await network.get_responses(headers=API_HEADERS, urls=urls)
    dailies = results[0]
    dailies_core = results[1]

    ret: dict = {}
    ret_core: dict = {}

    for daily in dailies:
        name: str = daily["name"].replace("Daily", "").strip()
        key, value = await parse_daily(name)

        if key is not None and value is not None:
            ret[key] = value

    for daily in dailies_core:
        name: str = daily["name"].replace("Daily", "").strip()
        key, value = await parse_daily(name)

        if key is not None and value is not None:
            ret_core[key] = value

    return {"dailies": [ret, ret_core], "psna": get_psna()}
