ShotClock
=========

Organize photos and videos by date &amp; time taken.


Functionality
-------------

*   Rename jpg and avi files by timestamp.
*   Offset jpg and avi timestamps by any time interval.


Basic Usage
-----------

*   `$ python shotclock.py rename [options] path`  
*   `$ python shotclock.py timeshift [options] path`  

### Examples

#### Adjust all AVIs and JPG metadata timestamps by -4 hours:
`$ python shotclock.py timeshift --hours -4 *.jpg *.avi`

#### Rename all JPGs by metadata timestamp:
`$ python shotclock rename *.jpg`

### Output

Output is always sent to an `./output/` sub-directory.  Original files are not modified.


Use Cases
---------

*   Want your photos and videos to be listed in chronological order when shown in a directory?  Rename them by timestamp.
*   Went on holidays but forgot to update your camera to local time? Look for sunrise/sunset/clocks in your photos to figure out the time offset.  Then apply the offset to all photos.
*   Have multiple cameras taking pictures of the same event (wedding, party etc...).  Find common photos of the same moment to determine the delta between each camera. Then apply the offset to all photos.


Limitations
-----------
Only tested on Canon A710 and Canon A590 (but likely to work for most digital cameras).


Requirements
------------

pyexiv2 (http://tilloy.net/dev/pyexiv2/download.html)  
hachoir (https://bitbucket.org/haypo/hachoir)  
