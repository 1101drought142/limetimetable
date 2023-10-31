var base_format = 'd-m-Y H:i'
new AirDatepicker('#from_calendar', {
    range: true,
    multipleDatesSeparator: ' - ',
    isMobile: true,
    autoClose: true,
})

$.datetimepicker.setLocale('ru');
function renew_datetime_pickers_in_modals(){
    // $('#modal_start_time').datetimepicker({
    //     lang: "ru",
    //     format: base_format,
    //     step: 30,
    //     minTime:'8:00',
    //     maxTime: '22:30',
    //     onShow:function( ct ){
    //         let temp_time = '';
    //         if (jQuery('#modal_end_time').val()){
    //             temp_time = jQuery('#modal_end_time').val().split(" ")[1];
    //             temp_time = `${(+temp_time.split(":")[0] - 1)}:${temp_time.split(":")[1]}` 
    //         }
    //         this.setOptions({
    //             maxDate:jQuery('#modal_end_time').val()?jQuery('#modal_end_time').val():false,
    //             maxTime:temp_time?temp_time:"22:30",
    //         })
    //     },
    // });
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
            console.log(temp_time)
            console.log(jQuery('#modal_start_time').val().split(" "))
            this.setOptions({
                minDate:jQuery('#modal_start_time').val()?jQuery('#modal_start_time').val():false,
                minTime:temp_time?temp_time:"9:00",
            })
        },
    });
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
                if (response.success === false) {
                    console.log("error")
                } else {
                    console.log("success")
                    console.log(response)

                    let container = document.querySelector(".modals");
                    container.innerHTML = response;
                    renew_datetime_pickers_in_modals();
                }
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

document.querySelectorAll(".raspisanie_block_empty").forEach(function (block) {
    block.addEventListener("click", function (event) {
        let temp_date = event.target.dataset.date;
        let temp_time = event.target.dataset.starttime;
        show_modal(temp_date, temp_time);
    })
})