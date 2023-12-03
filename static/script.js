var base_format = 'd-m-Y H:i'
var time_format = 'H:i'
new AirDatepicker('#filter_table_calendar', {
    range: true,
    multipleDatesSeparator: ' - ',
    isMobile: true,
    autoClose: true,
    onSelect({date, formattedDate, datepicker}) {
        if (formattedDate.length == 2){
            renew_table();
        }
    }
})

$.datetimepicker.setLocale('ru');
function renew_datetime_pickers_in_modals(){
    $('#modal_end_time').datetimepicker({
        lang: "ru",
        format: base_format,
        step: 30,
        minTime:'9:00',
        maxTime: '23:30',
        datepicker:false,
        onShow:function( ct ){
            let temp_time = '';
            if (jQuery('#modal_start_time').val()){
                temp_time = jQuery('#modal_start_time').val().split(" ")[1];
                temp_time = `${(+temp_time.split(":")[0] + 1)}:${temp_time.split(":")[1]}` 
            }
            this.setOptions({
                minDate:jQuery('#modal_start_time').val()?jQuery('#modal_start_time').val():false,
                maxDate:jQuery('#modal_start_time').val()?jQuery('#modal_start_time').val():false,
                minTime:temp_time?temp_time:"9:00",
            })
        },
    });
    $('#modal_start_time_only').datetimepicker({
        lang: "ru",
        step: 30,
        minTime:'8:00',
        maxTime: '23:30',
        datepicker:false,
        format: time_format,
        onShow:function( ct ){
            let temp_time = '';
            if (jQuery('#modal_end_time_only').val()){
                temp_time = jQuery('#modal_end_time_only').val();
                temp_time = `${(+temp_time.split(":")[0] - 1)}:${temp_time.split(":")[1]}`
            }
            this.setOptions({
                maxTime:temp_time?temp_time:"22:00",
            })
        },
    });
    $('#modal_end_time_only').datetimepicker({
        lang: "ru",
        step: 30,
        minTime:'9:00',
        maxTime: '23:30',
        datepicker:false,
        format: time_format,
        onShow:function( ct ){
            let temp_time = '';
            if (jQuery('#modal_start_time_only').val()){
                temp_time = jQuery('#modal_start_time_only').val();
                temp_time = `${(+temp_time.split(":")[0] + 1)}:${temp_time.split(":")[1]}` 
            }
            this.setOptions({
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
    document.querySelectorAll(".raspisanie_block_weekly").forEach(function (block) {
        block.addEventListener("click", function (event) {
            let id = event.target.dataset.orderid;
            show_repeatative_selection_modal(id);
        })
    })
    
}
document.querySelectorAll("#cort_type_id").forEach(function (block) {
    block.addEventListener("change", function (event) {
        renew_table();
    })
})
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
function show_repeatative_selection_modal(id){
    let request = {
        "block_id" : id
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/get_change_repeatative_modal_template/');
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

function show_repeatative_modal(){
    let request = {
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/get_create_repeatative_modal_template/');
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
function delete_repeatative_event(orderid){
    let request = {
        "block_id": orderid,
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/delete_repeatative_raspisanie_object/');
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
        "cort_id" : document.getElementById("cort_modal_id").value,
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
        "cort_id" : document.getElementById("cort_modal_id").value,
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
function create_new_repeatative_event(){
    let request = {
        "time_start": document.getElementById("modal_start_time_only").value,
        "time_end" : document.getElementById("modal_end_time_only").value,
        "description" : document.getElementById("description").value,
        "days" :  $('#weekdays').val(),
        "cort_id" : document.getElementById("cort_modal_id").value,
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/create_repeatative_raspisanie_object/');
    xhr.setRequestHeader("Content-Type", "application/json;");
    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                document.querySelector(".dialog").close()
            } else {
                console.error('Ошибка запроса:', xhr.status);
                let response = xhr.response;
                var error_text = ""
                if (response.error == undefined) {
                    error_text = "Ошибка запроса";
                } else {
                    error_text = response.error;
                }
                console.log(error_text)
                document.querySelector(".error_text").textContent = error_text;
            }
        }
    };
    xhr.send(JSON.stringify(request));
}
function change_repeatative_event(orderid) {
    let request = {
        "block_id": orderid,
        "time_start": document.getElementById("modal_start_time_only").value,
        "time_end" : document.getElementById("modal_end_time_only").value,
        "description" : document.getElementById("description").value,
        "days" :  $('#weekdays').val(),
        "cort_id" : document.getElementById("cort_modal_id").value,
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/change_repeatative_raspisanie_object/');
    xhr.setRequestHeader("Content-Type", "application/json;");
    xhr.responseType = 'json';
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 201) {
                document.querySelector(".dialog").close()
            } else {
                console.error('Ошибка запроса:', xhr.status);
                let response = xhr.response;
                if (response.error == undefined) {
                    var error_text = "Ошибка запроса";
                } else {
                    var error_text = response.error;
                }
                document.querySelector(".error_text").textContent = error_text;
            }
        }
    };
    xhr.send(JSON.stringify(request));
}
function renew_table() {
    let request = get_filter();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/server/v1/renew_table/');
    xhr.setRequestHeader("Content-Type", "application/json;");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                let response = xhr.response;
                document.getElementById("timetable_table").innerHTML = response;
                renew_cell_click_events();
            } else {
                console.error('Ошибка запроса:', xhr.status);
            }
        }
    };
    xhr.send(JSON.stringify(request));
}

function get_filter(){
    let filter = {
        "date_range" : document.getElementById("filter_table_calendar").value,
        "cort_id" : document.getElementById("cort_type_id").value,
    }
    return filter;
}


var client_id = Date.now()
var ws = new WebSocket(`wss://timetable.limetennis.ru/ws/${client_id}`);
console.log(ws)
ws.onmessage = function(event) {
    console.log("test")
    //document.getElementById("timetable_table").innerHTML = event.data;
    renew_table();
    
};
renew_datetime_pickers_in_modals();
renew_cell_click_events();