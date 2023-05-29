
# getting cpu ID
import machine, microcontroller
print(machine.unique_id())
print(microcontroller.cpu.uid)


# getting CPU temperature
import microcontroller
microcontroller.cpu.temperature
