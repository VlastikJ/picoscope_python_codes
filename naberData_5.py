import numpy as np
import ctypes
from picosdk.ps5000a import ps5000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
import time

def naberData_5(usr_range,n_pulses,time_b, sec_C_range):
    PICOSCOPE_CHANNEL_NAMES = {"A" : 0, "B" : 1, "C" : 2, "D" : 3}
    PICOSCOPE_COUPLING_NAMES = {"DC": 1, "AC": 0}
    PICOSCOPE_RANGE_NAMES = {
        "10 mV": 0,
        "20 mV": 1,
        "50 mV": 2,
        "100 mV": 3,
        "200 mV": 4,
        "500 mV": 5,
        "1 V": 6,
        "2 V": 7,
        "5 V": 8,
        "10 V": 9,
        "20 V": 10,
        }
    PICOSCOPE_RANGE_VOLTAGE = {
        "10 mV": 0.010,
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
        
    DEVICE_RESOLUTION= {
         "8-bit": 0,
        "12-bit": 1,
        "14-bit": 2,
        "15-bit": 3,
        "16-bit": 4,
        }
        


    status = {}

    # Connect to unit
    chandle = ctypes.c_int16()
    status["openunit"] = ps.ps5000aOpenUnit(ctypes.byref(chandle), None,1)
    

    try:
        assert_pico_ok(status["openunit"])
    except:

        # powerstate becomes the status number of openunit
        powerstate = status["openunit"]

        # If powerstate is the same as 282 then it will run this if statement
        if powerstate == 282:
            # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
            status["ChangePowerSource"] = ps.ps5000aChangePowerSource(chandle, 282)
        # If the powerstate is the same as 286 then it will run this if statement
        elif powerstate == 286:
            # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
            status["ChangePowerSource"] = ps.ps5000aChangePowerSource(chandle, 286)
        else:
            raise

        assert_pico_ok(status["ChangePowerSource"])
    
    
    status["resolution"] = ps.ps5000aSetDeviceResolution(chandle,DEVICE_RESOLUTION["12-bit"])
    assert_pico_ok(status["resolution"])
    # Configure channels A 

    
    coupling = 'DC'
    range_string = usr_range
    analog_offset = 0
    #if you use resolution 16-bit you have to use only one channel - others you have to disabled !!! number of channels depends on power source !!!
    
    enabled = True
    if sec_C_range == 0:
        channel = 'A'
        status["setCh{}".format(channel)] = ps.ps5000aSetChannel(chandle,
                                                                 PICOSCOPE_CHANNEL_NAMES[channel],
                                                                 int(enabled),
                                                                 PICOSCOPE_COUPLING_NAMES[coupling],
                                                                 PICOSCOPE_RANGE_NAMES[range_string],
                                                                 analog_offset)
        assert_pico_ok(status["setCh{}".format(channel)])
        
    if sec_C_range != 0:
        channel = 'A'
        status["setCh{}".format(channel)] = ps.ps5000aSetChannel(chandle,
                                                                PICOSCOPE_CHANNEL_NAMES[channel],
                                                                int(enabled),
                                                                PICOSCOPE_COUPLING_NAMES[coupling],
                                                                PICOSCOPE_RANGE_NAMES[range_string],
                                                                analog_offset)
        assert_pico_ok(status["setCh{}".format(channel)])
        
        channel = 'B'
        status["setCh{}".format(channel)] = ps.ps5000aSetChannel(chandle,
                                                                PICOSCOPE_CHANNEL_NAMES[channel],
                                                                int(enabled),
                                                                PICOSCOPE_COUPLING_NAMES[coupling],
                                                                PICOSCOPE_RANGE_NAMES[sec_C_range],
                                                                analog_offset)
        assert_pico_ok(status["setCh{}".format(channel)])
    
    
    
    
    
    maxADC = ctypes.c_int16()
    status["maximumValue"] = ps.ps5000aMaximumValue(chandle, ctypes.byref(maxADC))

    # Set trigger
    status["trigger"] = ps.ps5000aSetSimpleTrigger(chandle,
                                                   1,
                                                   PICOSCOPE_CHANNEL_NAMES["B"],
                                                   5000,
                                                   PICOSCOPE_TRIGGER_DIRECTIONS["rising"],
                                                   0,
                                                   0)
    assert_pico_ok(status["trigger"])

    
    # Run rapid block capture twice
    n_waveforms = n_pulses
    pre_samples = 1000
    post_samples = 3000
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
    
    status["GetTimebase2"] = ps.ps5000aGetTimebase2(chandle, 
                                                   timebase, 
                                                   total_samples, 
                                                   ctypes.byref(timeIntervalns), 
                                                   ctypes.byref(returnedMaxSamples), 
                                                   0)
    assert_pico_ok(status["GetTimebase2"])
    
    print(timeIntervalns, returnedMaxSamples, oversample)

    status["SetNoOfCaptures"] = ps.ps5000aSetNoOfCaptures(chandle,n_waveforms)
    
    assert_pico_ok(status["SetNoOfCaptures"])

    cMaxSamples = ctypes.c_int32()
    status["memorySegments"] = ps.ps5000aMemorySegments(chandle,
                                                        n_waveforms,
                                                        ctypes.byref(cMaxSamples))
    assert_pico_ok(status["memorySegments"])
    # print("Maximum number of samples:", cMaxSamples)
    oversample = ctypes.c_int16(0)
    pParameter = ctypes.c_bool(False)
    
    status["runBlock"] = ps.ps5000aRunBlock(chandle,
                                            pre_samples,
                                            post_samples,
                                            timebase,
                                            None,
                                            0, # Fails when 10 or above, works for 0-9
                                            None,
                                            None)
    assert_pico_ok(status["runBlock"])

    # Wait
    ready = ctypes.c_int16(0)
    check = ctypes.c_int16(0)
    while ready.value == check.value:
        status["isReady"] = ps.ps5000aIsReady(chandle, ctypes.byref(ready))
    # Check the number of captured scans

    nCaptures = ctypes.c_uint32()
    status["GetNoOfProcessedCaptures"] = ps.ps5000aGetNoOfProcessedCaptures(chandle,ctypes.byref(nCaptures))
    assert_pico_ok(status["GetNoOfProcessedCaptures"])
    print("Number of processed captures:", nCaptures.value)

    # Stop data capture
    status["stop"] = ps.ps5000aStop(chandle)
    assert_pico_ok(status["stop"])

    # Download channel B only
    channel = "A"
    buffer = (ctypes.c_int16 * total_samples)()
    results = np.empty((total_samples, n_waveforms), dtype=np.float32)
    for segment in range(n_waveforms):
        cmaxSamples = ctypes.c_int32(total_samples)
        overflow = ctypes.c_int16()

        status["setDataBuffer{}".format(channel)] = ps.ps5000aSetDataBuffer(chandle,
                                                                            PICOSCOPE_CHANNEL_NAMES[channel],
                                                                            ctypes.byref(buffer),
                                                                            total_samples,
                                                                            segment,
                                                                            0)
        assert_pico_ok(status["setDataBuffer{}".format(channel)])

        status["getValues"] = ps.ps5000aGetValues(chandle,
                                                  0,
                                                  ctypes.byref(cmaxSamples),
                                                  0, # downSampleRatio
                                                  0, # ps.PS5000a_RATIO_MODE['PS5000a_RATIO_MODE_NONE']
                                                  segment,
                                                  ctypes.byref(overflow))
        assert_pico_ok(status["getValues"])
        # Converts ADC from channel A to mV
        maxADC = ctypes.c_int16()
        status["maximumValue"] = ps.ps5000aMaximumValue(chandle, ctypes.byref(maxADC))
        assert_pico_ok(status["maximumValue"])
        adc2mVChAMax =  adc2mV(buffer,  PICOSCOPE_RANGE_NAMES[range_string], maxADC)       

        results[:,segment] = adc2mVChAMax
        
    
        
    # Close unitDisconnect the scope
    # handle = chandle
    
    status["close"] = ps.ps5000aCloseUnit(chandle)
    assert_pico_ok(status["close"])
    
    return results, total_samples
    # Close unitDisconnect the scope
    # handle = chandle
    
    
    

