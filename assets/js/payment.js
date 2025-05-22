let mpesa_modal = document.querySelector(".mpesa-container");

// let stk_modal = document.querySelector(".modal-container");

let bank_modal = document.querySelector(".bank-container");

let cash_modal = document.querySelector(".cash-container");

// let stkbtn = document.querySelector("#stk-btn");

let mpesabtn = document.querySelector("#mpesa-btn");

let bankbtn = document.querySelector("#bank-btn");

let cashbtn = document.querySelector("#cash-btn");

let addcbtn = document.querySelector("#addclient-btn");

// stkbtn.onclick = function () {
//   stk_modal.style.display = "block";
// };
mpesabtn.onclick = function () {
  mpesa_modal.style.display = "block";
};

bankbtn.onclick = function () {
  bank_modal.style.display = "block";
};

cashbtn.onclick = function () {
  cash_modal.style.display = "block";
};

window.onclick = function (event) {
  // if (event.target == stk_modal) {
  //   stk_modal.style.display = "none";
  // }
  if (event.target == mpesa_modal) {
    mpesa_modal.style.display = "none";
  }
  if (event.target == bank_modal) {
    bank_modal.style.display = "none";
  }
  if (event.target == cash_modal) {
    cash_modal.style.display = "none";
  }
};
