name = Math.random();
console.log("my name is " + name);
card = [];
selectCard = [];
updateData = [];
userCard = [];
var cardcolor = new Array(13)
var cardpoint = 0;
function sendData(event, name, card) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function()
    {
        if(this.readyState == 4 && this.status == 200) {
            re = this.responseText
            //console.log("my name is " + name);
            if(re.length > 20){
                updateData = JSON.parse(this.responseText);
                userCard = updateData['userCard'];
                cardOld = updateData['cardOld'];
                for(var i =0; i<13;i++){
                    cardpoint = userCard[i]%13+1;
                    cardcolor[i] = Math.floor(userCard[i]/13);
                    userCard[i]=cardpoint;
                    console.log(cardcolor[i]);
                    if(cardcolor[i]==0){
                        cardcolor[i] = '梅花'
                    }
                    else if(cardcolor[i]==1){
                        cardcolor[i] = '方塊'
                    }
                    else if(cardcolor[i]==2){
                        cardcolor[i] = '愛心'
                    }
                    else{
                        cardcolor[i] = '黑桃'
                    }
                }
                updateData['userCard']=userCard;
                //console.log(updateData)
                document.getElementById("name").innerHTML = name.toString();
                document.getElementById("mycard").innerHTML = updateData['userCard'].toString();
                document.getElementById("turncard").innerHTML = updateData['cardOld'].toString();
                document.getElementById("turn").innerHTML = updateData['userTurn'].toString();
                document.getElementById("mycard_color").innerHTML = cardcolor.toString();
            }
            else{
                console.log(this.responseText)
            }
        }
    }
    xhr.open("POST", "/");
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded');
    xhr.send("event=" + event + "&name=" + name + "&card=" + JSON.stringify(card));
}
setInterval(function(){
    sendData('update',name,'')
},1000);
function oncli() {
    text = JSON.parse(document.getElementById("myinput").value);
    console.log(text);
    card = [];
    sendData("sendCard", name, text);
}
function fakeSendData() {
    for (i in card){
        card[i] = userCard[card[i]];
    }
    sendData("sendCard", name, card);
    card = [];
}
function addCard(a){
    var yes = 0;
    for (i in card){
        if(card[i] == a){
            yes = 1;
            break;
        }
    }
    if(yes == 0){
        card.push(a)
    }
}