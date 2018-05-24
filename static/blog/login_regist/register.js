/**
* Created by huang on 2018/3/10.
*/


var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
});


//获取图形验证码
var code = "";
function get_image_code() {
    //获取当前时间戳
    var d = new Date().getTime();
    //code给了上一个时间戳变量
    var pre_code = code;

    code = d;
    $(".imgcode").attr("src", "/user/auth/captcha?pre_code="+pre_code+"&code="+code);
    $(".captcha-code").attr("value",code);
}


$(document).ready(function() {
    get_image_code();
    $('.imgcode').click(function () {
        get_image_code();
    });
});


//验证类函数
function checkUserName(username){
  var pattern = /^\w{3,}$/;  //用户名格式正则表达式：用户名要至少三位
  if(username.value.length == 0){
    return false;
    }
  if(!pattern.test(username.value)){
    return false;
    }
   else{
     return true;
     }
  }


//注册
$(document).ready(function () {
    $('#button').click(function () {
        event.preventDefault();
        var email = $('#email').val();
        var password = $('#password').val();
        var username = $('#user').val();
        var password1 = $('#password1').val();
        var verify = $('#verify').val();
        var timestamp = $('.captcha-code').val();
        $.ajax({
            'url': '/user/auth/register/',
            'type': 'post',
            'data': {
                'email': email,
                'password': password,
                'username': username,
                'password1': password1,
                'verify': verify,
                'timestamp': timestamp
            },
            'success': function (data) {
                if(data['status'] == 200){
                     swal({
                            'title': '注册成功!',
                            'text': data['msg'],
                            'type': 'success',
                            'showCancelButton': false,
                            'showConfirmButton': false,
                            'timer': 1000
                     },function () {
                         window.location = '/user/auth/login/'
                     })
                }
                else {
                     swal({
                            'title': '注册失败!',
                            'text': data['msg'],
                            'type': 'error',
                            'showCancelButton': true,
                            'showConfirmButton': true,
                            //'timer': 2000
                     },function () {
                         location.reload()
                     })
                }
            }
        })
    });
});



  //验证用户名

  //验证密码
function checkPassword(userpasswd){
  var pattern = /^\w{4,8}$/; //密码要在4-8位
  if(!pattern.test(userpasswd.value)){

    return false;
    }
   else{
     return true;
     }
  }
  //确认密码
  function ConfirmPassword(){
  var userpasswd = document.getElementById('userPasword');
  var userConPassword = document.getElementById('userConfirmPasword');
  var errConPasswd = document.getElementById('conPasswordErr');
  if((userpasswd.value)!=(userConPassword.value) || userConPassword.value.length == 0){
    errConPasswd.innerHTML="上下密码不一致";
    errConPasswd.className="error";
    return false;
    }
   else{
     errConPasswd.innerHTML="OK";
     errConPasswd.className="success";
     return true;
     }
  }
//验证手机号
  function checkPhone(){
  var userphone = document.getElementById('userPhone');
  var phonrErr = document.getElementById('phoneErr');
  var pattern = /^1[34578]\d{9}$/; //验证手机号正则表达式
  if(!pattern.test(userphone.value)){
    phonrErr.innerHTML="手机号码不合规范";
    phonrErr.className="error";
    return false;
    }
   else{
     phonrErr.innerHTML="OK";
     phonrErr.className="success";
     return true;
     }
  }