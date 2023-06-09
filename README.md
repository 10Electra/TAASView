<a href="https://aimeos.org/">
    <img src="https://github.com/10Electra/TAASView/blob/main/Example%20Photos/logo.png?raw=true" alt="TAASView logo" title="TAASView" align="right" height="60" />
</a>

# TAASView

[TAASView](https://github.com/10Electra/TAASView) is a small app that offers simultaneous control of multiple AlliedVision cameras. The app is geared towards use in a lab context, the cameras enabling monitoring and recording of routines and experiments.

<!-- ![aimeos-frontend](https://user-images.githubusercontent.com/8647429/212348410-55cbaa00-722a-4a30-8b57-da9e173e0675.jpg) -->

<figure>
<img
  src="https://github.com/10Electra/TAASView/blob/main/Example%20Photos/Example_1.png?raw=true"
  style="display: block;
          margin-left: auto;
          margin-right: auto;">
<figcaption align = "center"><b>Example screenshot</b></figcaption>
</figure>

To install TAASView, simply clone this repository into a local directory, or download the repository's .zip file. The file `controller.py` is the main script to run.

Currently, the default exposure values and camera resolutions are hardcoded in `vimba_handler.py` and `runnables.py`. A planned future improvement is to add config file loading and saving functionality.
