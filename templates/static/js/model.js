jQuery(function () {
    let data = {};
    $('#btn_dff').click(function () {
        data['type'] = 'dff';
    });
    $('#btn_dnc').click(function () {
        data['type'] = 'dnc';
    });
    $('#btn_rnn').click(function () {
        data['type'] = 'rnn';
    });
    $('#reg').click(() => data['out'] = 'reg');
    $('#classif').click(() => data['out'] = 'classif');
    $('body').click(function (e) {
        if ($('#next').is(e.target)) {
            if ($('#checkStep1').is(':visible')) {
                data['type'] = 'dff';
            }
            if ($('#checkStep2').is(':visible')) {
                data['size'] = parseInt($("#num").text());
            }
            if ($('#checkStep3').is(':visible')) {
                data['out'] = 'reg';
            }
            if ($('#checkStep4').is(':visible')) {
                e.preventDefault();
                e.stopImmediatePropagation();
                // console.log($('#features')[0].dropzone.getAcceptedFiles()[0]);
                var formData = new FormData();
                formData.append('features', $("#features")[0].dropzone.getAcceptedFiles()[0]);
                formData.append('answer', $("#answer")[0].dropzone.getAcceptedFiles()[0]);
                formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
                formData.append('type', data['type']);
                formData.append('size', data['size']);
                formData.append('out', data['out']);
                $.ajax({
                    type: "POST",
                    url: 'model_ajax',
                    cache: false,
                    contentType: false,
                    processData: false,
                    data: formData,
                    dataType: 'json',
                    success: function (msg) {
                        var val = Math.round(msg.val * 100);
                        $('#grafik')[0].ariaValueNow = String(Math.round(msg.val * 100));
                        $('#name_model').text(msg.name);
                    }
                });
            }
        }
    });
    // $('#save').click(function () {
    //     $.ajax({
    //         type: "GET",
    //         url: 'save_model',
    //         success: function (msg) {
    //             $('#name_model').text('Модель удалена!');
    //         }
    //     });

    $('#cancel').click(function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        $.ajax({
            type: "GET",
            url: 'cancel_model',
            success: function (msg) {
                $('#name_model').text('Модель удалена!');
            }
        });
    });
});