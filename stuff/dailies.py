from datetime import datetime, timedelta

import stuff.network as network

API_HEADERS: dict = {"X-Schema-Version": "latest"}
EASY_DAILIES: list = ["Forager", "Miner", "Lumberer", "Vista Viewer"]
PVP_DAILIES: list = ["Top Stats", "Player Kills", "Rank Points", "Reward Earner"]

BOUNTY_WAYPOINTS: dict = {
    "Crystal Oasis": "[&BLsKAAA=]",
    "Desert Highlands": "[&BGsKAAA=]",
    "Elon Riverlands": "[&BCgKAAA=]",
    "Desolation": "[&BNwKAAA=]",
    "Vabbian": "[&BNAKAAA=]"
}

TASKMASTER_WAYPOINTS: dict = {
    "Elon Riverlands": "[&BFMKAAA=] (Augury Rock hearts northwest are easier)",
    "Desolation": "[&BNwKAAA=] or [&BHcKAAA=]",
}

MINIDUNGEON_WAYPOINTS: dict = {
    "Bad Neighborhood": "[&BPkAAAA=] (northwest bandit cave)",
    "Don't Touch the Shiny": "[&BDoBAAA=] (should wiki this on first try)",
    "Forgotten Stream": "[&BBsDAAA=] (northeast, jump underwater then keep going NE)",
    "Forsaken Fortune": "[&BGUCAAA=] (on a timer, just do with everyone else)",
    "Goff's Loot": "[&BLoDAAA=] (north, at the end of bandit cave)",
    "Grounded": "[&BOQGAAA=] (northwest grounded ship, keep going down the ship)",
    "Magellan's Memento": "[&BHgCAAA=] (cave northeast beyond the grawls, hug the walls inside)",
    "Rebel's Seclusion": "[&BBoCAAA=] (entrance northeast)",
    "Ship of Sorrows": "[&BOACAAA=] (underwater ship west of POI, keep going down the ship)",
    "Tears of Itlaoco": "[&BD4BAAA=] (should wiki this on first try)",
    "The Long Way Around": "[&BPICAAA=] (should wiki this on first try)",
    "Vexa's Lab": "[&BBoCAAA=] (should wiki this on first try)",
    "Windy Cave Treasure": "[&BJkBAAA=] (southwest, mount through the start if possible)",
}

