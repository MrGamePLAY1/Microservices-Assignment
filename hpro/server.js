var hprose = require("hprose");
function hello(name) {
    return "Hello " + name + "!";
}
var server = hprose.Server.create("http://0.0.0.0:8080");
server.addFunction(hello);
server.start();