import json
import logging
import logging.config
import os
import traceback

import paho.mqtt.client as mqtt
from sht20 import SHT20

MQTT_IP = ""
MQTT_PORT = 1883
MQTT_TOPIC = ""
MQTT_USER = ""
MQTT_PASS = ""

dname = os.path.dirname(__file__)
os.chdir(dname)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def value_in_range(value, range_min, range_max):
    if range_min <= value <= range_max:
        logger.debug(f"Value: {value} in range: [{range_min}, {range_max}]")
        return True
    logger.error(f"Value: {value} out of range: [{range_min}, {range_max}]")
    return False


def mqtt_publish(record):
    payload = json.dumps(record)
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, password=MQTT_PASS)
    client.connect(MQTT_IP, MQTT_PORT)
    client.loop_start()
    logger.debug("Publishing to MQTT broker...")
    ret = client.publish(MQTT_TOPIC, payload, 0)
    ret.wait_for_publish(1)
    if ret.is_published():
        logger.info("Publish successful")
    else:
        logger.debug(f"Publish not successful. Returned: {ret}")
    client.loop_stop()
    client.disconnect()
    logger.debug("MQTT client disconnected")


def main():
    sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)
    temp = round(sht.read_temp(), 3)
    hum = round(sht.read_humid(), 3)
    if value_in_range(temp, -2.0, 41.0) and value_in_range(hum, 5.0, 100.0):
        record = {
            "stationID": 1,
            "count": 1,
            "Tmin": temp,
            "Tmax": temp,
            "Tmean": temp,
            "Tstdev": 0,
            "RHmin": hum,
            "RHmax": hum,
            "RHmean": hum,
            "RHstdev": 0,
            "freeHeap": 0,
        }
        mqtt_publish(record)


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
