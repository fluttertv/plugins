## 0.0.1

Initial release — tvOS implementation of `connectivity_plus` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Generated
by `flutter-tvos plugin port`.

* **Supported:** `checkConnectivity()` and `onConnectivityChanged`
  (`NWPathMonitor`-backed). Results: `wifi`, `ethernet`, `vpn`, `none`.
* **Differs from iOS:** no `mobile` / cellular result — Apple TV has
  no cellular radio. Wired Apple TVs report `ethernet`.
* **Not supported on tvOS:** cellular detection (not applicable).

Verified end-to-end on a physical Apple TV (integration tests pass).
See `README.md` and `PORTING_REPORT.md` for detail.
