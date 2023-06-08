# Why
The more data we send the longer we are on air and use battery.
For example a JSON payload versus handcrafted payload:
```
# json   7b226465766963655f7374617465223a312c226c61746974756465223a34372e3430313333303530333439323539352c226c6f6e676974757465223a382e3339303131393232393637383930322c2274656d7065726174757265223a32352e342c2268756d6964697479223a3232352c22636f325f70706d223a313234307d
# idddii 000000004047b35f000000004020c7be00000000403966660000000000000019000004d8
# bdddbh 004047b35f000000004020c7be0000000040396666000000001904d8
# bfffbi 00423d9af841063df041cb333019000004d8
# bfffbh 00423d9af841063df041cb33301904d8


```


# Payload formatter
Without formatter the data will only be available as base64 property under
```
{
  "data": {
    "uplink_message": {
      "frm_payload": "AEI9mvhBBj3wQcszMBkE2A==",
```

by using a formatter we get data with properties
```
{
  "data": {
    "uplink_message": {
      "decoded_payload": {
        "co2_ppm": 1240,
        "device_state": 0,
        "humidity": 25,
        "latitude": 47.401336669921875,
        "longitude": 8.390121459960938,
        "temperature": 25.399993896484375
      },
```

The example [ttn_payload_formatter.js](ttn_payload_formatter.js) shows how to parse the fixed length into properties with the JavaScript DataView API.

```javascript
  let buffer = new ArrayBuffer(bytes.length)
  let view = new DataView(buffer)
  for (let i=0;i<bytes.length;i++) { // load the bytes into the dataview
    view.setUint8(i, bytes[i])
  }
  // from top to bottom the offset and size of the previous property is used
  let data = {
    device_state: view.getUint8(0), // 1byte
    latitude: view.getFloat32(1, false), // 4byte
    longitude: view.getFloat32(5, false),
    temperature: view.getFloat32(9, false),
    humidity: view.getUint8(13),
    co2_ppm: view.getInt16(14),
  }
```

# Errors
If errors array contains a value, uplink_message.decoded_payload will be undefined.

# Warnings
If something happens the decoded_payload_warnings will be populated.
```
{
  "data": {
    "uplink_message": {
      "decoded_payload": {},
      "decoded_payload_warnings": [
        "Skipping decode: payload length did not match, got 16"
      ],
```
