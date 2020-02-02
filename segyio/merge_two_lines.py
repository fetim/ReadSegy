import segyio
import matplotlib.pyplot as pl
import numpy as np
import segyio_tools

folder = "../segy/set2_Lines2D_inlines/"
filename1="line12"
with segyio.open(folder+filename1+".sgy",ignore_geometry=True) as f:
    print('f.tracecount=',f.tracecount)
    seismicA    = f.trace.raw[:]
    textheader  = f.text[0]
    bin_headers = f.bin   
    # get trace headers values
    ilA         = f.attributes(segyio.TraceField.INLINE_3D)[:]
    xlA         = f.attributes(segyio.TraceField.CROSSLINE_3D)[:]
    cdpxA       = f.attributes(segyio.TraceField.CDP_X)[:]
    cdpyA       = f.attributes(segyio.TraceField.CDP_Y)[:]


filename2="line13"
with segyio.open(folder+filename2+".sgy",ignore_geometry=True) as f:
    print('f.tracecount=',f.tracecount)
    seismicB    = f.trace.raw[:]
    # get trace headers values
    ilB         = f.attributes(segyio.TraceField.INLINE_3D)[:]
    xlB         = f.attributes(segyio.TraceField.CROSSLINE_3D)[:]
    cdpxB       = f.attributes(segyio.TraceField.CDP_X)[:]
    cdpyB       = f.attributes(segyio.TraceField.CDP_Y)[:]

seismic_merge   = np.concatenate((seismicA,seismicB),axis=0)
il_merge        = np.concatenate((ilA     ,ilB)     ,axis=0)
xl_merge        = np.concatenate((xlA     ,xlB)     ,axis=0)
cdpx_merge      = np.concatenate((cdpxA   ,cdpxB)   ,axis=0)
cdpy_merge      = np.concatenate((cdpyA   ,cdpyB)   ,axis=0)

n_samples       = seismic_merge.shape[1]
n_traces        = seismic_merge.shape[0]
sample_rate     = 4 # ms

filenameout     = "merge_"+filename1+"-"+filename2

# Create a segy from a 2D matrix
segyio.tools.from_array2D(folder+filenameout+".sgy",seismic_merge)

# read empty segy
SEGY            = segyio.open(folder+filenameout+".sgy",'r+',ignore_geometry=True)

SEGY = segyio_tools.updateSEGYbinaryheader(SEGY)


tracl = np.arange(1,SEGY.bin[segyio.BinField.Traces]+1)

# Trace Header according ANP
# * Highly recommended information, recommended by SEG-Y standard
# @ Mandatory

# set trace headers values
for idx, key in enumerate(SEGY.header):
    key.update({segyio.TraceField.TRACE_SEQUENCE_LINE            : tracl[idx]        }) #1-4@ Trace sequence number within line (will increase if line continues on another reel) 
  # key.update({segyio.TraceField.TRACE_SEQUENCE_FILE            :                   }) #5-8* Trace sequence number within reel
  # key.update({segyio.TraceField.FieldRecord                    :                   }) #9-12*    Original field record number
  # key.update({segyio.TraceField.TraceNumber                    :                   }) #13-16*   Trace number within original field record. It should be the field channel numbe
  # key.update({segyio.TraceField.EnergySourcePoint              :                   }) #17-20@   Energy source point number (Integer)
    key.update({segyio.TraceField.CDP                      : SEGY.attributes(25)[idx]}) #21-24@   CMP number
  # key.update({segyio.TraceField.CDP_TRACE                      :                   }) #25-28    Trace number within the CDP ensemble (each ensemble starts with trace number one)
    key.update({segyio.TraceField.TraceIdentificationCode        : 1                 }) #29-30*   Trace identification code: 
#                                                                                                 1= Seismic data 
#                                                                                                 2= Dead
#                                                                                                 3= Dummy
#                                                                                                 4= Time break 
#                                                                                                 5= Uphole 
#                                                                                                 6= Sweep
#                                                                                                 7= Timing 
#                                                                                                 8= Water break 
#                                                                                                 9 ... N= optional use (N=32767)
  # key.update({segyio.TraceField.NSummedTraces                  :                   })   #31-32    Number of vertically summed traces yielding this one
  # key.update({segyio.TraceField.NStackedTraces                 :                   })   #33-34@   Number of horizontally stacked traces yielding this one 
  # key.update({segyio.TraceField.DataUse                        :                   })   #35-36    Data use: Production=1 Test=2
  # key.update({segyio.TraceField.offset                         :                   })   #37-40@   Distance from source point to receiver group  
  # key.update({segyio.TraceField.ReceiverGroupElevation         :                   })   #41-44@   Receiver group elevation
  # key.update({segyio.TraceField.SourceSurfaceElevation         :                   })   #45-48@   Surface elevation at source 
  # key.update({segyio.TraceField.SourceDepth                    :                   })   #49-52@   Source depth below surface (positive)
  # key.update({segyio.TraceField.ReceiverDatumElevation         :                   })   #53-56@   Datum elevation at receiver group    
  # key.update({segyio.TraceField.SourceDatumElevation           :                   })   #57-60@   Datum elevation at source
  # key.update({segyio.TraceField.SourceWaterDepth               :                   })   #61-64@   Water depth at source.
  # key.update({segyio.TraceField.GroupWaterDepth                :                   })   #65-68@   Water depth at group.
  # key.update({segyio.TraceField.ElevationScalar                :                   })   #69-70@   Scaler to be applied to all elevations and depths specified
