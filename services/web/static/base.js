$(function() {
    $('#shorten_btn').click(function() {
        $.ajax({
                type: "POST",
                url: "/shorten/",
                data: {
                    'url': $('#url').val(),
                    'custom_subpart': null || $('#custom_subpart').val(),
                },
                dataType: 'json',
            })
            .always(function(data_jqXHR, textStatus, jqXHR_errorThrown) {
                if (textStatus === 'error') {
                    var jqXHR = data_jqXHR;
                } else {
                    var jqXHR = jqXHR_errorThrown;
                }
                var data = data_jqXHR;
                console.log(data);

                switch (jqXHR.status) {
                    case 200:
                        $('#result').text('Succeed!');
                        $('#url').val(data.subpart_inner);
                        $('#custom_subpart').val('');
                        break;
                    default:
                        $('#result').text(JSON.parse(data.responseText).error);
                        break;
                }

            });
    });
});
