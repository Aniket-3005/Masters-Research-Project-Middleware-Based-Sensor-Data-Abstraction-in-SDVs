#include "RawImageMsgPubSubTypes.hpp"
#include "RawImageMsg.hpp"

#include <fastdds/dds/domain/DomainParticipantFactory.hpp>
#include <fastdds/dds/subscriber/DataReader.hpp>
#include <fastdds/dds/subscriber/DataReaderListener.hpp>
#include <fastdds/dds/subscriber/Subscriber.hpp>
#include <fastdds/dds/topic/Topic.hpp>
#include <fastdds/dds/domain/DomainParticipant.hpp>
#include <fastdds/dds/topic/TypeSupport.hpp>

#include <fstream>
#include <iostream>
#include <thread>

using namespace eprosima::fastdds::dds;

class RawImageListener : public DataReaderListener {
public:
    void on_data_available(DataReader* reader) override {
        sensor::RawImageMsg msg;
        SampleInfo info;
	if (reader->take_next_sample(&msg, &info) && info.valid_data)
            std::cout << "Received image of size: " << msg.data().size() << " bytes" << std::endl;
            std::ofstream outfile("/tmp/rpi_image.jpg", std::ios::binary);
            outfile.write(reinterpret_cast<const char*>(msg.data().data()), msg.data().size());
            outfile.close();
        }
};

int main() {
    DomainParticipantQos participant_qos;
    DomainParticipant* participant = DomainParticipantFactory::get_instance()->create_participant(0, participant_qos);

    TypeSupport type(new sensor::RawImageMsgPubSubType());
    type.register_type(participant);

    Topic* topic = participant->create_topic("rpi_camera_raw", "sensor::RawImageMsg", TOPIC_QOS_DEFAULT);
    Subscriber* subscriber = participant->create_subscriber(SUBSCRIBER_QOS_DEFAULT);

    RawImageListener* listener = new RawImageListener();
    DataReaderQos reader_qos;
    DataReader* reader = subscriber->create_datareader(topic, reader_qos, listener);

    std::cout << "DDS Subscriber running... Saving images to /tmp/rpi_image.jpg" << std::endl;
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    return 0;
};