#                                                                                                   This field is also influences in bytes 41-68 to give the real value. Scalar = + 1, + 10, + 100, + 1000 or + 10000.
#                                                                                                   If positive, scaler is used as a multiplier; if negative, scaler is used as a divisor
#                                                                                                   This field is also influences information from bytes 189 to 192 (Elevation for CMP).
    key.update({segyio.TraceField.SourceGroupScalar              : 100               })   #71-72@   Scaler to be applied to all coordinates specified in bytes 73-88 to give real value.
#                                                                                                   Scaler = + 1, + 10, + 100, + 1000 or + 10000.  If positive,scaler is used as a multiplier; if negative, 
#                                                                                                   scaler is used as a divisor
#                                                                                                   This field is also influences information from bytes 181 a 188 (X/Y coordinate for mid point).
  # key.update({segyio.TraceField.SourceX                        :                  })   #73-76@   Source coordinate X.
  # key.update({segyio.TraceField.SourceY                        :                  })   #77-80@   Source coordinate Y.
  # key.update({segyio.TraceField.GroupX                         :                  })   #81-84@   Group coordinate X. 
  # key.update({segyio.TraceField.GroupY                         :                  })   #85-88@   Group coordinate Y.
  # key.update({segyio.TraceField.CoordinateUnits                :                  })   #89-90@   Coordinate units. 1= length (meters or feet) 2= seconds of arc
  # key.update({segyio.TraceField.WeatheringVelocity             :                  })   #91-92    Weathering velocity. 
  # key.update({segyio.TraceField.SubWeatheringVelocity          :                  })   #93-94    Subweathering velocity. 
  # key.update({segyio.TraceField.SourceUpholeTime               :                  })   #95-96@   Uphole time at source.
  # key.update({segyio.TraceField.GroupUpholeTime                :                  })   #97-98@   Uphole time at receiver group.
  # key.update({segyio.TraceField.SourceStaticCorrection         :                  })   #99-100@  Source static correction.
  # key.update({segyio.TraceField.GroupStaticCorrection          :                  })   #101-102@ Group static correction.
  # key.update({segyio.TraceField.TotalStaticApplied             :                  })   #103-104@ Total static applied
  # key.update({segyio.TraceField.LagTimeA                       :                  })   #105-106  Lag time A.
  # key.update({segyio.TraceField.LagTimeB                       :                  })   #107-108  Lag time B
  # key.update({segyio.TraceField.DelayRecordingTime             :                  })   #109-110@ Delay recording time.
  # key.update({segyio.TraceField.MuteTimeStart                  :                  })   #111-112  Mute time start. 
  # key.update({segyio.TraceField.MuteTimeEND                    :                  })   #113-114  Mute time end. 
  # key.update({segyio.TraceField.TRACE_SAMPLE_COUNT             :                  })   #115-116@ Number of samples in this trace 
  # key.update({segyio.TraceField.TRACE_SAMPLE_INTERVAL          :                  })   #117-118@ Sample interval in microseconds for this trace 
    key.update({segyio.TraceField.GainType                       : 1                })   #119-120  Gain type of field instruments: 
#                                                                                                  1=fixed;
#                                                                                                  2=binary;
#                                                                                                  3=floating pont;
#                                                                                                  4 ... N=optional use.
  # key.update({segyio.TraceField.InstrumentGainConstant         :                 })   #121-122  Instrument gain constant 
  # key.update({segyio.TraceField.InstrumentInitialGain          :                 })   #123-124  Instrument early or initial gain (dB). 
  # key.update({segyio.TraceField.Correlated                     :                 })   #125-126  Correlated: 1 = no; 2 = yes.
  # key.update({segyio.TraceField.SweepFrequencyStart            :                 })   #127-128  Sweep frequency at start. 
  # key.update({segyio.TraceField.SweepFrequencyEnd              :                 })   #129-130  Sweep frequency at end.
  # key.update({segyio.TraceField.SweepLength                    :                 })   #131-132  Sweep length in ms.
  # key.update({segyio.TraceField.SweepType                      :                 })   #133-134  Sweep type: 
