# camviewer
viewer for some panasonic network cameras in the BL-C line. currently works for viewing multiple cameras (though still needs layout manipulation). also right now it doesn't work on my older cameras for some reason. the aim is to give it movement commands and vim keybindings.

requires requests, pyyaml, PyQt5, numpy, & opencv2. i'm hoping to drop the latter two in the long run but we'll see.

needs a `settings.yaml` file containing an `authcode` which is `user:pass` base64-encoded (only supports all cameras on same credentials for now), and a list of `cams`, each with `ip` and `port` fields:

    authcode: <code>
    cams:
        - ip: <ip1>
          port: <port1>
        - ip: <ip2>
          port: <port2>
        etc...
