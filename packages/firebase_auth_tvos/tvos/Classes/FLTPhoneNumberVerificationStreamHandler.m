// Copyright 2021 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

@import FirebaseAuth;

#import "include/Private/FLTPhoneNumberVerificationStreamHandler.h"
#import "include/Public/FLTFirebaseAuthPlugin.h"

@implementation FLTPhoneNumberVerificationStreamHandler {
  FIRAuth *_auth;
  NSString *_phoneNumber;
#if TARGET_OS_OSX
#else
  FIRMultiFactorSession *_session;
  FIRPhoneMultiFactorInfo *_factorInfo;
#endif
}

#if TARGET_OS_OSX
- (instancetype)initWithAuth:(id)auth request:(InternalVerifyPhoneNumberRequest *)request {
  self = [super init];
  if (self) {
    _auth = auth;
    _phoneNumber = request.phoneNumber;
  }
  return self;
}
#else
- (instancetype)initWithAuth:(id)auth
                     request:(InternalVerifyPhoneNumberRequest *)request
                     session:(FIRMultiFactorSession *)session
                  factorInfo:(FIRPhoneMultiFactorInfo *)factorInfo {
  self = [super init];
  if (self) {
    _auth = auth;
    _phoneNumber = request.phoneNumber;
    _session = session;
    _factorInfo = factorInfo;
  }
  return self;
}
#endif

- (FlutterError *)onListenWithArguments:(id)arguments eventSink:(FlutterEventSink)events {
// Phone-number verification disabled on tvOS by hand: TARGET_OS_IPHONE is
// true on tvOS too (it covers all embedded Apple OSes, not just iOS), so
// this block compiled here unmodified — but Firebase's CocoaPods
// FirebaseAuth/Auth subspec doesn't export FIRPhoneAuthProvider's
// interface for tvOS, same situation as FIRTOTPSecret above. Phone/SMS
// auth has no tvOS UI path anyway (no SIM, no number entry affordance);
// the stream simply never emits an event on tvOS.
#if TARGET_OS_IPHONE && !TARGET_OS_TV
  id completer = ^(NSString *verificationID, NSError *error) {
    if (error != nil) {
      FlutterError *errorDetails = [FLTFirebaseAuthPlugin convertToFlutterError:error];
      events(@{
        @"name" : @"Auth#phoneVerificationFailed",
        @"error" : @{
          @"code" : errorDetails.code,
          @"message" : errorDetails.message,
          @"details" : errorDetails.details,
        }
      });
    } else {
      events(@{
        @"name" : @"Auth#phoneCodeSent",
        @"verificationId" : verificationID,
      });
    }
  };

  // Try catch to capture 'missing URL scheme' error.
  @try {
    if (_factorInfo != nil) {
      [[FIRPhoneAuthProvider providerWithAuth:_auth]
          verifyPhoneNumberWithMultiFactorInfo:_factorInfo
                                    UIDelegate:nil
                            multiFactorSession:_session
                                    completion:completer];

    } else {
      [[FIRPhoneAuthProvider providerWithAuth:_auth] verifyPhoneNumber:_phoneNumber
                                                            UIDelegate:nil
                                                    multiFactorSession:_session
                                                            completion:completer];
    }
  } @catch (NSException *exception) {
    events(@{
      @"name" : @"Auth#phoneVerificationFailed",
      @"error" : @{
        @"message" : exception.reason,
      }
    });
  }
#endif

  return nil;
}

- (FlutterError *)onCancelWithArguments:(id)arguments {
  return nil;
}

@end