#                                                                                                  1=linear;
#                                                                                                  2=parabolic;
#                                                                                                  3=exponential;
#                                                                                                  4=other.
  # key.update({segyio.TraceField.SweepTraceTaperLengthStart     :                 })   #135-136  Sweep trace taper length atstart in ms. 
  # key.update({segyio.TraceField.SweepTraceTaperLengthEnd       :                 })   #137-138  Sweep trace taper length at end in ms. 
  # key.update({segyio.TraceField.TaperType                      :                 })   #139-140  Taper type: 1=linear; 2=cos2; 3=other.
  # key.update({segyio.TraceField.AliasFilterFrequency           :                 })   #141-142@ Alias filter frequency, if used.
  # key.update({segyio.TraceField.AliasFilterSlope               :                 })   #143-144@ Alias filter slope
  # key.update({segyio.TraceField.NotchFilterFrequency           :                 })   #145-146@ Notch filter frequency, if used
  # key.update({segyio.TraceField.NotchFilterSlope               :                 })   #147-148@ Notch filter slope
  # key.update({segyio.TraceField.LowCutFrequency                :                 })   #149-150@ Low cut frequency if used.
  # key.update({segyio.TraceField.HighCutFrequency               :                 })   #151-152@ High cut frequency if used
  # key.update({segyio.TraceField.LowCutSlope                    :                 })   #153-154@ Low cut slope.
  # key.update({segyio.TraceField.HighCutSlope                   :                 })   #155-156@ High cut slope
  # key.update({segyio.TraceField.YearDataRecorded               :                 })   #157-158@ Year data recorded.
  # key.update({segyio.TraceField.DayOfYear                      :                 })   #159-160@ Day of year.
  # key.update({segyio.TraceField.HourOfDay                      :                 })   #161-162@ Hour of day (24 hour clock) 
  # key.update({segyio.TraceField.MinuteOfHour                   :                 })   #163-164@ Minute of hour.
  # key.update({segyio.TraceField.SecondOfMinute                 :                 })   #165-166@ Second of minute.
    key.update({segyio.TraceField.TimeBaseCode                   :1                })   #167-168@ Time basis code: 1=local; 2=GMT; 3=other.
  # key.update({segyio.TraceField.TraceWeightingFactor           :                 })   #169-170  Trace weighting factor - defined as 2 -N volts for the least significant bit (N=0,1,...,32767).
  # key.update({segyio.TraceField.GeophoneGroupNumberRoll1       :                 })   #171-172  Geophone group number of roll switch position one. 
  # key.update({segyio.TraceField.GeophoneGroupNumberFirstTraceOrigField :         })   #173-174  Geophone group number of trace one witihin original field record.
  # key.update({segyio.TraceField.GeophoneGroupNumberLastTraceOrigField  :         })   #175-176  Geophone group number of last trace within original field record.
  # key.update({segyio.TraceField.GapSize                        :                 })   #177-178  Gap size (total number of traces dropped). 
  # key.update({segyio.TraceField.OverTravel                     :                 })   #179-180  Overtravel associated with taper at beginning or end of line: 1 = down (or behind); 2 = up (or ahead).
    key.update({segyio.TraceField.CDP_X                          : cdpx_merge[idx] })   #181-184@ X coordinate for CMP. [I4]
    key.update({segyio.TraceField.CDP_Y                          : cdpy_merge[idx] })   #185-188@ Y coordinate for CMP. [I4]
    key.update({segyio.TraceField.INLINE_3D                      : il_merge[idx]   })   #189-192@ Elevation for CMP. [I4] | INLINE_3D
    key.update({segyio.TraceField.CROSSLINE_3D                   : xl_merge[idx]   })   #193-196@ CDF Datum | CROSSLINE_3D
    # key.update({segyio.TraceField.ShotPoint                      :                 })   #197-200@ Energy Source Point Number (R4)
    # key.update({segyio.TraceField.ShotPointScalar                :                 })   #201-204@ First break time in ms. [I4] 
    # key.update({segyio.TraceField.TransductionConstantMantissa   :                 })   #205-208@ Receiver station number. [I4]
    # key.update({segyio.TraceField.TransductionConstantPower      :                 })   #209-212@ Source station number. [I4]
    # key.update({segyio.TraceField.TraceIdentifier                :                 })   #213-216@ Receiver line number. [I4]
    # key.update({segyio.TraceField.SourceType                     :                 })   #217-220@ Source line number. [I4] 
    # key.update({221                                              : il_merge[idx]   })   #221-224@ Inline number for trace [I4]
    # key.update({segyio.TraceField.SourceMeasurementMantissa      : xl_merge[idx]   })   #225-228@ Crossline number for trace [I4]
  # key.update({segyio.TraceField.SourceMeasurementExponent      :                 })   #229-230 Unassigned, for optional use.
  # key.update({segyio.TraceField.SourceMeasurementUnit          :                 })   #231-232 Unassigned, for optional use.
  # key.update({segyio.TraceField.UnassignedInt1                 :                 })   #233-236 Unassigned, for optional use.
  # key.update({segyio.TraceField.UnassignedInt2                 :                 })   #237-240 Unassigned, for optional use.
    

# SEGY.close()