import datetime as dt
import logging
import time

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import WriteType

from config import INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN, ENVIRONMENT, ENABLE_METRICS

logger = logging.getLogger(__name__)

update_types = {
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "inline_query",
    "chosen_inline_result",
    "callback_query",
    "shipping_query",
    "pre_checkout_query",
}

if ENABLE_METRICS:
    influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_options = WriteOptions(
        write_type=WriteType.asynchronous,
        batch_size=500,
        flush_interval=5_000,
        retry_interval=1_000,
        max_retries=1,
        max_retry_delay=2_000,
        exponential_base=1
    )
    writer = influxdb_client.write_api(write_options=write_options)


def send_metric(measurement: str, tags: dict, fields: dict):
    tags.update(service="bot-api-search", testing=ENVIRONMENT)
    data = {
        "measurement": measurement,
        "tags": tags,
        "fields": fields
    }
    record = Point.from_dict(data).time(dt.datetime.utcnow())
    try:
        writer.write(bucket=INFLUXDB_BUCKET, record=record)
    except Exception as e:
        logger.exception(f"Can't write to bucket: {e}")


def measure_time_metric(subject_type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            res = func(*args, **kwargs)

            if not ENABLE_METRICS:
                return res

            time_data = {
                "measurement": "spent_time",
                "tags": {
                    "env": ENVIRONMENT,
                    "type": subject_type,
                    "func_name": func.__name__,
                },
                "fields": {
                    "time_delta": time.monotonic() - start
                }
            }
            send_metric(time_data)

            return res

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator


class MetricsMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, *args):
        for t in update_types:
            if getattr(update, t):
                update_type = t
                break
        else:
            update_type = "unknown"

        tags = {"type": update_type}
        fields = {"id": update.update_id}

        if update_type == "chosen_inline_result":
            fields.update(chosen_result=update.chosen_inline_result.result_id)

        send_metric(
            measurement="updates",
            tags=tags,
            fields=fields
        )
