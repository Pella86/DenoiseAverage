# DenoiseAverage
This program will use the image averaging technique to denoise images. The effect should simulate a long exposure.

## Usage

![Example image](http://i.imgur.com/sDQTsMb.png)

The picture in the upper left panel is a single exposure. The upper right panel is about 580 exposures averaged. In order to avoid that features will be blurred, the algorithm includes an alignment method based on fast fourier transform and cross correlation.

In the picture below are highlighted some details and artifacts of the method:
1. The averaged picture shows a incredible denoising effect
1. The screen of the pc was running a movie. This is why in the average results grey.
1. The clock arms and ticks are almost not visibile in the unprocessed picture. In the averaged picture the quality is better but since the 500 pictures where taken in 5 minutes, the clock minute arm is blurred away.
