var base_format = 'd-m-Y H:i'
new AirDatepicker('#from_calendar', {
    range: true,
    multipleDatesSeparator: ' - ',
    isMobile: true,
    autoClose: true,
})

//$.datetimepicker.setLocale('ru');
function renew_datetime_pickers_in_modals(){
    $('#modal_end_time').datetimepicker({
        lang: "ru",
        format: base_format,
        step: 30,
        minTime:'9:00',
        maxTime: '23:30',
        onShow:function( ct ){
            let temp_time = '';
            if (jQuery('#modal_start_time').val()){
                temp_time = jQuery('#modal_start_time').val().split(" ")[1];
                console.log(temp_time)
                temp_time = `${(+temp_time.split(":")[0] + 1)}:${temp_time.split(":")[1]}` 
            }
            this.setOptions({
                minDate:jQuery('#modal_start_time').val()?jQuery('#modal_start_time').val():false,
                maxDate:jQuery('#modal_start_time').val()?jQuery('#modal_start_time').val():false,
                minTime:temp_time?temp_time:"9:00",
            })
        },
    });
}
function renew_cell_click_events() {
    document.querySelectorAll(".raspisanie_block_empty").forEach(function (block) {
        block.addEventListener("click", function (event) {
            let temp_date = event.target.dataset.date;
            let temp_time = event.target.dataset.starttime;
            show_modal(temp_date, temp_time);
        })
    })
    document.querySelectorAll(".raspisanie_block_ordered, .raspisanie_block_payed").forEach(function (block) {
        block.addEventListener("click", function (event) {
            let id = event.target.dataset.orderid;
            show_selection_modal(id);
        })
    })
}
function show_selection_modal(id){
    let request = {
        "block_id" : id
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/get_change_modal_template/');
    xhr.setRequestHeader("Content-Type", "application/json;");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                let response = xhr.responseText;
                let container = document.querySelector(".modals");
                container.innerHTML = response;
                renew_datetime_pickers_in_modals();
            } else {
                console.error('Ошибка запроса:', xhr.status);
            }
        }
    };
    xhr.send(JSON.stringify(request));
}
function show_modal(date, time){
    let request = {
        "start_time": time,
        "date" : date,
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/get_create_modal_template/');
    xhr.setRequestHeader("Content-Type", "application/json;");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                let response = xhr.responseText;
                let container = document.querySelector(".modals");
                container.innerHTML = response;
                renew_datetime_pickers_in_modals();
            } else {
                console.error('Ошибка запроса:', xhr.status);
            }
        }
    };
    xhr.send(JSON.stringify(request));
}

function create_new_event(){
    let request = {
        "date_start": document.getElementById("modal_start_time").value,
        "date_end" : document.getElementById("modal_end_time").value,
        "status" : document.getElementById("modal_status").value,
        "client_name" : document.getElementById("client_name").value,
        "client_phone" : document.getElementById("client_phone").value,
        "client_mail" : document.getElementById("client_mail").value,
        "client_bitrix_id" : document.getElementById("client_bitrix_id").value,
        "client_site_id" : document.getElementById("client_site_id").value,
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/create_raspisanie_object/');
    xhr.setRequestHeader("Content-Type", "application/json;");
    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                document.querySelector(".dialog").close()
            } else {
                console.error('Ошибка запроса:', xhr.status);
                let response = xhr.response;

                document.querySelector(".error_text").textContent = response.error;
            }
        }
    };
    xhr.send(JSON.stringify(request));
}

function close_modal(element){
    let modal = element.closest(".dialog");
    modal.close()
}
function delete_event(orderid){
    let request = {
        "block_id": orderid,
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/delete_raspisanie_object/');
    xhr.setRequestHeader("Content-Type", "application/json;");
    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                document.querySelector(".dialog").close()
            } else {
                console.error('Ошибка запроса:', xhr.status);
                let response = xhr.response;
                document.querySelector(".error_text").textContent = response.error;
            }
        }
    };
    xhr.send(JSON.stringify(request));
}
function edit_event(orderid){
    let request = {
        "block_id": orderid,
        "date_start": document.getElementById("modal_start_time").value,
        "date_end" : document.getElementById("modal_end_time").value,
        "status" : document.getElementById("modal_status").value,
        "client_name" : document.getElementById("client_name").value,
        "client_phone" : document.getElementById("client_phone").value,
        "client_mail" : document.getElementById("client_mail").value,
        "client_bitrix_id" : document.getElementById("client_bitrix_id").value,
        "client_site_id" : document.getElementById("client_site_id").value,
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/change_raspisanie_object/');
    xhr.setRequestHeader("Content-Type", "application/json;");
    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                document.querySelector(".dialog").close()
            } else {
                console.error('Ошибка запроса:', xhr.status);
                let response = xhr.response;
                document.querySelector(".error_text").textContent = response.error;
            }
        }
    };
    xhr.send(JSON.stringify(request));
}

var client_id = Date.now()
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
ws.onmessage = function(event) {
    console.log("test")
    document.getElementById("timetable_table").innerHTML = event.data;
    renew_cell_click_events();
};
renew_datetime_pickers_in_modals();
renew_cell_click_events();