# camviewer
viewer for some panasonic network cameras in the BL-C line. currently works for viewing multiple cameras. still need to add movement commands and vim keybindings.

requires requests, pyyaml, PyQt5, numpy, & opencv2. i'm hoping to drop the latter two in the long run but we'll see.

needs a `settings.yaml` file containing an , and a list of `cams`, each with `ip`, `port`, and `authcode` fields, the latter containing a base6-encoded `user:pass` 

    cams:
        - ip: <ip1>
          port: <port1>
          authcode: <authcode1>
        - ip: <ip2>
          port: <port2>
          authcode: <authcode2>
        etc...
