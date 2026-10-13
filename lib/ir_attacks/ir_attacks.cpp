#include "ArduinoJson.h"
#include "FreeRTOS.h"
#include "IrFramework.hpp"
#include "freertos/task.h"
#include "ir_attacks_task.hpp"
#include "ir_attacks_types.h"
#include "posixsd.hpp"

TaskHandle_t record_task_handle;

// Must outlive this function: the task reads it after we return, so a
// stack-local here is a use-after-free that crashes IR record. Only one record
// runs at a time, so a file-scope instance is safe.
static IrAttackTaskParams record_params;

TaskHandle_t ir_record_signal(IRRecordSignalPage *page,
                              IrFramework *framework) {
  record_params.ir_framework = framework;
  record_params.page = page;
  xTaskCreate(ir_record_signal_task, "ir_record_signal_task", 8000,
              &record_params, 5, &record_task_handle);
  return record_task_handle;
}

RecordedSignal json_to_signal(JsonDocument signal) {
  RecordedSignal parsed_signal;
  parsed_signal.protocol = signal["protocol"];
  JsonArray raw_data = signal["raw_data"];
  uint16_t len = signal["raw_len"];
  parsed_signal.address = signal["address"];
  parsed_signal.command = signal["command"];
  parsed_signal.decodedRawData = signal["decoded_raw_data"];
  parsed_signal.numberOfBits = signal["number_of_bits"];
  parsed_signal.flags = signal["flags"];
  /* Only PulseWidth/PulseDistance and Unknown require decodedRawDataArray, so
   * memory for others protocols */
  if (parsed_signal.protocol >= 0 && parsed_signal.protocol <= 2) {
    for (size_t i = 0; i < len; i++) {
      parsed_signal.decodedRawDataArray[i] = raw_data[i];
    }
  }
  parsed_signal.raw_len = len;
  return parsed_signal;
}

void ir_send_signal(IrFramework *framework, JsonDocument *signal_doc,
                    IRListsProgress *progress_page,
                    TaskHandle_t *list_handler) {
  RecordedSignal parsed_signal = json_to_signal(*signal_doc);
  if (signal_doc->is<JsonArray>()) {
    // Same lifetime issue as record: keep the params alive past this call.
    static IrAttackTaskParams emit_params;
    emit_params.ir_framework = framework;
    emit_params.signal = signal_doc;
    emit_params.progress_page = progress_page;
    xTaskCreate(ir_list_emit, "ir_list_emit", 20000, &emit_params, 5,
                list_handler);
  } else {
    RecordedSignal parsed_signal = json_to_signal(*signal_doc);
    framework->send_protocol_signal(parsed_signal);
  }
  framework->send_protocol_signal(parsed_signal);
}