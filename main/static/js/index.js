//this is called when facade button is pressed
function setFacade(f) {
    let bData
    b = document.getElementById(f)
    
    //change color
    if(b.textContent == "shedable"){
        b.textContent = "critical"
        bData = {branch: bNum, status :1}
    } else {
        b.textContent = "shedable"
        bData = {branch: bNum, status:0}
    }

    httpPost("http://localhost:5000/input",f)
}

function fillFiles(fileList){
    fileList = fileList.replace("[","");
    fileList = fileList.replace("]","");
    fileList = fileList.split(",")
    console.log(fileList)
    console.log(typeof fileList)

    let menu = document.getElementById('files')

    for(let l of fileList){
        let option = document.createElement("option");
        option.text = l;
        menu.add(option);
    }
    
}

//update live run info
function updateScreen(){

}

const xhr = new XMLHttpRequest();

function httpGetAsync(dst, callback){
    xhr.open("GET", dst, true);
    xhr.onload = (e) => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
              //console.log(xhr.responseText);
              callback(xhr.responseText)
            } else {
              console.error(xhr.statusText);
            }
        }
    };
    xhr.onerror = (e) => {
      console.error(xhr.statusText);
    };
    xhr.send(null); 
}



/*function httpGet(dst, syncBool,callback){

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", dst, syncBool ); // false for synchronous request
    xmlHttp.send( null );

    //use callback if async
    if(syncBool){
        callback()
    } else{ 
        //return text is syncronous
        return xmlHttp.responseText;
    }
}*/

function httpPost(dst,pData){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", dst, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(
        pData));
}

httpGetAsync("http://127.0.0.1:5000/options?options=files", fillFiles)

updateScreen()

setInterval(updateScreen, 5000); 
