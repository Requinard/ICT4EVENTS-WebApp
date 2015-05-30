$(document).ready(function () {
    $('#form-field-search').keypress(function (e) {
        // This is enter
        if (e.charCode === 13 || e.key === "Enter") {
            var text = e.currentTarget.value;
            text = text.replace(/abc/g, '');
            var url = "/search/";
            window.location = url + text + "/";
        }
    });

});

$(function () {
    $(".datepicker").datepicker();
    $( ".datepicker" ).datepicker( "option", "dateFormat","dd/mm/yy" );
});
$(document).ready(function () {
    $("#plek_autosearch").on('input', function (e) {
        var value = e.currentTarget.value;
        var list = $("#plek_listgroup");

        var url = "/api/auto/plek/"

        var totalURL = url + value + "/";

        console.log(totalURL);

        var plekken = {};

        $.get(totalURL, function (data) {
            if (data.length <= 0) {
                list.empty();
                list.append('<li class="list-group-item">Niks gevonden!</li>')
            }
            else {
                list.empty()
                //TODO: make pretty representation
                for (var i = 0; i != data.length; i++) {
                    var inter = {};
                    var id = data[i]['plek']['id']
                    if (id in plekken) {
                        plekken[id]['specificatie'].push(data[i]['specificatie']['naam']);
                        plekken[id]['waarde'].push(data[i]['waarde']);
                    }
                    else {

                        inter['naam'] = data[i]['plek']['nummer'];
                        inter['capaciteit'] = data[i]['plek']['capaciteit'];

                        inter['specificatie'] = [data[i]['specificatie']['naam']];

                        inter['waarde'] = [data[i]['waarde']];

                        plekken[id] = inter;
                    }
                }

                for (var item in plekken) {
                    var specString = "";
                    for (var i = 0; i != plekken[item]['specificatie'].length; i++) {
                        var internal_state = plekken[item]['specificatie'][i] + ": " + plekken[item]['waarde'][i] + "<br />";
                        specString += internal_state
                    }

                    var string = '<li class="list-group-item">Naam: ' + plekken[item]['naam'] + "<br />" + specString + "<a href='#' class='btn btn-default plek_clickable pull-right' plek_id=" + item + ">Reserveer</a></li>";

                    console.log(string);
                    list.append(string);
                }
            }
        })
    });
});

$(document).ready(function ($) {

    $('.password-field').strength({
        strengthClass: 'strength',
        strengthMeterClass: 'strength_meter',
        strengthButtonClass: '',
        strengthButtonText: '',
        strengthButtonTextToggle: 'Hide Password'
    });

});