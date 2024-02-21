import os
from dataclasses import dataclass
from datetime import timedelta

import faust
from database import conn, purchase_summmary

BROKER_URL = os.environ["BROKER_URL"]
TOPIC_NAME = os.environ["TOPIC_NAME"]


@dataclass
class PurchaseEvent(faust.Record):
    created_at: str
    username: str
    city: str
    country: str
    postal_code: str
    currency: str
    amount: int


app = faust.App("consumer", broker=BROKER_URL)
purchases_topic = app.topic(TOPIC_NAME, value_type=PurchaseEvent)
purchases_summary_table = app.Table("totals", default=int).tumbling(
    timedelta(minutes=1), expires=timedelta(minutes=1)
)


@app.agent(purchases_topic)
async def purchase(purchases):
    async for purchase in purchases.group_by(PurchaseEvent.country):

        purchases_summary_table[purchase.country] += purchase.amount

        print(
            f"{purchase.country}: {purchases_summary_table[purchase.country].current()}"
        )

        query = purchase_summmary.insert().values(
            {
                "created_at": purchase.created_at,
                "country": purchase.country,
                "amount": purchases_summary_table[purchase.country].current(),
            }
        )
        conn.execute(query)


if __name__ == "__main__":
    app.main()
