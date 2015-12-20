var testRequire = require('./test-require');

console.log("Hello world! - Sent from your javascript application. " + testRequire.woo());

// invoke an undefined function to test the stacktrace
testStacktrace()
