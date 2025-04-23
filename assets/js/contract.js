let add_prod = document.querySelector(".addprod-container")

let add_client = document.querySelector(".addclient-container")

let prod_btn = document.querySelector("#plus-product")

let client_btn = document.querySelector("#plus-client")


client_btn.onclick = function () {
    add_client.style.display = 'block';
}

prod_btn.onclick = function () {
    add_prod.style.display = 'block';
}

window.onclick = function (event) {
    if (event.target == add_prod) {
        add_prod.style.display = 'none'
    }
    if (event.target == add_client) {
        add_client.style.display = 'none'
    }
}