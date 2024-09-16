import asyncio
from typing import Generator

import pystac
import pystac_client
from download_utils import download_item, replace_href
from settings import (
    COLLECTION,
    DATA_ORBIT_DIR,
    END_DATE,
    FORMAT,
    STAC_API_URL,
    START_DATE,
)


def search_orbit_item() -> Generator[pystac.Item, None, None]:
    start_date = START_DATE

    while True:
        client = pystac_client.Client.open(STAC_API_URL)
        searched_items = client.search(
            collections=[COLLECTION],
            datetime=f"{start_date.strftime(FORMAT)}/{END_DATE.strftime(FORMAT)}",
        )  # 1度に検索可能な最大数は2000

        found = 0

        for item in searched_items.items():
            found += 1

            if start_date < item.datetime.replace(tzinfo=None):
                start_date = item.datetime.replace(tzinfo=None)

            if item.id.startswith("S1A_OPER_AUX_RESORB_OPOD") and item.id.endswith(
                ".EOF"
            ):
                yield item

        if found == 2000:
            print("Found exactly 2000 items, continuing...")
            continue
        elif found < 2000:
            print("Found fewer than 2000 items, stopping the search.")
            break
        else:
            raise RuntimeError("Unexpected number of items found, more than 2000.")


if __name__ == "__main__":
    for item in search_orbit_item():
        item = replace_href(item)
        output_dir = DATA_ORBIT_DIR / item.datetime.strftime("%Y-%m-%d")
        output_dir.mkdir(exist_ok=True)
        asyncio.run(download_item(item, output_dir))
