// open close menu
let menuBtn = document.getElementById('menu_btn');
let closeBtn = document.getElementById('btn_close');
let menu = document.getElementById("sidebar");
menuBtn.addEventListener("click",()=>{
    menu.classList.add("show_sidebar")
})

closeBtn.addEventListener("click",()=>{
    menu.classList.remove("show_sidebar")
})


// form preventdefault submit

function mySubmitFunction(e) {
    e.preventDefault();
    return false;
  }


// transfer page

function mySubmitFunction(event) {
    event.preventDefault();

    var transferMethod = document.querySelector('.button_group button.active').getAttribute('aria-label');
    var recipientInfo;
    if (transferMethod === 'via_no') {
        recipientInfo = document.getElementById('phone_no').value;
    } else if (transferMethod === 'via_ac') {
        recipientInfo = document.getElementById('account_no').value;
    }


    var amount = document.getElementById('amount').value;

    console.log('Transfer Method:', transferMethod);
    console.log('Recipient Info:', recipientInfo);
    console.log('Amount:', amount);

    return false;
}

document.querySelectorAll('.button_group button').forEach(button => {
    button.addEventListener('click', function() {

        document.querySelectorAll('.button_group button').forEach(btn => {
            btn.classList.remove('active');
        });
        this.classList.add('active');

        var transferMethod = this.getAttribute('aria-label');
        if (transferMethod === 'via_no') {
            document.querySelector('.phone_no_info').style.display = 'block';
            document.querySelector('.account_info').style.display = 'none';
        } else if (transferMethod === 'via_ac') {
            document.querySelector('.phone_no_info').style.display = 'none';
            document.querySelector('.account_info').style.display = 'block';
        }
    });
});


