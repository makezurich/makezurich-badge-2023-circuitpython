// Using the DataView API to parse the bytes of a fixed length payload,
// Decoded data will be available as uplink_message.decoded_payload
// If decoding failed uplink_message.decoded_payload will be an empty object {}
function decodeUplink(input) {
  let bytes = input.bytes
  if (input.bytes.length != 16) {
    return {
      errors: ['Payload length did not match, got ' + input.bytes.length],
    }
  }

  let buffer = new ArrayBuffer(bytes.length)
  let view = new DataView(buffer)
  for (let i=0;i<bytes.length;i++) { // load the bytes into the dataview
    view.setUint8(i, bytes[i])
  }
  // from top to bottom the offset and size of the previous property is used
  let data = {
    device_state: view.getUint8(0), // 1byte
    latitude:  view.getFloat32(1, false), // 4byte
    longitude: view.getFloat32(5, false),
    temperature: view.getFloat32(9, false),
    humidity: view.getUint8(13),
    co2_ppm: view.getInt16(14),
  }

  return {
    data: data,
    warnings: [], // optional
    errors: [], // optional (if set, the decoding failed)
  }
}
