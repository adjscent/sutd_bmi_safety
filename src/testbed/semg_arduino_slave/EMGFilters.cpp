#include "EMGFilters.h"


void EMGFilters::init(SAMPLE_FREQUENCY sampleFreq,
                     NOTCH_FREQUENCY  notchFreq,
                     bool             enableNotchFilter,
                     bool             enableLowpassFilter,
                     bool             enableHighpassFilter) {
    m_sampleFreq   = sampleFreq;
    m_notchFreq    = notchFreq;
    m_bypassEnabled = true;
    if (((sampleFreq == SAMPLE_FREQ_500HZ) || (sampleFreq == SAMPLE_FREQ_1000HZ)) &&
        ((notchFreq == NOTCH_FREQ_50HZ) || (notchFreq == NOTCH_FREQ_60HZ))) {
            m_bypassEnabled = false;
    }

    m_LPF.init(FILTER_TYPE_LOWPASS, m_sampleFreq);
    m_HPF.init(FILTER_TYPE_HIGHPASS, m_sampleFreq);
    m_AHF.init(m_sampleFreq, m_notchFreq);

    m_notchFilterEnabled    = enableNotchFilter;
    m_lowpassFilterEnabled  = enableLowpassFilter;
    m_highpassFilterEnabled = enableHighpassFilter;
}

int EMGFilters::update(int inputValue) {
    int output = 0;
    if (m_bypassEnabled) {
        return output = inputValue;
    }

    // first notch filter
    if (m_notchFilterEnabled) {
        // output = NTF.update(inputValue);
        output = m_AHF.update(inputValue);
    } else {
        // notch filter bypass
        output = inputValue;
    }

    // second low pass filter
    if (m_lowpassFilterEnabled) {
        output = m_LPF.update(output);
    }

    // third high pass filter
    if (m_highpassFilterEnabled) {
        output = m_HPF.update(output);
    }

    return output;
}
