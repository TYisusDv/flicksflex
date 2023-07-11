var api_path = window.location.pathname;
var api_load = false;
var api_typingTimer;
var api_CSRFToken = null;

$(document).ready(function () {
    api_path = window.location.pathname;  
    
    if(api_path == "/"){
        api_path = '/home';
    }

    history.pushState(null, null, api_path);
    api_loadView();

    $(document).on("click", "a", function (event) {
        event.preventDefault();
        
        var path = $(this).attr("href");
        var lv = $(this).attr("lv");
    
        if (lv == "0") {
            window.location = path;
        } else if(lv=="1"){
            window.open(path, "_blank");
        } else {
            if (path != "javascript:;" && !path.startsWith("#") && path != api_path) {
                if(!api_load){
                    api_path = path;
                    history.pushState(null, null, api_path);
                    api_loadView();
                }
            }
        }
    });
    
    $(window).on("popstate", function () {
        if(!api_load){
            api_loadView();
        } else {
            history.pushState(null, null, path);
        }
    });
});

function api_web_get_tokencsrf(callback) {
    $.ajax({
        url: `/api/web/token/csrf`,
        type: 'GET',
        dataType: 'json',
        success: function (xhr) {
            if (xhr.success) {
                api_CSRFToken = xhr.token;
                callback(api_CSRFToken);
            } else {
                api_CSRFToken = null;
                callback(api_CSRFToken);
            }
        },
        error: function (xhr) {
            api_CSRFToken = null;
            callback(api_CSRFToken);
        }
    });
}

function api_loadView() {
    if(!api_load){
        api_load = true;        
        
        $('#appcontainer').fadeOut(400, function () {
            $(this).html($("#preloader").html()).fadeIn(400);
        });
                
        api_path = window.location.pathname;
                
        var response = api_sendData(url = `widget${api_path}`, type = 'POST');
        response.then(function (response) {
            $('#appcontainer').fadeOut(400, function () {
                $(this).html(response.html).fadeIn(400);
            });           
            api_load = false;
        }).catch(function (response) {
            api_load = false;            
        });
    }
}

function api_sendData(url = '', type = 'GET', formData = new FormData()) {
    return new Promise(function (resolve, reject) {
        api_web_get_tokencsrf(function (token) {
            $.ajax({
                url: `/api/web/${url}`,
                type: type,
                data: formData,
                dataType: 'json',
                processData: false,
                contentType: false,
                enctype: 'multipart/form-data',
                beforeSend: function (xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                        xhr.setRequestHeader('X-CSRFToken', api_CSRFToken);
                    }
                },
                success: function (xhr) {
                    resolve(xhr);
                },
                error: function (xhr) {
                    reject(xhr);
                }
            });
        });
    });
}