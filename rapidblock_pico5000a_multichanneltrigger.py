import numpy as np
import ctypes
from picosdk.ps5000a import ps5000a as ps
from picosdk.functions import adc2mV, assert_pico_ok,mV2adc
import time



def getData(usr_range,n_pulses,timebase ,bit,TrLevel):
    PICOSCOPE_CHANNEL_NAMES = {"A" : 0, "B" : 1, "C" : 2, "D" : 3,"EXT":4}
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

    TIMEBASE = {
        "1 ns": 0,
        "2 ns": 1,
        "4 ns": 2,
        "8 ns": 3,
        "16 ns": 4
        }
    trig_lev = TrLevel


# Defining a Python class to represent the structure


    # Connect to unit
    chandle = ctypes.c_int16()
    status = {}

    
    
    
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
    
    status["resolution"] = ps.ps5000aSetDeviceResolution(chandle,DEVICE_RESOLUTION[bit])
    assert_pico_ok(status["resolution"])

    # Configure channels A 

    
    coupling = 'DC'
    analog_offset = PICOSCOPE_RANGE_VOLTAGE[usr_range]*(0)
    #if you use resolution 16-bit you have to use only one channel - others you have to disabled !!! number of channels depends on power source !!!
    
    enabled = True
    disabled = False
   
    channel = 'A'
    status["setCh{}".format(channel)] = ps.ps5000aSetChannel(chandle,
                                                                PICOSCOPE_CHANNEL_NAMES[channel],
                                                                int(enabled),
                                                                PICOSCOPE_COUPLING_NAMES[coupling],
                                                                PICOSCOPE_RANGE_NAMES[usr_range],
                                                                analog_offset)
    assert_pico_ok(status["setCh{}".format(channel)])
        
    channel = 'B'
    status["setCh{}".format(channel)] = ps.ps5000aSetChannel(chandle,
                                                                PICOSCOPE_CHANNEL_NAMES[channel],
                                                                int(enabled),
                                                                PICOSCOPE_COUPLING_NAMES[coupling],
                                                                PICOSCOPE_RANGE_NAMES[usr_range],
                                                                analog_offset)
    assert_pico_ok(status["setCh{}".format(channel)])
    
    channel = 'C'
    status["setCh{}".format(channel)] = ps.ps5000aSetChannel(chandle,
                                                                PICOSCOPE_CHANNEL_NAMES[channel],
                                                               int(enabled),
                                                                PICOSCOPE_COUPLING_NAMES[coupling],
                                                                PICOSCOPE_RANGE_NAMES[usr_range],
                                                                analog_offset)
    assert_pico_ok(status["setCh{}".format(channel)])
    
    
    channel = 'D'
    status["setCh{}".format(channel)] = ps.ps5000aSetChannel(chandle,
                                                                PICOSCOPE_CHANNEL_NAMES[channel],
                                                               int(enabled),
                                                                PICOSCOPE_COUPLING_NAMES[coupling],
                                                                PICOSCOPE_RANGE_NAMES[usr_range],
                                                                analog_offset)
    assert_pico_ok(status["setCh{}".format(channel)])
    
    
    
    maxADC = ctypes.c_int16()
    status["maximumValue"] = ps.ps5000aMaximumValue(chandle, ctypes.byref(maxADC))

    # Set trigger
    adcTriggerLevelA = mV2adc(trig_lev, PICOSCOPE_RANGE_NAMES[usr_range], maxADC)
    adcTriggerLevelB = mV2adc(trig_lev, PICOSCOPE_RANGE_NAMES[usr_range], maxADC)
    adcTriggerLevelC = mV2adc(trig_lev, PICOSCOPE_RANGE_NAMES[usr_range], maxADC)
    adcTriggerLevelD = mV2adc(trig_lev, PICOSCOPE_RANGE_NAMES[usr_range], maxADC)

    triggerProperties = (ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2 * 4)()
    triggerProperties[0] = ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2(adcTriggerLevelA,
                                                                10,
                                                                0,
                                                                10,
                                                                ps.PS5000A_CHANNEL["PS5000A_CHANNEL_A"])
                                                                
    triggerProperties[1] = ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2(adcTriggerLevelB,
                                                                10,
                                                                0,
                                                                10,
                                                                ps.PS5000A_CHANNEL["PS5000A_CHANNEL_B"])
                                                                
    triggerProperties[2] = ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2(adcTriggerLevelC,
                                                                10,
                                                                0,
                                                                10,
                                                                ps.PS5000A_CHANNEL["PS5000A_CHANNEL_C"])
                                                                
    triggerProperties[3] = ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2(adcTriggerLevelD,
                                                                10,
                                                                0,
                                                                10,
                                                                ps.PS5000A_CHANNEL["PS5000A_CHANNEL_D"])
                                                            
                                                                
    status["setTriggerChannelPropertiesV2"] = ps.ps5000aSetTriggerChannelPropertiesV2(chandle, ctypes.byref(triggerProperties), 4, 0)

    triggerConditionsA = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_A"],
                                                            ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
    triggerConditionsB = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_B"],
                                                            ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
    triggerConditionsC = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_C"],
                                                            ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
    triggerConditionsD = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_D"],
                                                            ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
    clear = 1
    add = 2
                                                            
    status["setTriggerChannelConditionsV2_A"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(triggerConditionsA), 1, (clear + add))
    status["setTriggerChannelConditionsV2_B"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(triggerConditionsB), 1, (add))
    status["setTriggerChannelConditionsV2_C"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(triggerConditionsC), 1, (add))
    status["setTriggerChannelConditionsV2_D"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(triggerConditionsD), 1, (add))

    triggerDirections = (ps.PS5000A_DIRECTION * 4)()
    triggerDirections[0] = ps.PS5000A_DIRECTION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_A"], 
                                                                ps.PS5000A_THRESHOLD_DIRECTION["PS5000A_RISING"], 
                                                                ps.PS5000A_THRESHOLD_MODE["PS5000A_LEVEL"])
    triggerDirections[1] = ps.PS5000A_DIRECTION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_B"], 
                                                                ps.PS5000A_THRESHOLD_DIRECTION["PS5000A_RISING"], 
                                                                ps.PS5000A_THRESHOLD_MODE["PS5000A_LEVEL"])
    triggerDirections[2] = ps.PS5000A_DIRECTION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_C"], 
                                                                ps.PS5000A_THRESHOLD_DIRECTION["PS5000A_RISING"], 
                                                                ps.PS5000A_THRESHOLD_MODE["PS5000A_LEVEL"])
    triggerDirections[3] = ps.PS5000A_DIRECTION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_D"], 
                                                                ps.PS5000A_THRESHOLD_DIRECTION["PS5000A_RISING"], 
                                                                ps.PS5000A_THRESHOLD_MODE["PS5000A_LEVEL"])
    status["setTriggerChannelDirections"] = ps.ps5000aSetTriggerChannelDirectionsV2(chandle, ctypes.byref(triggerDirections), 4)



    
    # Run rapid block capture twice
    n_waveforms = n_pulses
    pre_samples = 1000
    post_samples = 4000
    total_samples = pre_samples + post_samples
    cmaxSamples = ctypes.c_int32(total_samples)
    
    # Get timebase information
    # handle = chandle
    # timebase = 8 = timebase
    # noSamples = totalSamples
    # pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalNs)
    # pointer to totalSamples = ctypes.byref(returnedMaxSamples)
    # segment index = 0
   
    timeIntervalns = ctypes.c_float()
    returnedMaxSamples = ctypes.c_int32()
    oversample = ctypes.c_int16(0)
    
    status["GetTimebase2"] = ps.ps5000aGetTimebase2(chandle, 
                                                   TIMEBASE[timebase], 
                                                   total_samples, 
                                                   ctypes.byref(timeIntervalns), 
                                                   ctypes.byref(returnedMaxSamples), 
                                                   0)
    assert_pico_ok(status["GetTimebase2"])
    
    #print(timeIntervalns, returnedMaxSamples, oversample)
    status["MemorySegments"] = ps.ps5000aMemorySegments(chandle, n_waveforms, ctypes.byref(cmaxSamples))
    assert_pico_ok(status["MemorySegments"])

    status["SetNoOfCaptures"] = ps.ps5000aSetNoOfCaptures(chandle,n_waveforms)
    
    assert_pico_ok(status["SetNoOfCaptures"])

    
    # print("Maximum number of samples:", cMaxSamples)
  
    status["runBlock"] = ps.ps5000aRunBlock(chandle,
                                            pre_samples,
                                            post_samples,
                                            TIMEBASE[timebase],
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

    # Create buffers ready for assigning pointers for data collection
    bufferAMax = (ctypes.c_int16 * total_samples)()
    bufferAMin = (ctypes.c_int16 * total_samples)()

  
    bufferBMax = (ctypes.c_int16 * total_samples)()
    bufferBMin = (ctypes.c_int16 * total_samples)()
  
    bufferCMax = (ctypes.c_int16 * total_samples)()
    bufferCMin = (ctypes.c_int16 * total_samples)()
    bufferDMax = (ctypes.c_int16 * total_samples)()
    bufferDMin = (ctypes.c_int16 * total_samples)()
  

    

    overflow = ctypes.c_int16()

    cMaxSamples = ctypes.c_int32(total_samples)
      


# convert ADC counts data to mV


    
    resultsA = np.empty((total_samples, n_waveforms), dtype=np.float32)
    resultsB = np.empty((total_samples, n_waveforms), dtype=np.float32)
    resultsC = np.empty((total_samples, n_waveforms), dtype=np.float32)
    resultsD = np.empty((total_samples, n_waveforms), dtype=np.float32)
    for segment in range(n_waveforms):
        
        overflow = ctypes.c_int16()
        
        channel = "A"
        status["setDataBuffersA"] = ps.ps5000aSetDataBuffers(chandle, PICOSCOPE_CHANNEL_NAMES[channel], ctypes.byref(bufferAMax), ctypes.byref(bufferAMin),total_samples, segment, 0)
        assert_pico_ok(status["setDataBuffersA"])
        
        channel = "B"
        status["setDataBuffersB"] = ps.ps5000aSetDataBuffers(chandle, PICOSCOPE_CHANNEL_NAMES[channel], ctypes.byref(bufferBMax), ctypes.byref(bufferBMin), total_samples, segment, 0)
        assert_pico_ok(status["setDataBuffersB"])
    
        channel = "C"
        status["setDataBuffersC"] = ps.ps5000aSetDataBuffers(chandle, PICOSCOPE_CHANNEL_NAMES[channel], ctypes.byref(bufferCMax), ctypes.byref(bufferCMin), total_samples, segment, 0)
        assert_pico_ok(status["setDataBuffersC"])
      
        channel = "D"
        status["setDataBuffersD"] = ps.ps5000aSetDataBuffers(chandle, PICOSCOPE_CHANNEL_NAMES[channel], ctypes.byref(bufferDMax), ctypes.byref(bufferDMin), total_samples, segment, 0)
        assert_pico_ok(status["setDataBuffersD"])

        status["getValues"] = ps.ps5000aGetValues(chandle,
                                                  0,
                                                  ctypes.byref(cmaxSamples),
                                                  0, # downSampleRatio
                                                  0, # ps.PS5000a_RATIO_MODE['PS5000a_RATIO_MODE_NONE']
                                                  segment,
                                                  ctypes.byref(overflow))
        assert_pico_ok(status["getValues"])
        
        
        adc2mVChAMax =  adc2mV(bufferAMax,  PICOSCOPE_RANGE_NAMES[usr_range], maxADC)
        adc2mVChCMax =  adc2mV(bufferCMax,  PICOSCOPE_RANGE_NAMES[usr_range], maxADC)
        adc2mVChBMax =  adc2mV(bufferBMax,  PICOSCOPE_RANGE_NAMES[usr_range], maxADC)
        adc2mVChDMax =  adc2mV(bufferDMax,  PICOSCOPE_RANGE_NAMES[usr_range], maxADC)


        resultsA[:,segment] = adc2mVChAMax
        resultsB[:,segment] = adc2mVChBMax
        resultsC[:,segment] = adc2mVChCMax
        resultsD[:,segment] = adc2mVChDMax
        
    
    # Close unitDisconnect the scope
    # handle = chandle
    
    status["close"] = ps.ps5000aCloseUnit(chandle)
    assert_pico_ok(status["close"])
    
    return   resultsA,resultsB,resultsC,resultsD,total_samples
    # Close unitDisconnect the scope
    # handle = chandle
    
    
    

