# my-o-FirstAirGuitar

## Initialization
### Requirements
* Myo Connect and SDK ([Windows / Mac](https://developer.thalmic.com/downloads)) - you will have to sign up for a Myo Developer Account (just takes email)
* Python 2.7.9 (pre-installed on Macs, on Windows go [here](https://www.python.org/downloads/release/python-279/))
* Git
Unfortunately, Myo Connect and the Myo SDK don't come packaged for Linux distros at this time, so you're stuck with either Mac or Windows.

## Setup Procedure

### Myo
***
Download Myo Connect and the Myo SDK (from Requirements)

Set up your Myo typically - you can follow the linked instructions ([Windows](https://support.getmyo.com/hc/en-us/articles/202657596-Getting-starting-with-Myo-on-Windows) / [Mac](https://support.getmyo.com/hc/en-us/articles/202667496-Getting-starting-with-Myo-on-Mac-OS-X)), but in most cases, it's as easy as running Myo Connect and following the prompts.

Make sure you're putting the Myo on with the connector port facing your wrist and the Myo symbol plate on top of your forearm (last part is not required by Myo, but helpful for us if we want to have similar channels showing similar data). You should be able to perform all 5 officially supoorted gestures and have them recognized by Myo Connect - it's not super relevant to the project, but it ensures that you have the Myo on properly and that EMG connectivity works. You might want to set up a custom calibration profile. 

Add the path of the framework file from the Myo SDK (e.g. "/Users/[user_name]/Downloads/sdk/myo.framework") to the required system variable (PATH on Windows, DYLD_LIBRARY_PATH - full instructions [here](http://developerblog.myo.com/myo-unleashed-python/)).

### Git
***
If you don't have [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) or [GitHub Desktop](https://desktop.github.com/) installed, install either one now. [Clone](https://help.github.com/articles/cloning-a-repository/) this repository to somewhere where you won't randomly delete it.

### FirstAirGuitar
***
Open up a terminal window, navigate to the directory that you've cloned this repository into, and enter

```pip install -r requirements.txt``` 

(you can also do this in a virtual environment, if you have that [set up](http://docs.python-guide.org/en/latest/dev/virtualenvs/), but otherwise you don't need to bother). The install may take a while because of scipy's ridiculously long list of compiled dependencies.

You should now be able to run anything in the repository, but let me know if you can't. This documentation is still a work in progress.

## Use
***
Right now, my work-flow is as follows:
1. I run a listener script to gather data, following the prompts as they show up in the terminal window:
```python gesture_classifier_5.py```
The data gets stored to a pkl file in a directory called "data" in the same folder. 
2. I pre-process the data, as the arrays of EMG channel data aren't properly shaped when stored. 
```python preprocessing.py [hyphenated-date-time]_myo_data.pkl```
3. I import the gesture classifier neural network model I've made for the scenario, and check the accuracy of classification on the.
```python gesture_classifier_5.py data/[hyphenated-date-time]_myo_data.pkl.proc```

Obviously, this isn't optimal, but I've mostly just been using Jupyter Notebook to visualize the data and check accuracy. I can also start tracking my Notebook file if you think that would be of use to you. Otherwise, improvements that I think could be done are currently being tracked in issues.