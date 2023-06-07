# Reading uplink messages

`retrieve_uplinks.py` is an example how one can obtain messages sent to an
[application](https://www.thethingsindustries.com/docs/integrations/adding-applications/).
For each application one can enable a list of
[integrations](https://www.thethingsindustries.com/docs/integrations/adding-integrations/).
The one used here is the
[storage integration](https://www.thethingsindustries.com/docs/integrations/storage/),
which retains data for 24 hours for The Things Stack Community Edition.
It offers an
[HTTP API](https://www.thethingsindustries.com/docs/integrations/storage/retrieve/#retrieve-uplinks-using-the-http-api)
with which one can retrieve uplink messages.

In order to be able to use this API, one needs to generate an API key using the
[TTN Console](https://eu1.cloud.thethings.network/console/).
Add this key as `API_KEY` variable in the script and then execute it:

```shell
python3 retrieve_uplinks.py
```

An example response looks like this:

```json
{
    "result": {
        "end_device_ids": {
            "device_id": "eui-2cf7f1205020aa6d",
            "application_ids": {
                "application_id": "makezurich-badge-2023"
            },
            "dev_eui": "2CF7F1205020AA6D",
            "dev_addr": "260BEB3F"
        },
        "received_at": "2023-06-06T19:33:16.108116083Z",
        "uplink_message": {
            "f_port": 8,
            "f_cnt": 2,
            "frm_payload": "SGVsbG8gY2xlbWVucyAx",
            "rx_metadata": [
                {
                    "gateway_ids": {
                        "gateway_id": "uzhloragwstb",
                        "eui": "B827EBFFFE03753A"
                    },
                    "time": "2023-06-06T19:33:15.888578Z",
                    "timestamp": 4131444884,
                    "rssi": -117,
                    "channel_rssi": -117,
                    "snr": 2.8,
                    "location": {
                        "latitude": 47.382,
                        "longitude": 8.541,
                        "altitude": 433,
                        "source": "SOURCE_REGISTRY"
                    },
                    "received_at": "2023-06-06T19:33:15.901787419Z"
                },
                {
                    "gateway_ids": {
                        "gateway_id": "b827ebfffe97f686",
                        "eui": "B827EBFFFE97F686"
                    },
                    "time": "2023-06-06T19:33:15.892148Z",
                    "timestamp": 840985860,
                    "rssi": -107,
                    "channel_rssi": -107,
                    "snr": 8.8,
                    "received_at": "2023-06-06T19:33:15.902936144Z"
                }
            ],
            "settings": {
                "data_rate": {
                    "lora": {
                        "bandwidth": 125000,
                        "spreading_factor": 9,
                        "coding_rate": "4/5"
                    }
                },
                "frequency": "868100000",
                "timestamp": 4131444884,
                "time": "2023-06-06T19:33:15.888578Z"
            },
            "received_at": "2023-06-06T19:33:15.902662084Z",
            "confirmed": true,
            "consumed_airtime": "0.226304s",
            "network_ids": {
                "net_id": "000013",
                "tenant_id": "ttn",
                "cluster_id": "eu1",
                "cluster_address": "eu1.cloud.thethings.network"
            }
        }
    }
}
```
