#pragma once
#include <esp_sntp.h>

// Simple helper to query the current time in microseconds.
struct timeval tv_now;

// Return the current system time in microseconds.
int64_t get_time_us()
{
        gettimeofday(&tv_now, NULL);
        int64_t time_us = (int64_t)tv_now.tv_sec * 1000000L + (int64_t)tv_now.tv_usec;
        return time_us;
}

