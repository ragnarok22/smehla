function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSaveMethod(method) {
    // these http methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function (e) {
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSaveMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    let btn_scroll = $('.go-top');

    //Show or hide the sticky footer button
    $(window).scroll(function (e) {
        if ($(this).scrollTop() > 200) {
            btn_scroll.fadeIn(200);
        } else {
            btn_scroll.fadeOut(200);
        }
    });

    //animate the scroll to top
    btn_scroll.click(function (ev) {
        ev.preventDefault();
        $('html, body').animate({scrollTop: 0}, 300);
    });
});