var page = require('webpage').create();
console.log('The default user agent is ' + page.settings.userAgent);
page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36';

var system = require('system');
var args = system.args;

var url = 'https://new.nicehash.com/miner/';
if (args.length === 1) {
  console.log('Requires a nice hash miner address parameter.');
  phantom.exit();
} else {
  args.forEach(function(arg, i) {
    console.log(i + ': ' + arg);
  });
  url += args[1];
}

page.open(url, function(status) {
  if (status !== 'success') {
    console.log('Unable to access network');
  } else {
    var ua = page.evaluate(function() {
      return document.textContent;
    });
    console.log(page.plainText);
  }
  phantom.exit();
});
