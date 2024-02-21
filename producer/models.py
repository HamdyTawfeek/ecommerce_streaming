import json
import random
from dataclasses import asdict, dataclass, field
from datetime import datetime

from faker import Faker

faker = Faker()


@dataclass
class Purchase:
    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    )
    username: str = field(default_factory=faker.user_name)
    city: str = field(default_factory=faker.city)
    country: str = field(
        default_factory=lambda: random.choice(
            ["Germany", "Italy", "Spain", "France", "Poland"]
        )
    )
    postal_code: str = field(default_factory=faker.postalcode)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(10, 2000))

    def serialize(self):
        """Serializes the object in JSON string format"""
        return json.dumps(asdict(self))
