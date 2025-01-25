const scrollingBox = document.getElementById('chat-content');
scrollingBox.scrollTop = scrollingBox.scrollHeight;

const observer = new MutationObserver(() => {
    scrollingBox.scrollTop = scrollingBox.scrollHeight;
});

observer.observe(scrollingBox, { childList: true });


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function fetchMessages() {
    var currentUrl = window.location.href;
    var urlParts = currentUrl.split('/');
    var chatId = urlParts[urlParts.length - 2];
    var requestUrl = 'http://localhost:8000/account/update-chat/' + chatId + '/';

    $.ajax({
        url: requestUrl,
        type: 'GET',
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            $('#chat-content').html(data);            
        }
    });
}

$(document).ready(function () {
    setInterval(fetchMessages, 2000);
});

document.getElementById('file-input').addEventListener('change', function () {
    var file = this.files[0];
    var maxSize = 7 * 1024 * 1024;

    if (file.size > maxSize) {
        alert('حجم فایل بیش از 7 مگابایت است!');
        this.value = '';
        document.getElementById('fileNameBox').innerText = '';
    } else {
        var fileName = file.name;
        document.getElementById('fileNameBox').innerText = 'فایل شما: ' + fileName;
    }
});