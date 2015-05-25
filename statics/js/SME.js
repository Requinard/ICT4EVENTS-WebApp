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

        list.empty();

        var url = "/api/auto/plek/"

        var totalURL = url + value + "/";

        console.log(totalURL)

        $.get(totalURL, function (data) {
            console.log(data);

            for(var i =0; i!= data.length; i++)
            {
                list.append('<li class="list-group=item">' + data[i]['waarde'] + '</li>');
            }
        })
    });
});