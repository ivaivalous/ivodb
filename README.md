# ivodb

## Unfortunately, this project is no longer in active development

## Scripter Workflow

Ivodb is capable of safely executing user-provided, hence unsecure, JavaScript on the back-end. In order to do this in the safest possible way, execution is sandboxed by being executed via WebDriver and PhantomJS.

To do so, it utilizes the following flow:

 1. User-provided JavaScript is saved in a MongoDB database. This allows the user to access, update, or delete it.

 2. Consumers may request the script - in this case it shall be executed on the back-end. Since it could pottentially be harmful, it is run inside a sandbox.

 3. ivodb provides a number of helper JS functions. They allow the user to access consumer-specific data within their back-end script. For example, a script may use the consumer's IP address, user agent string or provided GET parameters.

 This is done by reading the relevant data from the HTTP request and replacing it within a text template to make up a valid chunk of JavaScript. The scripter builds this JavaScript as a variable and then has WebDriver execute it.

 The scripter then executes the user's JavaScript in the same "browser" session as the helper JS and returns the result of the execution.

 4. The WebDriver/PhantomJS session is closed and its return value is returned as an HTTP response to the customer.
