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
}

function changeInput(selectObj) {
    let s = selectObj.value.split("-")
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
    let value = selectObj.value
    let s = value.split("%")

    let change_elem = document.getElementById(`passed%${s[0]}%${s[1]}`)
    if(s[2] !== "none") {
        let v_pass = data[selectObj.getAttribute("pass_grade")]
        let v_enter = data[s[2]]

        if(v_enter >= v_pass){
            change_elem.innerText = "Pass"
        }
        else if(v_enter === 0.0){
            change_elem.innerText = "Fail"
        }
        else{
            change_elem.innerText = "Not pass"
        }
    }
    else{
        change_elem.innerText = "Unknown"
    }
}
