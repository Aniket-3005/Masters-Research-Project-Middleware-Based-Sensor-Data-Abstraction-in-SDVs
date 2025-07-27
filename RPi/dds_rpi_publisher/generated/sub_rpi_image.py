import time
import fastdds
import RawImageMsg
import _RawImageMsgWrapper  # Required by SWIG binding

class RawImageMsgListener(fastdds.DataReaderListener):
    def __init__(self):
        super().__init__()

    def on_data_available(self, reader):
        info = fastdds.SampleInfo()
        msg = RawImageMsg.RawImageMsg()

        if reader.take_next_sample(msg, info) == fastdds.ReturnCode_t.RETCODE_OK:
            if info.valid_data:
                print(f"Image received from: {msg.camera_source()}")
                filename = f"recv_{int(time.time())}.jpg"
                with open(filename, "wb") as f:
                    f.write(msg.image_data().encode("latin1"))
                print(f"Image saved as {filename} ({len(msg.image_data())} bytes)")

# === Fast DDS Setup ===
participant_qos = fastdds.DomainParticipantQos()
participant = fastdds.DomainParticipantFactory.get_instance().create_participant(0, participant_qos)

# Register Type
msg_type = RawImageMsg.RawImageMsgPubSubType()
participant.register_type(msg_type)

# Create Topic
topic = participant.create_topic("rpi_cam_raw_image", msg_type.get_type_name(), fastdds.TopicQos())

# Create Subscriber + Listener
subscriber = participant.create_subscriber(fastdds.SubscriberQos())
listener = RawImageMsgListener()

# Create DataReader
reader = subscriber.create_datareader(topic, fastdds.DataReaderQos(), listener)

print("Subscriber running. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n Exiting...")
