"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys




CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

p = pyaudio.PyAudio()

deviceCount = p.get_device_count()
print("Device count:",deviceCount)

for i in range(0, deviceCount):
    deviceInfo = p.get_device_info_by_index(i)
    print("Device " + str(i) + ": ")
    print(deviceInfo)


hostApiInfoCount = p.get_host_api_count()
print("Host Api Count:",hostApiInfoCount)

for i in range(0, hostApiInfoCount):
    hostApiInfo = p.get_host_api_info_by_index(i)
    print("Host Api " + str(i) + ": ")
    print(hostApiInfo)

wf = wave.open(sys.argv[1], 'rb')
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)



print(wf)
data = wf.readframes(CHUNK)
while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)
stream.stop_stream()
stream.close()





# data = wf.readframes(CHUNK)
# while data != '':
#     stream.write(data)
#     data = wf.readframes(CHUNK)


# while(True):
#
#
#
#
#     time.sleep(2)




p.terminate()