# otp-notify
Computes One-Time-Passwords using `oathtool` from [oath-toolkit](http://www.nongnu.org/oath-toolkit/) and displays them in a desktop notification.

The input consits of a `tokens.xml` file from the Android application [FreeOTP](https://freeotp.github.io/), found in `/data/data/org.fedorahosted.freeotp/shared_prefs`, and placed in the same directory as `otp.py`.

Obvious disclaimer: only use this software if you are aware of the security implications.

Requires [xmltodict](https://pypi.python.org/pypi/xmltodict/) and python-gobject.
