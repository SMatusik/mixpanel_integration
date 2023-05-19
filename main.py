import logging
from datetime import datetime
from uuid import uuid4, UUID

from fastapi import FastAPI
from mixpanel import Mixpanel

MIXPANEL_TOKEN = "token"  # change it
USER_ID = uuid4()

logger = logging.getLogger(__name__)

app = FastAPI(debug=True)
mp = Mixpanel(MIXPANEL_TOKEN)


@app.get("/send_event")
async def send_event(user_id: UUID = USER_ID):
    event_name = "user logged-in"
    payload = {"username": "user@example.net", "timestamp": datetime.now()}
    mp.track(
        distinct_id=str(user_id),
        event_name=event_name,
        properties=payload)

    logger.warning("successfully sent event: {} for user: {}".format(event_name, datetime))


@app.get("/set_user")
async def add_user(user_id: UUID = USER_ID, email: str = "patrick.smith@example.com"):
    mp.people_set(
        distinct_id=str(user_id),
        properties={
            "$first_name": "Patrick",
            "$last_name": "Smith",
            "$email": email,
        }
    )
    logger.warning("successfully set user with email {}".format(email))


@app.get("/unset_property")
async def unset_property(user_id: UUID = USER_ID, property_name: str = "$last_name"):
    mp.people_unset(
        distinct_id=str(user_id),
        properties=[property_name]
    )
    logger.warning("successfully unset property {} for user {}".format(property_name, user_id))


@app.get("/charge_user")
async def unset_property(user_id: UUID = USER_ID, amount: int = 5):
    mp.people_track_charge(
        distinct_id=str(user_id),
        amount=amount,
        properties={"source": "top-up"},
    )
    logger.warning("successfully charged user {} for {} EUR".format(user_id, amount))
