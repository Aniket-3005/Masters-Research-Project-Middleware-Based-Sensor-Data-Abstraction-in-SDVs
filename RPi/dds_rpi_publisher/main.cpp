#include "RawImageMsgPubSubTypes.hpp"
#include "RawImageMsg.hpp"

#include <fastdds/dds/domain/DomainParticipantFactory.hpp>
#include <fastdds/dds/publisher/DataWriter.hpp>
#include <fastdds/dds/publisher/Publisher.hpp>
#include <fastdds/dds/topic/Topic.hpp>
#include <fastdds/dds/domain/DomainParticipant.hpp>
#include <fastdds/dds/topic/TypeSupport.hpp>

#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <cstdio>
#include <fstream>


using namespace eprosima::fastdds::dds;

int main() {
    // DDS setup
    DomainParticipantQos participant_qos;
    participant_qos.name("RawImagePublisher");
    DomainParticipant* participant = DomainParticipantFactory::get_instance()->create_participant(0, participant_qos);

    TypeSupport type(new sensor::RawImageMsgPubSubType());
    type.register_type(participant);

    Topic* topic = participant->create_topic("rpi_camera_raw", "sensor::RawImageMsg", TOPIC_QOS_DEFAULT);
    Publisher* publisher = participant->create_publisher(PUBLISHER_QOS_DEFAULT);
    DataWriter* writer = publisher->create_datawriter(topic, DATAWRITER_QOS_DEFAULT);

    // Launch libcamera-vid as pipe
    FILE* pipe = popen("libcamera-vid -t 0 --codec mjpeg --inline -o -", "r");
    if (!pipe) {
        std::cerr << "Failed to start libcamera-vid." << std::endl;
        return 1;
    }

    std::vector<uchar> buffer;
    uchar c;
    sensor::RawImageMsg msg;

    while (true) {
        buffer.clear();
        bool start_found = false;

        // Read until JPEG start marker (0xFF 0xD8)
        while (fread(&c, 1, 1, pipe) == 1) {
            if (!start_found && c == 0xFF) {
                fread(&c, 1, 1, pipe);
                if (c == 0xD8) {
                    buffer.push_back(0xFF);
                    buffer.push_back(0xD8);
                    start_found = true;
                    break;
                }
            }
        }

        // Continue reading until end marker (0xFF 0xD9)
        while (start_found && fread(&c, 1, 1, pipe) == 1) {
            buffer.push_back(c);
            if (buffer.size() > 2 && buffer[buffer.size() - 2] == 0xFF && buffer.back() == 0xD9) {
                break;
            }
        }

        if (buffer.empty()) continue;

        // Decode with OpenCV
        cv::Mat frame = cv::imdecode(buffer, cv::IMREAD_COLOR);
        if (frame.empty()) continue;

        // Publish via DDS
        msg.timestamp() = std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch()).count();
        msg.format() = "jpeg";
        msg.data().assign(buffer.begin(), buffer.end());

        writer->write(&msg);
        std::cout << "Published frame: " << buffer.size() << " bytes" << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(250));
    }

    pclose(pipe);
    return 0;
}
