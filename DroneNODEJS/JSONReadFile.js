/*var fs = require("fs");

fs.readFile("/home/r2d2/maya/2015-x64/DroneStuff/test3.json", "utf8", function(error, data){
	console.log(data);
});*/

var arDrone = require('ar-drone');
var client = arDrone.createClient();
var ctrl = require('Controller');
//client.config('general:navdata_demo', 'False');
