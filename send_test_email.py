from email_utils import send_results_email
import pandas as pd

# Tiny fake dataframe
df = pd.DataFrame(
    [
        {
            "unit_id": "TEST1",
            "community": "Demo Place",
            "rent": 1234,
            "beds": 1,
            "baths": 1,
            "sqft": 600,
            "amenities": "gym,pool",
            "available_from": "2025-02-01",
            "pets": "allowed",
        }
    ]
)

send_results_email("avikshith.y@gmail.com", df)