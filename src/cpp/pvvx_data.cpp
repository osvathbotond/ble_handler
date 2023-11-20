#include <pybind11/pybind11.h>

#include <chrono>
#include <array>

const uint8_t PVXX_MESSAGE_SIZE = 18;
const uint16_t PVXX_MESSAGE_UUID = 0x181A;
const size_t PVXX_STRUCT_SIZE = 11*sizeof(uint8_t) + sizeof(int16_t) + 3*sizeof(uint16_t);

uint32_t currentTime() {
    auto now = std::chrono::system_clock::now().time_since_epoch();
    return static_cast<uint32_t>(std::chrono::duration_cast<std::chrono::seconds>(now).count());
}

struct PVVXData {
    uint8_t                size;           // = 18
    uint8_t                uid;            // = 0x16, 16-bit UUID
    uint16_t               UUID;           // = 0x181A, GATT Service 0x181A Environmental Sensing
    std::array<uint8_t, 6> MAC;            // [0] - lo, .. [6] - hi digits
    int16_t                temperature;    // x 0.01 degree
    uint16_t               humidity;       // x 0.01 %
    uint16_t               battery_mv;     // mV
    uint8_t                battery_level;  // 0..100 %
    uint8_t                counter;        // measurement count
    uint8_t                flags;
    uint32_t               timestamp;


    PVVXData(const char* data) {
        std::memcpy(this, data, PVXX_STRUCT_SIZE);
        this->timestamp = currentTime();
    }
};

PVVXData PVVXDataFromMessage(const char* message) {
    return PVVXData(message);
}

bool checkType(const char* message) {
    const uint8_t size = *reinterpret_cast<const uint8_t*>(message);
    const uint16_t uuid = *reinterpret_cast<const uint16_t*>(message+2);
    return size == PVXX_MESSAGE_SIZE && uuid == PVXX_MESSAGE_UUID;
}

pybind11::dict toJson(const PVVXData& data, const std::string& name) {
    using namespace pybind11::literals; // to bring in the `_a` literal
    return pybind11::dict("name"_a=name,
                          "timestamp"_a=data.timestamp,
                          "temperature"_a=data.temperature/100.0f,
                          "humidity"_a=data.humidity/100.0f,
                          "battery"_a=data.battery_level);
}

PYBIND11_MODULE(_pvvx_data, m) {
    pybind11::class_<PVVXData>(m, "PVVXData")
        .def("to_json", &toJson)
        .def_readonly("size", &PVVXData::size)
        .def_readonly("uid", &PVVXData::uid)
        .def_readonly("UUID", &PVVXData::UUID)
        .def_readonly("MAC", &PVVXData::MAC)
        .def_readonly("temperature", &PVVXData::temperature)
        .def_readonly("humidity", &PVVXData::humidity)
        .def_readonly("battery_mv", &PVVXData::battery_mv)
        .def_readonly("battery_level", &PVVXData::battery_level)
        .def_readonly("counter", &PVVXData::counter)
        .def_readonly("flags", &PVVXData::flags)
        .def_readonly("timestamp", &PVVXData::timestamp)
        .def_static("check_type", &checkType)
        .def_property_readonly_static("from_message", [](pybind11::object){return pybind11::cpp_function(PVVXDataFromMessage);});
}