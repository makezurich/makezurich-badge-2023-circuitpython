import mz_badge

appkey = "YOUR_APP_KEY_HERE, eg. FFFFFFFFFFFFFFFFFF"
appeui = "YOUR_APPEUI_HERE, eg. AAAAAAAAAAAA"

lora_module = mz_badge.LoRaModule()
lora_module.show_information()

lora_module.setup_and_join_otaa(appkey, appeui)
lora_module.send_string("01234567")
