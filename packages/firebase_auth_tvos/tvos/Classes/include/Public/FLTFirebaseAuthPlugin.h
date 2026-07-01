// Copyright 2020 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#import <TargetConditionals.h>

#if TARGET_OS_OSX
#import <FlutterMacOS/FlutterMacOS.h>
#else
#import <Flutter/Flutter.h>
#endif

// Restored by hand — see FLTFirebaseAuthPlugin.m for why the porter's
// removal of this import was wrong (ASAuthorizationController et al. are
// used by FLTFirebaseAuthPlugin below and are tvOS 13+ APIs).
#import <AuthenticationServices/AuthenticationServices.h>
#import <Foundation/Foundation.h>
// Points at our own firebase_core_tvos pod, not upstream's "firebase_core"
// pod (which has no tvOS platform declaration) — see PORTING_REPORT.md.
#if __has_include(<firebase_core_tvos/FLTFirebasePlugin.h>)
#import <firebase_core_tvos/FLTFirebasePlugin.h>
#else
#import "FLTFirebasePlugin.h"
#endif
#import "firebase_auth_messages.g.h"

#if !TARGET_OS_OSX
@protocol FlutterSceneLifeCycleDelegate;
#endif

@interface FLTFirebaseAuthPlugin
    : FLTFirebasePlugin <FlutterPlugin,
                         FirebaseAuthHostApi,
                         FirebaseAuthUserHostApi,
                         MultiFactorUserHostApi,
                         MultiFactoResolverHostApi,
                         MultiFactorTotpHostApi,
                         MultiFactorTotpSecretHostApi,
                         ASAuthorizationControllerDelegate,
                         ASAuthorizationControllerPresentationContextProviding
#if !TARGET_OS_OSX
#if __has_include(<Flutter/FlutterSceneLifeCycle.h>)
                         ,
                         FlutterSceneLifeCycleDelegate
#endif
#endif
                         >

+ (FlutterError *)convertToFlutterError:(NSError *)error;
@end
