# EXTRACT VALID JSON FROM HTML

**Purpose**

This script was designed out of sheer frustration with Tiktok's method of embedding a JSON object
within their HTML in such a way that it is virtually impossible to hard code start and stop characters
for a REGEX approach. Even though REGEX should never be used on HTML, we developers will continuously
attempt the impossible.

Instead, this script makes some general assumptions and then makes a few optimizations to find large valid
JSON objects within milliseconds (this can probably be improved by another order of magnitude but CPU time
has become much cheaper than developer time so this is what we end up with now).

**General approach:**

Find all beginning characters that are used for the start of a JSON object -- "{". Then find all ending
brackets -- "}". Create a list of positions for each one and then brute force checking if all the text

between the two constitute a valid JSON object. There are some configuration variables that can be adjusted
to improve the speed of the script (mainly by reducing the amount of text and tries that are necessary until
a valid JSON object is found.

The entire process starts with finding a known valid key within the JSON object that is always present. For
the case of a Tiktok user, this script uses "friendCount" (case is important). The objective is to use a key
that is rare but always present in a Tiktok user JSON object so that we don't detect that text in other parts
of the HTML. Once the start position of the text is found (friendCount), we look X characters behind that string for starting brackets and then Y characters after the start position of the string. X and Y are two configurable options.

If you set them to be too small, you may not grab all of the JSON object and get a false negative. If they are made too large, it will increase the runtime of the script. Currently the script takes about one millisecond to find a JSON object with X character look behind / ahead. This should be tested over a large number of HTML data to make sure all use cases are covered sufficiently with the default configuration.

**Running**

Running the script is fairly straight-forward. Just close the repository and make sure you pip install the requirements file (mainly make sure you grab ujson -- I usually do:

~~~
 pip3 install ujson
 ~~~

 When the script is run, it grabs the HTML code for one of Tiktok's most popular accounts. Then it will find the user JSON object and output that object to the screen. The total time to find the object and extract it is on the order of a couple of milliseconds.

 **Known issues and limitations**

 Although the script does run quickly, there is further optimization that could probably speed up the script by another magnitude. If you are building an ingest and need to quickly scale out, it would probably be fastest to use multi-processing (not multi-thread!) and run an extraction on each available core. Right now I am getting around 50-100 extractions per second per core. More optimizations could push this up to ~250.

 The bigger limitation right now is that this script assumes that we are trying to fetch only one JSON within a blob of text / html. The next version will give further options to fetch multiple JSON objects per text / html while retaining its flexibility.

 As always, have fun!
