let output = document.getElementById("results");
let random_output = document.getElementById("random");


function getIp() {
    output.textContent += location.host;
};

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   random_output.textContent += result;
}

getIp();
makeid(10);