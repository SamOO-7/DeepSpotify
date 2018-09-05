# DeepSpotify



Congratulations! You have just found DeepSpotify.

Follow my progress on this project on my blog, [alexisafk.com](alexisafk.com).

DeepSpotify learns your favorite Spotify playlists to generate music. It uses [Melodia](https://www.upf.edu/web/mtg/melodia) and [spotipy](https://github.com/plamere/spotipy)/[Spotify Web API](https://developer.spotify.com/web-api/) to extract a melody from your favorite Spotify playlist, [Keras](https://keras.io/) to learn the grammars of these melodies with a two layer [LSTM](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) [RNN](https://karpathy.github.io/2015/05/21/rnn-effectiveness/), and generates a new melody that should sound like the other songs in that playlist.

## Dependencies

### The Easy Way

Make sure to have Anaconda and Melodia installed. See further down how to install Melodia.

Then create an Anaconda environment from the `DeepSpotify.yaml` in the project root directory by running:

```bash
$ conda env create -f DeepSpotify.yml
$ source activate DeepSpotify
```

This will create an environment called DeepSpotify and install the necessary libraries that you need to run DeepSpotify.

P.S. Detailed instructions on how to install Melodia 1.0 are [here](https://www.upf.edu/web/mtg/melodia).

### The Hard Way

Manually install all these dependencies in Python 3.6 environment:

* [tensorflow](https://www.tensorflow.org/install/)=1.10.0
* [Keras](https://keras.io/)==2.2.2
* [spotipy](https://github.com/plamere/spotipy)==2.4.4
* [Melodia](https://www.upf.edu/web/mtg/melodia)==1.0
* [vamp](https://pypi.org/project/vamp/)==1.1.0
* [librosa](https://github.com/librosa/librosa)==0.6.2
* [music21](http://web.mit.edu/music21/)==5.3.0
* [MIDIUtil](https://pypi.org/project/MIDIUtil/)==1.2.1
* [matplotlib](https://github.com/matplotlib/matplotlib)==2.2.3

## Getting Started

`main.py` is run by passing two parameters:

```bash
$ python src/main.py -h
Using TensorFlow backend.
usage: main.py [-h] run_opt uri

positional arguments:
  run_opt     An integer: 1 to analyze audio, 2 to train, 3 to generate, 4 to
              do everything.
  uri         A string: spotify playlist uri

optional arguments:
  -h, --help  show this help message and exit
  
```

The `run_opt` is used to run different parts of the program. Keep in mind that (1) analyzing audio is required before (2) you can train the model which is required before (3) you can generate new songs. Use (4) to run everything all at once. This will take quite some time to run.

The `uri` is the Spotify playlist URI. This should in a format like this `spotify:user:alezabeth1997:playlist:1LMwOJtfhsnN2FGf0yizXl` (an example of my personal Snarky Puppy playlist).

## Quality Control

Because all music is not equal, the quality of the generated songs may differ greatly. This is probably attributed to how Melodia can extract the melodic frequencies better from some songs than for other songs (i.e., cleaner melody in a jazz piece than an Eminem rap). 

## Future Work

Feel free to fork this project! I'll be making improvements to this project (i.e., considering using raw melodies instead of midi files because midi doesn't seem to capture melody accurately, feeding in model data differently, etc.).

Follow my progress on my blog, [alexisafk.com](alexisafk.com).