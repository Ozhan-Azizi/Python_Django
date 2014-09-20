//
//  DetailViewController.h
//  TryOut
//
//  Created by Ozhan Azizi on 20/09/2014.
//  Copyright (c) 2014 Ozhan Azizi. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DetailViewController : UIViewController

@property (strong, nonatomic) id detailItem;
@property (weak, nonatomic) IBOutlet UILabel *detailDescriptionLabel;

@end

