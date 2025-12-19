//
//  GetWinPid
//
//  $ clang -o GetWinPid -lobjc -framework Foundation -framework CoreGraphics GetWinPid.m
//
//  Created on 12/19/25.
//

#import <Foundation/Foundation.h>
#import <CoreGraphics/CoreGraphics.h>
#include <unistd.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        CFArrayRef wlBefore = CGWindowListCopyWindowInfo(kCGWindowListExcludeDesktopElements, kCGNullWindowID);
        NSLog(@"Move target window\n");
        sleep(5);
        CFArrayRef wlAfter = CGWindowListCopyWindowInfo(kCGWindowListExcludeDesktopElements, kCGNullWindowID);

        NSMutableSet *result = [NSMutableSet setWithArray:(__bridge NSArray *)wlBefore];
        [result minusSet:[NSSet setWithArray:(__bridge NSArray *)wlAfter]];
        NSLog(@"\nList of windows that moved:");
        NSLog(@"%@", result);
        NSLog(@"\n");
    }
    return 0;
}
