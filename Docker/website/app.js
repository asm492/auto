const express = require("express")
const app = express();

app.get("/", function(req, res){
    res.send("Hello from function");
});

app.listen(8080, function(){
    console.log("App listening on 8080");
});