let add_client_modal = document.querySelector(".addclient-container")
let edit_client_modal = document.querySelector(".editclient-container")

let add_client_btn = document.querySelector("#addclient-btn")
let edit_client_btn = document.querySelectorAll(".updclient-btn")

add_client_btn.onclick = function () {
    add_client_modal.style.display = 'block'
}

edit_client_btn.onclick = function () {
    edit_client_modal.style.display = 'block'
}

window.onclick = function (event) {
    if (event.target == add_client_modal) {
        add_client_modal.style.display = 'none'
    }
    if (event.target == edit_client_modal) {
        edit_client_modal.style.display = 'none'
    }
}
