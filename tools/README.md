# Koalafinder Tools

> The following tools only runs for Windows OS. To run on Linux, a virtual layer such as a VM or Wine is needed.

## Extract_all.sh

`extract_all.sh` is a command-line script to convert a video file into a directory of images that can be labelled individually using a tool such as DarkLabel. 

```bash
# extract the entire video length
extract_all.sh [video_path]
# or extract a snippet
extract_all.sh [video_path] [start_time] [end_time]
```

To use `extract_all.sh`, the following command is an example:

```bash
extract_all.sh DJI_0036.MP4
extract_all.sh DJI_0026.MP4 00:03:00 00:06:18
```


## DarkLabel

Darklabel is a tool developed by [darkpgmr@Github](https://github.com/darkpgmr) and the latest version is on the following repository [DarkLabel](https://github.com/darkpgmr/DarkLabel).

To use DarkLabel:

1. Load image folder

2. Load GT folder

3. Create bbox using Left-Click

4. Press Enter to predict the next bbox

5. Shift + Right-Click to delete bbox labels

*Important notes to consider when labelling*

1. **The AI quality is directly determined by the data quality**: Bad teacher results in a bad learner. Make the most in effort to produce high-quality data labels

2. **Do not abuse the predict tool**: It can save a lot of time but be sure to 'reset' the label manually after a number of frames so inaccuracies do not compound the prediction

3. **Label any obscured koala**: Unless it is completely invisible, label what part of the koala is still visible. This temporal knowledge will be considered in the model


