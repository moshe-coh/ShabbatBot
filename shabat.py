import httpx


def get_shabbat(geotag: int = 281184, shabat_min: int = 50):
    times = httpx.get(f"https://www.hebcal.com/shabbat/?cfg=json&geonameid={geotag}&m={shabat_min}").json()
    data = [i for i in eval(str(times))['items'] if i["category"] == "havdalah" or i["category"] == "candles"]
    return [data[0]['title'], data[-1]['title']]


def get_in(geotag: int = 281184, shabat_min: int = 72):
    return get_shabbat(geotag, shabat_min)[0][get_shabbat(geotag, shabat_min)[0].find(r":") + 2:]


def get_out(geotag: int = 281184, shabat_min: int = 42) -> str:
    return get_shabbat(geotag, shabat_min)[-1][get_shabbat(geotag, shabat_min)[-1].find(r":") + 2:]


def get_shabbat_info(geotag: int = 281184):
    time = httpx.get(f"https://www.hebcal.com/shabbat?cfg=json&geonameid={geotag}&M=on").json()
    get = [i for i in eval(str(time))['items']]
    parasha = get[1]["hebrew"]
    date = get[1]["date"]
    return parasha, date


# 281184 ירושלים
# 294801 חיפה
# 293397 תל אביב
# באר שבע 295530
