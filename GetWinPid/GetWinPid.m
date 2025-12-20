//
//  GetWinPid
//
//  $ clang -o GetWinPid -lobjc -framework Foundation -framework CoreGraphics GetWinPid.m
//
//  Created on 12/19/25.
//

#import <Foundation/Foundation.h>
#import <CoreGraphics/CoreGraphics.h>
#include <stdio.h>
#include <unistd.h>

#define Log(fmt, ...) \
fprintf(stdout, "%s", [[NSString stringWithFormat:(fmt), ##__VA_ARGS__] UTF8String])

NSString *Right(NSString *s, NSInteger width, NSString *padSymbol)
{
    NSInteger padding = width - [s length];
    if (padding < 0) padding = 0;

    NSString *pad = [@"" stringByPaddingToLength:padding
                                      withString:padSymbol
                                 startingAtIndex:0];

    return [pad stringByAppendingString:s];
}

NSString *Left(NSString *s, NSInteger width, NSString *padSymbol)
{
    return [s stringByPaddingToLength:width
                           withString:padSymbol
                      startingAtIndex:0];
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        CFArrayRef wlBefore = CGWindowListCopyWindowInfo(kCGWindowListExcludeDesktopElements, kCGNullWindowID);
        Log(@"Move target window\n");
        sleep(5);
        CFArrayRef wlAfter = CGWindowListCopyWindowInfo(kCGWindowListExcludeDesktopElements, kCGNullWindowID);

        NSMutableSet *result = [NSMutableSet setWithArray:(__bridge NSArray *)wlBefore];
        [result minusSet:[NSSet setWithArray:(__bridge NSArray *)wlAfter]];
        Log(@"\nList of windows that moved:\n");
        Log(@"%@ %@  %@\t[Title] SubTitle\n",
              Right(@"PID",7,@" "),
              Right(@"WinID",5,@" "),
              Left(@"x,y,w,h",21,@" ")
              );
        Log(@"%@ %@  %@ %@\n",
              Right(@"-",7,@"-"),
              Right(@"-",5,@"-"),
              Left(@"-",21,@"-"),
              @"\t-------------------------------------------"
              );

        for (NSObject* v in result) {
            //NSLog(@"Class <%@>\n", [v class]);
            NSNumber *OwnerPID = [v valueForKey:@"kCGWindowOwnerPID"] ?: @"?";
            NSNumber *WindowNumber = [v valueForKey:@"kCGWindowNumber"] ?: @"?";
            NSString *OwnerName = [v valueForKey:@"kCGWindowOwnerName"] ?: @"";
            NSString *WindowName = [v valueForKey:@"kCGWindowName"] ?: @"";
            NSObject *WindowBounds = [v valueForKey:@"kCGWindowBounds"];
            NSString *Coords = @"";
            if (WindowBounds!=nil) {
                Coords = [NSString stringWithFormat:@"{%@,%@,%@,%@}",
                          [WindowBounds valueForKey:@"X"],
                          [WindowBounds valueForKey:@"Y"],
                          [WindowBounds valueForKey:@"Width"],
                          [WindowBounds valueForKey:@"Height"]
                          ];
            }

            if ([WindowName length]!=0)
                WindowName = [@" " stringByAppendingString:WindowName];
            Log(@"%@ %@  %@\t[%@] %@\n",
                  Right([OwnerPID stringValue],7,@" "),
                  Right([WindowNumber stringValue],5,@" "),
                  Left(Coords,21,@" "),
                  OwnerName,
                  WindowName
                  );
        }
        //Log(@"%@", result);
        Log(@"\n");
    }
    return 0;
}
