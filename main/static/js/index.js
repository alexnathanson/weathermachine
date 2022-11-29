let runUpdateInfo

let gMode = 0

//populate the file options drop down menu
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

//populate the port options drop down menu
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

//clean these characters from the responses
function cleanList(aList){
    aList = aList.replace("[","");
    aList = aList.replace("]","");
    aList = aList.replace(/["']/g,"");
    aList = aList.split(",")
    return aList
}

//this is run when the function is submitted
function formHandling(){
    let runBool = true

    console.log("Form Handling")

    //get port
    let fPort = document.getElementById('ports').value
    fPort = fPort.split(" - ")[0]
    //console.log(typeof fPort);

    if(fPort.length === 0){
        runBool = false
        alert("Arduino not found! Check Arduino connection and refresh page.")
    }

    //get file
    let fFile = document.getElementById('files').value
    fFile = fFile.replace(".csv","")
    //console.log(fFile);

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

    //get time range
    let sDay = document.getElementById('sd').value;
    let sTime = document.getElementById('st').value;
    let eDay = document.getElementById('ed').value;
    let eTime = document.getElementById('et').value;

    //runBool = checkDateTimeFormat(sDay, eDay, sTime,eTime)

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
    //console.log(fLight);


    if(runBool){
        let runSettings = "port="+fPort+"&file="+fFile+"&facade="+fFacade+"&time="+fTime+"&light="+fLight

        //if all start and end fields are specified add to the call
        if(sDay != "" && eDay != "" && sTime != "" && eTime != ""){
            runSettings = runSettings + "&sday=" + sDay + "&stime=" + sTime + "&eday=" + eDay + "&etime=" + eTime
        }
        console.log(runSettings)
        httpGetAsync("http://127.0.0.1:5000/weather?" + runSettings, updateData)
    } else {
        console.log("Form not submitted because of formatting errors.")
    }

}

//this is run after the form is submitted
function updateData(){
    //httpGetAsync("http://127.0.0.1:5000/data",makeGraph)
    clearInterval(runUpdateInfo)
    runUpdateInfo = setInterval(()=>{httpGetAsync("http://127.0.0.1:5000/runStats",runInfo)}, 10000); 
}

function checkDateTimeFormat(dValS, dValE, hValS,hValE){
    //this should catch malformated dates
    try {

        let [month, day, year] = dValS.split('-');
        let  sD = new Date(month, day,year);
        [month, day, year] = dValE.split('-');
        let  eD = new Date(month, day, year);

        console.log(typeof eD)
        //check if the days are in order
        if(sD <= eD){
            console.log("d order!")
            //check data types
            try{
                hValS = int(hValS)
                hValE = int(hValE)

                //check ranges
                if(hValS > 0 && hValS <= 24 && hValE > 0 && hValE <= 24){
                    //check sequence if on the same day
                    if(sD == eD){
                        if (hValE >= hValS){
                            return true;
                        } else {
                            alert("End hour must be after start hour!")
                            return false;
                        }
                    } else {
                        return true;
                    }                    
                } else {
                    alert("Hours must be in range of 1 to 24!")
                    return false;
                }
            } catch {
                alert("Hours must be integers!")
                return false;
            }
        } else {
            alert("Start date must be before end date")
            return false;
        }
        
    } catch (error){
        //console.log(error)
        alert("Dates must be in D-M-YYYY format!")
        return false;
    }
    
}

//update live run info
function runInfo(rData){

    rData = JSON.parse(rData)

    //console.log("Updating!")

    let percent = document.getElementById('percent')
    percent.innerHTML = "Percent complete: " + rData['percent'] + "%" 

    let timeellapsed = document.getElementById('time-ellapsed')

    let eT
    //hourly resolution
    if(rData['elapsedTime'] > (60*60)){
        eT = String(rData['elapsedTime']/60/60) + " hours"
    } else if (rData['elapsedTime'] > 60){
        eT = String(rData['elapsedTime']/60) + " minutes"
    } else {
        eT = String(rData['elapsedTime']) + " seconds"
    }
    timeellapsed.innerHTML = "Ellapsed time: " + eT

    let timeremaining = document.getElementById('time-remaining')
    timeremaining.innerHTML = "Est. Time remaining: " + rData['estimatedRemainingTimes']

    let lO = document.getElementById('lightOutput')
    lO.innerHTML = "Light: " + rData['light']
    console.log(rData['light'])

    //change this so its only run once at the start to collect the run data
    //if(rData['elapsedTime'] > 0){
    httpGetAsync("http://127.0.0.1:5000/data", (r)=>{drawChart(JSON.parse(r),rData['percent'],gMode)})
    //}
}

/*function makeGraph(gData){
    console.log(JSON.parse(gData))
    //let graph = document.getElementById('graph')
    //graph.innerHTML = gData
    drawChart(gData)
}*/

//this stops the current test. It is triggered when the stop button is pressed
function stopRun(){
    httpGetAsync("http://127.0.0.1:5000/weather?stop=true", (response)=>{console.log(response)})
}

//this shuts down the program
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

function graphMode(mode){
    gMode = mode;
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

//get data via API needed to specify test settings
httpGetAsync("http://127.0.0.1:5000/options?options=files", fillFiles)
httpGetAsync("http://127.0.0.1:5000/options?options=ports", fillPorts)

