from bs4 import BeautifulSoup

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


async def get_daily_ids() -> str:
    response: dict = await network.get_response(headers=API_HEADERS, url="https://api.guildwars2.com/v2/achievements/daily")
    dailies: dict = response.get("pve") + response.get("wvw") + response.get("pvp")
    daily_ids: str = ""

    for daily in dailies:
        required_access = daily.get("required_access")
        max_level: int = daily["level"]["max"]

        if required_access is None or required_access["condition"] == "HasAccess":
            if max_level == 80:
                daily_ids += f"{str(daily['id'])},"

    return daily_ids


async def get_daily_data(daily_ids: str) -> tuple:
    urls: dict = {
        f"https://api.guildwars2.com/v2/achievements?ids={daily_ids[:-1]}": True,
        "https://wiki.guildwars2.com/wiki/Daily/easy_dailies": False,
    }

    results: list = await network.get_responses(headers=API_HEADERS, urls=urls)
    easy_table = BeautifulSoup(results[1], "html.parser").find_all("table", class_="pve table")[0]
    return results[0], easy_table


def find_easy_waypoint(area: str, task: str, easy_table, map_data):
    if area == "Maguuma Jungle" or area == "Maguuma":
        area = "Maguuma (Jungle)"

    if "Vista Viewer" in task:
        task = "Vista"

    rows: list = easy_table.find_all("tr")
    i: int = 0

    for i in range(len(rows)):
        if rows[i].text.strip() == area:
            break

    try:
        rows = rows[i:]
        row = [tr for tr in rows if tr.text.strip().startswith(task)][0]
        data: list = [td for td in row.find_all("td")]
        waypoint_name = [a for d in data for a in d.find_all("a") if "Waypoint" in a.text][0]
        waypoint = map_data.get(waypoint_name.text.strip())
    except Exception:
        waypoint = None

    return waypoint


async def parse_daily(name: str, easy_table, map_data) -> tuple:
    if name == "WvW Big Spender":
        return name, "Spend Badges of Honor on traps or at guild hall vendor."

    if "PvP" in name or name == "Top Stats":
        task: str = name.replace("PvP", "").strip()
        if task in PVP_DAILIES:
            return name, "Custom arena - [LOFT] or [TTS]"
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

    if "Desert" in area and ("Forager" in task or "Miner" in task or "Lumberer" in task):
        return name, "Guild Hall"

    waypoint = find_easy_waypoint(area, task, easy_table, map_data)
    return name, waypoint


async def get_dailies(map_data: dict) -> dict:
    daily_ids: str = await get_daily_ids()
    dailies, easy_table = await get_daily_data(daily_ids)
    ret: dict = {}

    for daily in dailies:
        name: str = daily["name"].replace("Daily", "").strip()
        key, value = await parse_daily(name, easy_table, map_data)

        if key is not None and value is not None:
            ret[key] = value

    return ret
