

function onSignIn(googleUser) {
    const access_token = googleUser.getAuthResponse().access_token;
    $.ajax({
        type: 'post',
        url: '/auth/social-login/',
        dataType: 'json',
        data: {
            "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val(),
            "access_token": access_token
        },
        success: function () {
            location.href = "/";
        },
    });
}
