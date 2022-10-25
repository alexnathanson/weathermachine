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