JP_WAYPOINTS: dict = {
    "Antre of Adjournment": "[&BKoCAAA=]",
    "Behem Gauntlet": "[&BP0BAAA=]",
    "Branded Mine": "[&BNcAAAA=]",
    "Buried Archives": "[&BCIDAAA=]",
    "Chaos Crystal Cavern": "[&BOQBAAA=]",
    "Coddler's Cove": "[&BEYCAAA=]",
    "Collapsed Observatory": "[&BBIAAAA=]",
    "Conundrum Cubed": "[&BMgCAAA=]",
    "Crash Site": "[&BIAHAAA=]",
    "Craze's Folly": "[&BAECAAA=]",
    "Crimson Plateau": "[&BMYDAAA=]",
    "Dark Reverie": "[&BDUBAAA=] or [&BEIBAAA=] (Skyscale skip)",
    "Demongrub Pits": "[&BPwAAAA=] (can just mount through lol)",
    "Fawcett's Bounty": "[&BLIAAAA=] (hard)",
    "Goemm's Lab": "[&BLIEAAA=]",
    "Grendich Gamble": "[&BNoAAAA=]",
    "Griffonrook Run": "[&BOgAAAA=] or [&BJYBAAA=] (SS / Griffon skip)",
    "Hexfoundry": "[&BM0BAAA=]",
    "Hidden Garden": "[&BMkCAAA=], [&BM8CAAA=], [&BNECAAA=], [&BNICAAA=] (potential entrances, defeat keepers)",
    "King Jalis's Refuge": "[&BLUAAAA=]",
    "Loreclaw Expanse": "[&BMcDAAA=]",
    "Morgan's Leap": "[&BDUBAAA=]",
    "Only Zuhl": "[&BE4CAAA=]",
    "Pig Iron Quarry": "[&BBcCAAA=]",
    "Portmatt's Lab": "[&BKQBAAA=]",
    "Scavenger's Chasm": "[&BKoCAAA=]",
    "Shaman's Rookery": "[&BHcBAAA=]",
    "Shattered Ice Ruins": "[&BH4CAAA=]",
    "Skipping Stones": "[&BNAGAAA=]",
    "Spekks's Lab": "[&BDcBAAA=]",
    "Spelunker's Delve": "[&BP4FAAA=]",
    "Swashbuckler's Cove": "[&BJEBAAA=]",
    "Tribulation Caverns": "[&BD8FAAA=]",
    "Tribulation Rift": "[&BD8FAAA=]",
    "Under New Management": "[&BNUGAAA=]",
    "Urmaug's Secret": "[&BA0EAAA=]",
    "Vizier's Tower": "[&BPcCAAA=] or [&BPECAAA=] (safer Skyscale skip)",
    "Wall Breach Blitz": "[&BGEBAAA=]",
    "Weyandt's Revenge": "[&BDMEAAA=]",
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
        "Forager": "[&BEMLAAA=], [&BEAKAAA=] (North), [&BJEKAAA=] (North, @ waterfall)",
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


dailies_cache: dict = {}
dailies_tomorrow_time: datetime
max_level_only: bool = True


def toggle_max_level_only():
    global max_level_only
    max_level_only = not max_level_only
    print(max_level_only)


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
                if max_level_only:
                    continue
                daily_ids_core += f"{str(daily['id'])},"
        else:
            if max_level == 80 or not max_level_only:
                daily_ids_core += f"{str(daily['id'])},"

    # for daily in dailies:
    #     required_access = daily.get("required_access")
    #
    #     if required_access is None or required_access["condition"] == "HasAccess":
    #         daily_ids += f"{str(daily['id'])},"

    return daily_ids, daily_ids_core


async def parse_daily(name: str) -> tuple:
    if name == "WvW Big Spender":
        return name, "Spend 30 Badges of Honor at guild hall vendor.", True

    if "Mystic Forger" in name:
        return name, "[&BBAEAAA=] - FREE 2 GOLD!", False

    if "PvP" in name or name == "Top Stats":
        task: str = name.replace("PvP", "").strip()
        if task in PVP_DAILIES:
            return name, "", True
        return None, None, None

    if "Bounty Hunter" in name:
        map_name: str = name.replace("Bounty Hunter", "").strip()
        waypoint = BOUNTY_WAYPOINTS.get(map_name)
        return name, waypoint, False

    if "Jumping Puzzle" in name:
        jp_name: str = name.replace("Jumping Puzzle", "").strip()
        waypoint = JP_WAYPOINTS.get(jp_name)
        return name, waypoint, False

    if "Minidungeon" in name:
        md_name: str = name.replace("Minidungeon", "").strip()
        waypoint = MINIDUNGEON_WAYPOINTS.get(md_name)
        return name, waypoint, False

    if "Taskmaster" in name:
        map_name: str = name.replace("Taskmaster", "").strip()
        waypoint = TASKMASTER_WAYPOINTS.get(map_name)
        return name, waypoint, False

    tasks: list = [t for t in EASY_DAILIES if t in name]

    if len(tasks) < 1:
        return None, None, None

    task: str = tasks[0]
    area: str = name.replace(task, "").strip()

    if area == "Maguuma":
        area = "Maguuma Jungle"

    if task == "Vista Viewer":
        task = "Vista"

    try:
        waypoint = EASY_WAYPOINTS[area][task]
    except KeyError:
        print(f"Invalid task or area: {task} {area}")
        waypoint = None

    return name, waypoint, False


def get_psna():
    now = datetime.today()
    today = now - timedelta(hours=16, minutes=0)
    weekday = today.weekday()
    return PSNA[weekday]


async def get_dailies() -> dict:
    global dailies_tomorrow_time, dailies_cache
    if len(dailies_cache) == 0 or dailies_tomorrow_time is None:
        print("- Pulling dailies due to no cache...")
        await pull_dailies()
    elif datetime.now() >= dailies_tomorrow_time:
        print("- Pulling dailies due to outdated cache...")
        await pull_dailies()

    ret: dict = dailies_cache
    ret["psna"] = get_psna()
    return ret


async def pull_dailies():
    global dailies_cache, dailies_tomorrow_time, max_level_only
    daily_ids, daily_ids_core = await get_daily_ids()

    urls: dict = {
        f"https://api.guildwars2.com/v2/achievements?ids={daily_ids[:-1]}": True,
        f"https://api.guildwars2.com/v2/achievements?ids={daily_ids_core[:-1]}": True,
    }

    results: list = await network.get_responses(headers=API_HEADERS, urls=urls)
    dailies = results[0]
    dailies_core = results[1]
    today = datetime.today() - timedelta(hours=8, minutes=0)
    tomorrow = today.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=32, minutes=0)

    ret: dict = {}
    ret_core: dict = {}
    ret_pvp: list = []

    for daily in dailies:
        name: str = daily["name"].replace("Daily", "").strip()
        key, value, is_pvp = await parse_daily(name)

        if is_pvp:
            if key is not None:
                ret_pvp.append(key)
            continue

        if key is not None and value is not None:
            ret[key] = value

    for daily in dailies_core:
        name: str = daily["name"].replace("Daily", "").strip()
        key, value, is_pvp = await parse_daily(name)

        if key is not None and value is not None:
            ret_core[key] = value

    dailies_cache = {"dailies": [ret, ret_core, ret_pvp], "max_level": max_level_only}
    dailies_tomorrow_time = tomorrow
