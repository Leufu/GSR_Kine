#pragma once

// Utility helpers for working with FSR data.
//extern FSR_data_t;

/*
void printFSRData(FSR_data_t &data)
{
	Serial.printf("t: %d, F0: %d, F1: %d, F2: %d, F3: %d",data.time_stamp,data.FSR_0,data.FSR_1,data.FSR_2,data.FSR_3);
}
*/


// Convert an FSR_data_t structure to a CSV string stored in `buffer`.

void GSRDataToCSV_char(GSR_data_t *data, char *buffer, size_t bufferSize)
{
  snprintf(buffer, bufferSize,"%"PRId64",%"PRIu16,data->time_stamp,data->GSR);
}


/*
void FSRDataToCSV_char(FSR_data_t *data, char *buffer, size_t bufferSize)
{
  snprintf(buffer, bufferSize,
           "%"PRId64",%"PRIu16",%"PRIu16",%"PRIu16",%"PRIu16",%"PRIu16",%"PRIu16",%"PRIu16",%"PRIu16,
           data->time_stamp,
           data->FSR_0,
                          data->FSR_1,
                          data->FSR_2,
           data->FSR_3,
                          data->FSR_4,
                          data->FSR_5,
                                data->FSR_6,
                          data->FSR_7
                          );
}

*/

