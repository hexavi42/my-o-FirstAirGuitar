# my-o-FirstAirGuitar

## Initialization
### Requirements
* Myo Connect and SDK ([Windows / Mac](https://developer.thalmic.com/downloads)) - you will have to sign up for a Myo Developer Account (just takes email)
* Python 2.7.9 (pre-installed on Macs, on Windows go [here](https://www.python.org/downloads/release/python-279/))
Unfortunately, Myo Connect and the Myo SDK don't come packaged for Linux distros at this time, so you're stuck with either Mac or Windows.

## Setup Procedure

Set up your Myo typically ([Windows](https://support.getmyo.com/hc/en-us/articles/202657596-Getting-starting-with-Myo-on-Windows) / [Mac](https://support.getmyo.com/hc/en-us/articles/202667496-Getting-starting-with-Myo-on-Mac-OS-X)) - make sure you're putting the Myo on with the connector port facing your wrist and the Myo symbol plate on top of your forearm (last part is not required by Myo, but helpful for us if we want to have similar channels showing similar data).

Open up a terminal window, navigate to the directory that you've cloned this repository into, and enter 
"pip install -r requirements.txt" 
(you can also do this in a virtual environment, if you have that [set up](http://docs.python-guide.org/en/latest/dev/virtualenvs/), but otherwise you don't need to bother). The install may take a while because of scipy's ridiculously long list of compiled dependencies.

Add the path of the framework file from the Myo SDK (e.g. "/Users/[user_name]/Downloads/sdk/myo.framework") to the required system variable (PATH on Windows, DYLD_LIBRARY_PATH - full instructions [here](http://developerblog.myo.com/myo-unleashed-python/)).

You should now be able to run anything in the repository, but let me know if you can't. This documentation is still a work in progress. 