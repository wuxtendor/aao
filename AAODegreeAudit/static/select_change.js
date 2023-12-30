const data = {
    "A": 4.0,
    "A-": 3.67,
    "B+": 3.33,
    "B": 3.0,
    "B-": 2.67,
    "C+": 2.33,
    "C": 2.0,
    "C-": 1.67,
    "D+": 1.33,
    "D": 1.0,
    "F": 0.0
};

function creditChangeInput(selectObj){
    let section = selectObj.id.split("-")[1];
    let selects = document.getElementById(`${section}-credits`);
    let minus = 0;
    for(let elem of selects.children){
        minus += parseInt(elem.value);
    }
    let span = document.getElementById(`need_credits-${section}`);
    let finalCredits = parseInt(span.getAttribute("credits")) - minus;
    if(finalCredits < 0){
        span.innerText = `${0}`;
    }
    else{
        span.innerText = finalCredits.toString();
    }

    let allSelects = document.getElementsByClassName("is_credit");
    let totalCredits = 0;
    for(let elem of allSelects){
        totalCredits += parseInt(elem.value);
    }
    let totalCreditB = document.getElementById("total_credits");
    totalCreditB.innerText = totalCredits.toString();
}

function changeInput(selectObj) {
    let s = selectObj.value.split("-");
    let k = s[1];
    let i = Number(s[2]);
    let j = Number(s[3]);
    let enable_elem = document.getElementById(`course_level-${k}-${i}-${j}`);
    enable_elem.removeAttribute("hidden");

    let a = 0
    while(!!enable_elem) {
        if(a === j){
            a++;
            continue;
        }
        enable_elem = document.getElementById(`course_level-${k}-${i}-${a}`);
        enable_elem.setAttribute("hidden", "");
        a++;
    }
}

function gradeChangeInput(selectObj){
    let value = selectObj.value;
    let s = value.split("%");

    let change_elem = document.getElementById(`passed%${s[0]}%${s[1]}`);
    if(s[2] !== "none") {
        let v_pass = data[selectObj.getAttribute("pass_grade")];
        let v_enter = data[s[2]];

        if(v_enter >= v_pass){
            change_elem.innerText = "Pass";
        }
        else if(v_enter === 0.0){
            change_elem.innerText = "Fail";
        }
        else{
            change_elem.innerText = "Not pass";
        }
    }
    else{
        change_elem.innerText = "Unknown";
    }
}

function save(blob) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = 'test.txt'; //filename
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}

function downloadExcel(majorId){
    let formElem = document.querySelector("form");
    formElem.onsubmit = async (e) => {
        e.preventDefault();
    }
    let formData = new FormData(formElem);
    let formDict = {};
    for(let [key, value] of formData.entries()){
        formDict[key] = value;
    }
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/download_form/")
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    const body = JSON.stringify(formDict);
    xhr.responseType = 'blob';
    xhr.onload = (e) => {
        console.log(e);
        save(xhr.response);
    }
    xhr.send(body);
}