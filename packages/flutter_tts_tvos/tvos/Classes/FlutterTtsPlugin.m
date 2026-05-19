#import "FlutterTtsPlugin.h"
// Renamed to the tvOS federated module: the Swift→ObjC generated header
// follows the pod/module name (`flutter_tts_tvos`), not the upstream
// `flutter_tts`.
#if __has_include(<flutter_tts_tvos/flutter_tts_tvos-Swift.h>)
#import <flutter_tts_tvos/flutter_tts_tvos-Swift.h>
#else
// Support project import fallback if the generated compatibility header
// is not copied when this plugin is created as a library.
// https://forums.swift.org/t/swift-static-libraries-dont-copy-generated-objective-c-header/19816
#import "flutter_tts_tvos-Swift.h"
#endif

@implementation FlutterTtsPlugin
+ (void)registerWithRegistrar:(NSObject<FlutterPluginRegistrar>*)registrar {
  [SwiftFlutterTtsPlugin registerWithRegistrar:registrar];
}
@end
