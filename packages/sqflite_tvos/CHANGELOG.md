## 0.0.1

Initial release — tvOS implementation of `sqflite` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Generated
by `flutter-tvos plugin port` (modular-SwiftPM podspec) from
`sqflite_darwin`.

* **Supported:** full SQLite — `openDatabase`, `execute`, `rawQuery`,
  `query`, `insert`, `update`, `delete`, transactions, batches
  (`sqlite3` ships with tvOS).
* **Differs from iOS:** the tvOS sandbox is constrained and
  OS-managed caches can be purged — put the database under a
  `path_provider` directory (Documents / Application Support),
  **not** in a cache / temp dir, if you need durability.
* **Not supported on tvOS:** none for core SQLite usage.

Simulator build GREEN and 14/14 integration tests pass. On-device
verification recommended for storage-durability edge cases. See
`README.md` and `PORTING_REPORT.md` for detail.
