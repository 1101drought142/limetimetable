var base_format = 'd.m.Y H:i'
new AirDatepicker('#from_calendar', {
    range: true,
    multipleDatesSeparator: ' - ',
    isMobile: true,
    autoClose: true,
})

$.datetimepicker.setLocale('ru');

$('#modal_start_time').datetimepicker({
    lang: "ru",
    format: base_format,
    step: 30,
    minTime:'8:00',
    maxTime: '22:30',
    onShow:function( ct ){
        let temp_time = '';
        if (jQuery('#modal_end_time').val()){
            temp_time = jQuery('#modal_end_time').val().split(" ")[1];
            temp_time = `${(+temp_time.split(":")[0] - 1)}:${temp_time.split(":")[1]}` 
        }
        this.setOptions({
            maxDate:jQuery('#modal_end_time').val()?jQuery('#modal_end_time').val():false,
            maxTime:temp_time?temp_time:"22:30",
        })
    },
});
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


 function close_modal(element){
    let modal = element.closest(".dialog");
    modal.close()
 }