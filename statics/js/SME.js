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

$(document).ready(function () {
    $("#plek_autosearch").on('input', function (e) {
        var value = e.currentTarget.value;
        var list = $("#plek_listgroup");

        var url = "/api/auto/plek/"

        var totalURL = url + value + "/";

        console.log(totalURL)

        $.get(totalURL, function (data) {
            if (data.length <= 0) {
                list.empty();
                list.append('<li class="list-group-item">Niks gevonden!</li>')
            }
            else {
                console.log(data);
                list.empty();
                for (var i = 0; i != data.length; i++) {
                    $.get("/api/plek/" + data[i]['plek'] + "/", function (plek_data) {

                        list.append('<li class="list-group-item">' + plek_data['nummer'] + '</li>');
                    })

                }
            }
        })
    });
});