import numpy as np
import ctypes
from picosdk.ps3000a import ps3000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
import time


def naberData(usr_range,n_pulses,time_b):
    PICOSCOPE_CHANNEL_NAMES = {"A" : 0, "B" : 1, "C" : 2, "D" : 3}
    PICOSCOPE_COUPLING_NAMES = {"DC": 1, "AC": 0}
    PICOSCOPE_RANGE_NAMES = {
        "20 mV": 0,
        "50 mV": 1,
        "100 mV": 2,
        "200 mV": 3,
        "500 mV": 4,
        "1 V": 5,
        "2 V": 6,
        "5 V": 7,
        "10 V": 8,
        "20 V": 9,
        }
    PICOSCOPE_RANGE_VOLTAGE = {
        "20 mV": 0.020,
        "50 mV": 0.050,
        "100 mV": 0.100,
        "200 mV": 0.200,
        "500 mV": 0.500,
        "1 V": 1.000,
        "2 V": 2.000,
        "5 V": 5.000,
        "10 V": 10.000,
        "20 V": 20.000,
        }
    PICOSCOPE_TRIGGER_DIRECTIONS = {
        "above": 0,
        "below": 1,
        "rising": 2,
        "falling": 3,
        }


    status = {}

    # Connect to unit
    chandle = ctypes.c_int16()
    status["openunit"] = ps.ps3000aOpenUnit(ctypes.byref(chandle), None)
    

    try:
        assert_pico_ok(status["openunit"])
    except:

        # powerstate becomes the status number of openunit
        powerstate = status["openunit"]

        # If powerstate is the same as 282 then it will run this if statement
        if powerstate == 282:
            # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
            status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 282)
        # If the powerstate is the same as 286 then it will run this if statement
        elif powerstate == 286:
            # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
            status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 286)
        else:
            raise

        assert_pico_ok(status["ChangePowerSource"])

    # Configure channels A 

    channel = 'A'
    enabled = True
    coupling = 'DC'
    range_string = usr_range
    analog_offset = 0
    status["setCh{}".format(channel)] = ps.ps3000aSetChannel(chandle,
                                            PICOSCOPE_CHANNEL_NAMES[channel],
                                            int(enabled),
                                            PICOSCOPE_COUPLING_NAMES[coupling],
                                            PICOSCOPE_RANGE_NAMES[range_string],
                                            analog_offset)
    
    assert_pico_ok(status["setCh{}".format(channel)])
    
    channel = 'B'
    enabled = True
    coupling = 'DC'
    range_string = usr_range
    analog_offset = 0
    
    status["setCh{}".format(channel)] = ps.ps3000aSetChannel(chandle,
                                            PICOSCOPE_CHANNEL_NAMES[channel],
                                            int(enabled),
                                            PICOSCOPE_COUPLING_NAMES[coupling],
                                            PICOSCOPE_RANGE_NAMES[range_string],
                                            analog_offset)
    
    assert_pico_ok(status["setCh{}".format(channel)])
    
    maxADC = ctypes.c_int16()
    status["maximumValue"] = ps.ps3000aMaximumValue(chandle, ctypes.byref(maxADC))

    # Set trigger
    """   status["trigger"] = ps.ps3000aSetSimpleTrigger(chandle,
                                                   1,
                                                   PICOSCOPE_CHANNEL_NAMES["A"],
                                                   -3201,
                                                   PICOSCOPE_TRIGGER_DIRECTIONS["falling"],
                                                   0,
                                                   0) """
    status["trigger"] = ps.ps3000aSetSimpleTrigger(chandle,
                                                   1,
                                                   PICOSCOPE_CHANNEL_NAMES["B"],
                                                   5201,
                                                   PICOSCOPE_TRIGGER_DIRECTIONS["rising"],
                                                   0,
                                                   0)                
    
    assert_pico_ok(status["trigger"])

    
    # Run rapid block capture twice
    n_waveforms = n_pulses
    pre_samples = 700
    post_samples = 2000
    total_samples = pre_samples + post_samples
    
    # Get timebase information
    # handle = chandle
    # timebase = 8 = timebase
    # noSamples = totalSamples
    # pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalNs)
    # pointer to totalSamples = ctypes.byref(returnedMaxSamples)
    # segment index = 0
    timebase = time_b
    timeIntervalns = ctypes.c_float()
    returnedMaxSamples = ctypes.c_int32()
    oversample = ctypes.c_int16(0)
    status["getTimebase2"] = ps.ps3000aGetTimebase2(chandle,
                                                    timebase,
                                                    total_samples,
                                                    ctypes.byref(timeIntervalns),
                                                    oversample,
                                                    ctypes.byref(returnedMaxSamples),
                                                    0)
    assert_pico_ok(status["getTimebase2"])
    
    print(timeIntervalns, returnedMaxSamples, oversample)

    status["SetNoOfCaptures"] = ps.ps3000aSetNoOfCaptures(chandle,n_waveforms)
    
    assert_pico_ok(status["SetNoOfCaptures"])

    cMaxSamples = ctypes.c_int32()
    status["memorySegments"] = ps.ps3000aMemorySegments(chandle,
                                                        n_waveforms,
                                                        ctypes.byref(cMaxSamples))
    assert_pico_ok(status["memorySegments"])
    # print("Maximum number of samples:", cMaxSamples)
    oversample = ctypes.c_int16(0)
    pParameter = ctypes.c_bool(False)
    
    status["runBlock"] = ps.ps3000aRunBlock(chandle,
                                            pre_samples,
                                            post_samples,
                                            timebase,
                                            oversample,
                                            None,
                                            0, # Fails when 10 or above, works for 0-9
                                            None,
                                            None)
    assert_pico_ok(status["runBlock"])

    # Wait
    ready = ctypes.c_int16(0)
    check = ctypes.c_int16(0)
    while ready.value == check.value:
        status["isReady"] = ps.ps3000aIsReady(chandle, ctypes.byref(ready))
    # Check the number of captured scans

    nCaptures = ctypes.c_uint32()
    status["GetNoOfProcessedCaptures"] = ps.ps3000aGetNoOfProcessedCaptures(chandle,ctypes.byref(nCaptures))
    assert_pico_ok(status["GetNoOfProcessedCaptures"])
    print("Number of processed captures:", nCaptures.value)

    # Stop data capture
    status["stop"] = ps.ps3000aStop(chandle)
    assert_pico_ok(status["stop"])

    # Download channel B only
    channel = "A"
    buffer = (ctypes.c_int16 * total_samples)()
    results = np.empty((total_samples, n_waveforms), dtype=np.float32)
    for segment in range(n_waveforms):
        cmaxSamples = ctypes.c_int32(total_samples)
        overflow = ctypes.c_int16()

        status["setDataBuffer{}".format(channel)] = ps.ps3000aSetDataBuffer(chandle,
                                                                            PICOSCOPE_CHANNEL_NAMES[channel],
                                                                            ctypes.byref(buffer),
                                                                            total_samples,
                                                                            segment,
                                                                            0)
        assert_pico_ok(status["setDataBuffer{}".format(channel)])

        status["getValues"] = ps.ps3000aGetValues(chandle,
                                                  0,
                                                  ctypes.byref(cmaxSamples),
                                                  0, # downSampleRatio
                                                  0, # ps.PS3000a_RATIO_MODE['PS3000a_RATIO_MODE_NONE']
                                                  segment,
                                                  ctypes.byref(overflow))
        assert_pico_ok(status["getValues"])
        
        maxADC = ctypes.c_int16()
        status["maximumValue"] = ps.ps3000aMaximumValue(chandle, ctypes.byref(maxADC))
        assert_pico_ok(status["maximumValue"])
        adc2mVChAMax =  adc2mV(buffer,  PICOSCOPE_RANGE_NAMES[range_string], maxADC)

        # Converts ADC from channel A to mV
        

        results[:,segment] = adc2mVChAMax
    # Close unitDisconnect the scope
    # handle = chandle
    status["close"] = ps.ps3000aCloseUnit(chandle)
    assert_pico_ok(status["close"])
    
    return results, total_samples
    # Close unitDisconnect the scope
    # handle = chandle
    
    
    

