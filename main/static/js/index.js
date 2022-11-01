let runUpdateInfo

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
    fileList = cleanList(fileList)
    console.log(fileList)
    console.log(typeof fileList)

    let menu = document.getElementById('files')

    for(let l of fileList){
        let option = document.createElement("option");
        option.text = l;
/*        option.class = "select"*/
        menu.add(option);
    }
}

function fillPorts(portList){
    portList = cleanList(portList)
    /*console.log(portList)
    console.log(typeof portList)*/

    let pMenu = document.getElementById('ports')

    for(let l of portList){
        let option = document.createElement("option");
        option.text = l;
        pMenu.add(option);
    }
}

function cleanList(aList){
    aList = aList.replace("[","");
    aList = aList.replace("]","");
    aList = aList.replace(/["']/g,"");
    aList = aList.split(",")
    return aList
}

function formHandling(){
    let runBool = true

    console.log("Form Handling")

    //get port
    let fPort = document.getElementById('ports').value
    fPort = fPort.split(" - ")[0]
    console.log(typeof fPort);

    if(fPort.length === 0){
        runBool = false
        alert("Arduino not found! Check Arduino connection and refresh page.")
    }

    //get file
    let fFile = document.getElementById('files').value
    fFile = fFile.replace(".csv","")
    console.log(fFile);

    //get facade

    let fFacade = document.getElementsByName('facade');
    for (let f = 0; f < fFacade.length; f++) {
        if (fFacade[f].checked) {
            fFacade = fFacade[f].value
            console.log(fFacade);
            break;
        }
    }
    if(typeof fFacade != "string"){
        runBool = false
        alert("Facade is not selected!")
    }

    //get time scale

    let fTime = document.getElementsByName('time');
    console.log(typeof fTime)
    for (let t = 0; t < fTime.length; t++) {
        if (fTime[t].checked) {
            fTime = fTime[t].value
            console.log(fTime);
            break;
        }
    }
    if(typeof fTime != "string"){
        runBool = false
        alert("Time is not selected!")
    }

    //get components
    let fLight = document.getElementById('lights').checked
    console.log(fLight);


    if(runBool){
        let runSettings = "port="+fPort+"&file="+fFile+"&facade="+fFacade+"&time="+fTime+"&light="+fLight
        console.log(runSettings)
        httpGetAsync("http://127.0.0.1:5000/weather?" + runSettings, updateData)
    }

}

function updateData(){
    httpGetAsync("http://127.0.0.1:5000/data",makeGraph)
    clearInterval(runUpdateInfo)
    runUpdateInfo = setInterval(()=>{httpGetAsync("http://127.0.0.1:5000/runStats",runInfo)}, 10000); 
}

//update live run info
function runInfo(rData){

    rData = JSON.parse(rData)

    console.log("Updating!")

    console.log(rData)

    let percent = document.getElementById('percent')
    percent.innerHTML = "Percent complete: " + rData['percent'] + "%" 

    let timeellapsed = document.getElementById('time-ellapsed')
    timeellapsed.innerHTML = "Ellapsed time: " + rData['elapsedTime']

    let timeremaining = document.getElementById('time-remaining')
    timeremaining.innerHTML = "Est. Time remaining: " + rData['estimatedRemainingTimes']

    if(rData['elapsedTime'] > 0){
        ("http://127.0.0.1:5000/data", makeGraph)
    }

    drawChart()
}

function makeGraph(gData){
    let graph = document.getElementById('graph')
    graph.innerHTML = gData
}

function stopRun(){
    httpGetAsync("http://127.0.0.1:5000/weather?stop=true", (response)=>{console.log(response)})
}

function shutdown(){
    httpGetAsync("http://127.0.0.1:5000/shutdown", (response)=>{console.log(response)})
}

function httpGetAsync(dst, callback){
    const xhr = new XMLHttpRequest();
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

httpGetAsync("http://127.0.0.1:5000/options?options=ports", fillPorts)