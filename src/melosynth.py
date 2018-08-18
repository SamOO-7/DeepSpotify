import os, wave, logging
import numpy as np
import scipy.io.wavfile
import librosa
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def wavwrite(x, filename, fs=44100, N=16):
    '''
    Synthesize signal x into a wavefile on disk. The values of x must be in the
    range [-1,1].

    :parameters:
    - x : numpy.array
    Signal to synthesize.

    - filename: string
    Path of output wavfile.

    - fs : int
    Sampling frequency, by default 44100.

    - N : int
    Bit depth, by default 16.
    '''
    
    maxVol = 2**15-1.0 # maximum amplitude
    x = x * maxVol # scale x
    
    scipy.io.wavfile.write(filename, fs, np.asarray(x, dtype=np.int16))
    

def melosynth(times, freqs, orig_freqs, outputfolder, outputid, fs, nHarmonics, square, useneg):
    '''
    Load pitch sequence from  a txt/csv file and synthesize it into a .wav

    :parameters:
    - times: np.ndarray
    Array of timestamps (float)

    - freqs: np.ndarray
    Array of corresponding frequency values (float)
    
    - orig_url: str
    URL string of the original song. Used to write to 
    [outputid].melosynth.mix.wav


    - outputfolder: str
    Path to where output csv and wav files should be saved.

    - outputid: str
    [outputid].csv and [outputid].melosynth.wav will be written.

    - fs : int
    Sampling frequency for the synthesized file.

    - nHarmonics : int
    Number of harmonics (including the fundamental) to use in the synthesis
    (default is 1). As the number is increased the wave will become more
    sawtooth-like.

    - square : bool
    When set to true, the waveform will converge to a square wave instead of
    a sawtooth as the number of harmonics is increased.

    - useneg : bool
    By default, negative frequency values (unvoiced frames) are synthesized as
    silence. If useneg is set to True, these frames will be synthesized using
    their absolute values (i.e. as voiced frames).
    '''

    # Preprocess input parameters
    fs = int(float(fs))
    nHarmonics = int(nHarmonics)

    # Load pitch sequence
    logging.info('Loading data...')
    #times, freqs = loadmel(inputfile)

    # Preprocess pitch sequence
    if useneg:
        freqs = np.abs(freqs)
    else:
        freqs[freqs < 0] = 0
    # Impute silence if start time > 0
    if times[0] > 0:
        estimated_hop = np.median(np.diff(times))
        prev_time = max(times[0] - estimated_hop, 0)
        times = np.insert(times, 0, prev_time)
        freqs = np.insert(freqs, 0, 0)


    logging.info('Generating wave...')
    signal = []

    translen = 0.010 # duration (in seconds) for fade in/out and freq interp
    phase = np.zeros(nHarmonics) # start phase for all harmonics
    f_prev = 0 # previous frequency
    t_prev = 0 # previous timestamp
    for t, f in zip(times, freqs):

        # Compute number of samples to synthesize
        nsamples = int(np.round((t - t_prev) * fs))

        if nsamples > 0:
            # calculate transition length (in samples)
            translen_sm = float(min(np.round(translen*fs), nsamples))

            # Generate frequency series
            nsamples
            freq_series = np.ones(nsamples) * f_prev

            # Interpolate between non-zero frequencies
            if f_prev > 0 and f > 0:
                freq_series += np.minimum(np.arange(nsamples)/translen_sm, 1) *\
                               (f - f_prev)
            elif f > 0:
                freq_series = np.ones(nsamples) * f

            # Repeat for each harmonic
            samples = np.zeros(nsamples)
            for h in range(nHarmonics):
                # Determine harmonic num (h+1 for sawtooth, 2h+1 for square)
                hnum = 2*h+1 if square else h+1
                # Compute the phase of each sample
                phasors = 2 * np.pi * (hnum) * freq_series / float(fs)
                phases = phase[h] + np.cumsum(phasors)
                # Compute sample values and add
                samples += np.sin(phases) / (hnum)
                # Update phase
                phase[h] = phases[-1]

            # Fade in/out and silence
            if f_prev == 0 and f > 0:
                samples *= np.minimum(np.arange(nsamples)/translen_sm, 1)
            if f_prev > 0 and f == 0:
                samples *= np.maximum(1 - (np.arange(nsamples)/translen_sm), 0)
            if f_prev == 0 and f == 0:
                samples *= 0

            # Append samples
            signal.extend(samples)

        t_prev = t
        f_prev = f

    # Normalize signal
    signal = np.asarray(signal)
    signal *= 0.8 / float(np.max(signal))

    logging.info('Saving csv file...')
    # music/data/melodia/data
    csv_data = np.array([times, freqs]).T
    csv_f = os.path.join(outputfolder, "data", outputid + ".csv")
    np.savetxt(csv_f, csv_data, delimiter=",")
    
    logging.info('Saving wav file...')
    # music/data/melodia/synths
    wav_f = os.path.join(outputfolder, "synths", outputid + ".melosynth.wav")
    wavwrite(np.asarray(signal), wav_f, fs)
    
    logging.info('Saving mixed wav file...')
    # music/data/melodia/synths
    wav_mix_f = os.path.join(outputfolder, "synths", outputid + ".melosynth.mix.wav")
    
    # cut off last second to keep both arrays same size
    orig, sr = librosa.load(orig_url, sr=44100, mono=True, duration=29, offset=0.05)
    melo, sr = librosa.load(wav_f, sr=44100, mono=True, duration=29)
    orig_and_melo = np.add(orig*0.3, melo*0.7)
    librosa.output.write_wav(wav_mix_f, orig_and_melo, sr)