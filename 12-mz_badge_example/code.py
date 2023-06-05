import mz_badge
import os

lora_module = mz_badge.LoRa_module()
lora_module.show_information()

#lora_module.setup_and_join_otaa(os.getenv(mode), os.getenv(appkey), os.getenv(appeui))
lora_module.join()

lora_module.send_string('01234567')