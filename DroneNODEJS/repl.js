var fs = require('fs');
var path = require('path');
var arDrone = require('ar-drone');
var arDroneConstants = require('ar-drone/lib/constants');
var autonomy = require('./Controller');

var client  = arDrone.createClient();
var c    = new autonomy(client, {debug: false});
var repl    = client.createRepl();

function navdata_option_mask(c) {
  return 1 << c;
}

// From the SDK.
var navdata_options = (
    navdata_option_mask(arDroneConstants.options.DEMO)
  | navdata_option_mask(arDroneConstants.options.VISION_DETECT)
  | navdata_option_mask(arDroneConstants.options.MAGNETO)
  | navdata_option_mask(arDroneConstants.options.WIFI)
);

// Connect and configure the drone
client.config('general:navdata_demo', true);
client.config('general:navdata_options', navdata_options);
client.config('video:video_channel', 1);
client.config('detect:detect_type', 12);

// Add a ctrl object to the repl. You can use the controller
// from there. E.g.
// ctrl.go({x:1, y:1});
//
repl._repl.context['c'] = c;
