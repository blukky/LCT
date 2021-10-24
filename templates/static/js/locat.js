jQuery(function () {
    let data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
    $('.next-btn').attr('disabled', 'disabled');

    const email = document.getElementById('id_email');
    const fio = document.getElementById('id_fio');
    const telephone = document.getElementById('id_telephone');
    let bEmail = false;
    let bFIO = false;
    let bFTelephone = false;

    function checkVal() {
        if (bEmail && bFIO && bFTelephone) {
            return true;
        } else {
            return false;
        }
    }


    email.addEventListener('change', function () {
        bEmail = email.checkValidity();
        if (checkVal()) {
            $('.next-btn').removeAttr('disabled');
            email.setCustomValidity('');
        } else {
            email.setCustomValidity('Неправилный email!');
            $('.next-btn').attr('disabled', 'disabled');
        }
    });

    fio.addEventListener('change', function () {
        bFIO = fio.checkValidity();
        if (checkVal()) {
            $('.next-btn').removeAttr('disabled');
            fio.setCustomValidity('');
        } else {
            fio.setCustomValidity('Не корректно заполнено поле ФИО!');
            $('.next-btn').attr('disabled', 'disabled');
        }
    });

    telephone.addEventListener('change', function () {
        bFTelephone = telephone.checkValidity();
        if (checkVal()) {
            $('.next-btn').removeAttr('disabled');
            telephone.setCustomValidity('');
        } else {
            telephone.setCustomValidity('Не корректно заполнено поле Телефон!');
            $('.next-btn').attr('disabled', 'disabled');
        }
    });
    $('.next-btn').click(function () {
        if ($(this).text() == 'Далее') {
            data['fio'] = $('input[name="fio"]').val();
            data['email'] = $('input[name="email"]').val();
            data['telephone'] = $('input[name="telephone"]').val();
            $(this).text('Отправить');
        } else {
            data['character'] = $('input[name="character"]').val();
            data['time'] = $('input[name="time"]').val();
            data['name_industry'] = $('select[name="name_industry"]').val();
            data['street'] = $('select[name="street"]').val();
            data['city'] = $('input[name="city"]').val();
            data['house_number'] = $('input[name="house_number"]').val();
            data['comment'] = $('input[name="comment"]').val();
            $.ajax({
                url: 'location',
                type: 'POST',
                data: data,
                success: function (data) {
                    console.log(data.ok);
                }
            });
            $('.prev-btn').hide();
            $(this).hide();
        }
    });
});