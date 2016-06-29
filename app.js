/*eslint-env node*/

//------------------------------------------------------------------------------
// node.js starter application for Bluemix
//------------------------------------------------------------------------------

// This application uses express as its web server
// for more info, see: http://expressjs.com
var express = require('express');
var fs = require('fs');

// cfenv provides access to your Cloud Foundry environment
// for more info, see: https://www.npmjs.com/package/cfenv
var cfenv = require('cfenv');

// create a new express server
var app = express();

// body-parser for form data
app.use(require('body-parser')());

// serve the files out of ./public as our main files
app.use(express.static(__dirname + '/public'));

// get the app environment from Cloud Foundry
var appEnv = cfenv.getAppEnv();

app.get('/railways', function(request, response){
	response.sendfile('./public/railways.html');
});

app.get('/book', function(request, response){
	response.sendfile('./public/books.html');
});

app.post('/placeOrder', function(request, response){
	//extract the order from request object
	console.log(request.body);
	fs.readFile('public/orders.json', {encoding: "utf8", flag: "r"}, function(err, data){
		if (err) {
			console.log("Read Error");
		}
		else{
			var orders = JSON.parse(data);
			orders.push(request.body);
			var options = {encoding: "utf8", flag: "w"};
			fs.writeFile('public/orders.json', JSON.stringify(orders), options, function(err){
				if (err) {
					console.log("Order write failed");
				}
				else{
					console.log("Order saved.");
				}
			});
		}
	});
});

app.get('/admin', function(request, response){
	response.sendfile('./public/myAdmin.html');
});

app.post('/saveOrder', function(request, response){
	var options = {encoding: 'utf8', flag: 'w'}
	fs.writeFile('public/orders.json', JSON.stringify(request.body), options, function(err){
		if (err) {
			console.log("Order write failed");
		}
		else{
			console.log("Order saved.");
		}
	});
});

// start server on the specified port and binding host
app.listen(appEnv.port, '0.0.0.0', function() {
  // print a message when the server starts listening
  console.log("server starting on " + appEnv.url);
});
