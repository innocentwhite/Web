// using jQuery
//used for csrf authentication
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//end csrf

//process mouseon and out event
jQuery.fn.mouseon = function(type, ori_one, new_one) {
    $(this).mouseover(function(){
        if ($(this).attr(type)==undefined){
            $(this).css(type, new_one);
        }
        else {
            $(this).attr(type, new_one);
        }
    })
    $(this).mouseout(function(){
        if ($(this).attr(type)==undefined){
            $(this).css(type, ori_one);
        }
        else {
            $(this).attr(type, ori_one);
        }
    })
}

$(document).ready(function(){
    //one modal attach different title
    //show gallery
    $(function () { $("[data-toggle='tooltip']").tooltip(); });
    $('#myModal').on('show.bs.modal', function (event) {
      // var button = $(event.relatedTarget) // Button that triggered the modal
      // var recipient = button.data('whatever') // Extract info from data-* attributes
      // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
      // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
      //get path and get project
      var path = window.location.pathname;
      var arr = path.split('/');
      arr = jQuery.grep(arr, function(value){
          return value != '';
      });
      var Project = arr[arr.length-1];
      var modal = $(this)
      modal.find('.modal-title').text(Project + ' Gallery')
    })
    $("#chose_from_database").on('click', function () {
    	var host = window.location.host
        var gal = $('#idx_gallery');
        var param={'num': 10};
        //get path and get project
        var path = window.location.pathname;
        var arr = path.split('/');
        arr = jQuery.grep(arr, function(value){
            return value != '';
        });
        var Project = arr[arr.length-1];
        $.ajax({
            url: "/"+ Project +"/gallery/",
            type: "POST",
            data: param,
            success: function (data, textStatus, jqXHR) {
                var tobj = $.parseJSON(data);
                var dataLen=tobj.length;
                var maxSiz=200;
                gal.empty();
                for(var ii=0; ii<dataLen; ii++) {
                    var tUrl = tobj[ii];
                    var pw = 200;
                    var ph = 200;
                    // if (tobj[ii].w >= tobj[ii].h) {
                    //     pw = maxSiz;
                    //     ph = Math.floor(maxSiz * tobj[ii].h / tobj[ii].w);
                    // } else {
                    //     pw = Math.floor(maxSiz * tobj[ii].w / tobj[ii].h);
                    //     ph = maxSiz;
                    // }
                    var tmpImg = $('<img>',{
                        class: 'img-thumbnail',
                        width: pw,
                        height: ph,
                        id:  'gal_'+ii,
                        src: "http://"+host+"/static/"+Project+"_gallery_thumb/"+tUrl
                    });
                    $(tmpImg).on('click', function() {
                        var spl = this.src.split('/');
                        var fn  = spl[spl.length-1];
                        console.log(fn);
                        $('#gallery-close').click();
                        $('#img_name').val(fn);
                        $('#gallery_submit').click();
                        // var param2={'fname': fn};
                        // $.ajax({
                        //     url: "/project/"+Project+"/",
                        //     type: "POST",
                        //     data: param2,
                        //     success: function (data, textStatus, jqXHR) {
                        //         console.log(data);
                        //     },
                        //     error: function (jqXHR, textStatus, errorThrown) {
                        //         funShowErrorMessage('Server error: bad image in DB');
                        //     }
                        // });
                        //window.location="/";
                    });
                    $(tmpImg).css('cursor','pointer');
                    $(tmpImg).prop('title', 'Press mouse button to add image');
                    gal.append(tmpImg);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                funShowErrorMessage('Error gallery query...');
            }
        });
    });
    //select file button：
    $('#up_from_local').on('click', function(){
        $('#file').click();
    })
    //remove button
    $('#remove').on('click', function(){
        $('#imagediv').attr('hidden', 'hidden');
    })
    // interact with user
    $('#file').change(function(){
        var path = window.location.pathname;
        var arr = path.split('/');
        arr = jQuery.grep(arr, function(value){
            return value != '';
        });
        var Project = arr[arr.length-1];
        var file = $(this)[0].files[0];
        var img_name = file.name;
        $('#submit').click();
        var param2={'img_name': img_name};
        $(this).send_recv_display(Project, param2);
    })

    //change color when mouse on:
    $('#chose_from_database').mouseon('background-color', '#696969', '#494949');
    $('#up_from_local').mouseon('background-color', '#428bca', '#226baa');
    $('#remove').mouseon('background-color', '#FA8072', '#DA6052')
    $('#proj1-img').mouseon("src", "static/img/diabetic_before.jpg", "static/img/diabetic_after.jpg")
    $('#proj2-img').mouseon("src", "static/img/lung_before.png", "static/img/lung_after.png")
    $('.proj-btn').mouseon("background-color", "#428BCA", "#226BAA")
    //example
    // $('#logo').mouseover(function(){
    //     $(this).find('img').css("border", "3px solid red");
    // });
    // $('#logo').mouseout(function(){
    //     $(this).find('img').css("border", "0px solid red");
    // });
    // $('#logo').on('click', function(){
    //     $('#Show_Large_Image').find('#image_show').html('<img src="static/img/logo.png" alt="logo""/>')
    // });
    var width = document.body.clientWidth;
    var height = document.body.clientHeight;
    var width_use = 0;
    var height_use = 0;
    if (height > width){
        height_use = height*0.45;
        width_use = 'auto';
    }
    else{
        width_use = width*0.45;
        height_use = 'auto';
    }
    if (width<500){
        width_use = width*0.8;
        height_use = width*0.8;
    }
    $('#input_image').mouseon("border", "0px solid red", "3px solid red");
    $('#input_image').on('click', function(){
        var src = $(this).attr("src")
        $('#Show_Large_Image').find('#image_show').html('<img src='+ src + ' style="height:'+height_use+'px;width: '+width_use+'px;"/>')
    });
    $('#processed_image').mouseon("border", "0px solid red", "3px solid red")
    $('#processed_image').on('click', function(){
        var src = $(this).attr("src")
        $('#Show_Large_Image').find('#image_show').html('<img src='+ src + ' style="height:'+height_use+'px;width: '+width_use+'px;"/>')
    });
});
