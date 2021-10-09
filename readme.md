# camviewer
viewer for some panasonic network cameras in the BL-C line. currently works for single cameras. the aim is to give it multi-camera support, movement commands, and vim keybindings.

requires PyQt5, numpy, & opencv2. i'm hoping to drop the latter two in the long run but we'll see.

needs a settings.yaml file with `ip` and `authcode` fields. the former is self-explanatory. the latter is a code attached as a header to http requests from authorised users. i think it might be the same for all cameras in this line (it's at least the same for all of the 4 that i have, which are different models). it's easy to find if you look at the http requests.
