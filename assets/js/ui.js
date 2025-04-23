// side nav

let menuicn = document.querySelector(".menuicn")
let nav = document.querySelector(".nav-container")


menuicn.onclick = function () {
    // console.log("menu icon clicked")
    nav.classList.toggle("nav-close");
    checkNav()

}

function checkNav() {
    if (nav.classList.contains("nav-close")) {
        localStorage.removeItem('nav');
        localStorage.setItem('nav', 'mini');
    } else {
        localStorage.removeItem('nav');
        localStorage.setItem('nav', 'full');

    }
}
function setNav() {
    const NavState = localStorage.getItem('nav')
    if (NavState == 'mini') {
        nav.classList.add("nav-close")
    } else if (NavState == 'full') {
        nav.classList.remove("nav-close")
    } else {

    }
}

document.addEventListener('DOMContentLoaded', setNav())


// clear DOM
let contracticn = document.querySelector(".nav-option")
let stats = document.querySelector(".box-container")
let tbl = document.querySelector(".snippet")



contracticn.onclick = function () {
    console.log("contract icon clicked")
    stats.remove()
    tbl.remove()
}

// active side nav

let navoptions = document.querySelectorAll(".nav-dash-options a")
let icontext = document.querySelector(".nav-option i")
let bodyId = document.querySelector("body").id
let containerId = document.querySelector(".content-container").id


for (let option of navoptions) {
    if (option.dataset.active == containerId) {

        option.classList.add('active')
        icontext.classList.add('active')

    } else {
        option.classList.remove('active')
        icontext.classList.remove('active')

    }
}

// let newuser = document.getElementById("submit-user")
// let userinputs = document.querySelectorAll(".new-user > div > input")
// let newinputs = document.querySelectorAll(".new-data > div > input")
// let newselects = document.querySelectorAll(".new-data > div > select")
// // console.log(newinputs)

// newuser.onclick = function (e) {
//     e.preventDefault()

//     for (let i = 0; i < newinputs.length; i++) {
//         newinputs[i].removeAttribute('disabled')

//     }
//     for (let x = 0; newselects.length; x++) {
//         newselects[x].removeAttribute('disabled')

//     }
// }


