HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Sun, 24 Nov 2024 03:01:36 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: close
X-Powered-By: PHP/7.4.9

1fb5
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" /> 
    <meta name="keywords" content="">
    <meta name="author" content="Pang">
    <meta content="width=device-width, initial-scale=1.0, maximum-scale=2.3, user-scalable=0" name="viewport">
    <title>bai.com</title>
    <link rel="shortcut icon" type="image/ico" href="{:config('favicon')}"/>
    <link rel="stylesheet" href="https://static.dnparking.com/static/css/apply-form.css?v=1.0.0" />
    <script type="text/javascript" src="https://static.dnparking.com/js/jquery.min.js"></script>
    <script type="text/javascript" src="https://static.dnparking.com/js2/layer/layer.js"></script>
    <script type="text/javascript" src="https://static.dnparking.com/js2/exhibition.js?v1.0.3"></script>
</head>
<script type="text/javascript">
if (document.documentElement.clientWidth>=750) {
    document.documentElement.style.fontSize = 750 / 7.5 + 'px';
}else{
    document.documentElement.style.fontSize = document.documentElement.clientWidth / 7.5 + 'px';
}

function myload() {
    var script = document.createElement("script");
    script.src = "https://traffic.dnparking.com/analysis.js?d=bai.com&_t"+new Date().getTime();
    document.getElementsByTagName("body")[0].appendChild(script);
}

var islangcn = true;

$(function() {
    $('[data-toggle]').click(function() {
        $('.lang-cn').toggle();
        $('.lang-en').toggle();
        islangcn = !islangcn;
    })
});
</script>
<style type="text/css">
    *{
        padding: 0;
        margin: 0;
    }

    .lang-cn {}
    .lang-en {display: none;}

    html,body{
        width: 100%;
        height: 100%;
        background: url('./image/bg.jpg')no-repeat center;
        background-size: 100% 100%;
    }
    .hide { display: none; }
    .app-form {font-size: 0.15rem;}
    .pc_warp{
        width: 6rem;
        height: 5rem;
        position: absolute;
        margin: auto;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
    }
    .error_img{
        width: 3.57rem;
        position: absolute;
        margin: auto;
        left: 0;
        right: 0;
        top: 0;
    }
    .logo_img{
        width: 2.88rem;
        position: absolute;
        margin: auto;
        left: 0;
        right: 0;
        bottom: 2.2rem;
    }
    .text_img{
        width: 2.05rem;
        position: absolute;
        margin: auto;
        left: 0;
        right: 0;
        top: 0;
    }
    .phone_warp{
        display: none;
    }
    .contact_us {
        font-size: 0.2rem;
        position: absolute;
        margin: auto;
        width: 100%;
        text-align: center;
        bottom: -0.3rem;
    }
    .contact_us u {cursor: pointer;}
    .contact_us u:hover {color: #003399;}
    .footer {
        font-size: 0.14rem;
        position: absolute;
        margin: auto;
        width: 100%;
        text-align: center;
        bottom: -2rem;
    }
    .footer a {color: #000;}
    .footer a:hover {color: #003399;}
    .lang-switch {
        font-size: 0.2rem;
        position: absolute;
        right: 0.2rem;
        top: 0.1rem;
        cursor: pointer;
        text-decoration: underline;
    }

    @media screen and (max-width:750px){
        .pc_warp{
            display: none;
        }
        .phone_warp{
            display: block;
            width: 6.94rem;
            height: 7rem;
            position: absolute;
            margin: auto;
            left: 0;
            right: 0;
            top: 0;
            bottom: 0;
        }
        html,body{
            background: url('./image/phone_bg.jpg')no-repeat center;
            background-size: 100% 100%;
        }
        .phone_error_img{
            width: 4.65rem;
            position: absolute;
            margin: auto;
            left: 0;
            right: 0;
            top: 0;
        }
        .phone_logo_img{
            width: 2.88rem;
            position: absolute;
            margin: auto;
            left: 0;
            right: 0;
            bottom: 2.8rem;
        }
        .phone_text_img{
            width: 2.67rem;
            position: absolute;
            margin: auto;
            left: 0;
            right: 0;
            top: 0;
        }
        .contact_us {
            font-size: 0.3rem;
            position: absolute;
            margin: auto;
            width: 100%;
            text-align: center;
            bottom: -0.65rem;
        }
        .footer {
            font-size: 0.22rem;
            position: absolute;
            margin: auto;
            width: 100%;
            text-align: center;
            bottom: -1.4rem;
        }
        .app-form {font-size: 0.3rem;}
    }
</style>
<body onload="myload()">
    <div class="lang-switch"><span class="lang-cn" data-toggle>English</span><span class="lang-en" data-toggle>中文</span></div>

    <div class="pc_warp">
        <!--<img class="error_img" src="./image/404.png">-->
        <img class="logo_img" src="./image/logo.png">
        <img class="text_img" src="./image/text.png">
        <div class="contact_us"><u data-app-btn><span class="lang-cn">联系我们</span><span class="lang-en">Contact Us</span></u></div>
        <div class="footer">
            <span>Copyright ©Bai.com | <a href="http://beian.miit.gov.cn/" target="_blank">粤B2-20050580</a>
        </div>
    </div>

    <div class="phone_warp">
        <!--<img class="phone_error_img" src="./image/phone_404.png">-->
        <img class="phone_logo_img" src="./image/phone_logo.png">
        <img class="phone_text_img" src="./image/phone_text.png">
        <div class="contact_us"><u data-app-btn><span class="lang-cn">联系我们</span><span class="lang-en">Contact Us</span></u></div>
        <div class="footer">
            <span>Copyright ©Bai.com | <a href="http://beian.miit.gov.cn/" target="_blank">粤B2-20050580</a>
        </div>
    </div>
    <div class="app-form-mask hide">
        <div id="app-form" class="app-form">
            <div class="close-btn"></div>
            <p class="title"><span class="lang-cn">请填写并提交您的相关信息</span><span class="lang-en">Please fill in your information</span></p>
        <ul>
        <li class="clearfix">
            <div class="label"><label for="name"><span class="lang-cn">姓名：</span><span class="lang-en">Name: </span></label></div>
                <div class="field"><input name="name" class="input-text" type="text" placeholder="" /></div>
            </li>
            <li class="clearfix">
                <div class="label"><label for="phone_number"><span class="lang-cn">手机号：</span><span class="lang-en">Phone NO.: </span></label></div>
                <div class="field"><input name="phone_number" class="input-text" type="text" placeholder="" /></div>
            </li>
            <li class="clearfix">
                <div class="label"><label for="email"><span class="lang-cn">电子邮件：</span><span class="lang-en">Email: </span></label></div>
                <div class="field"><input name="email" class="input-text" type="text" placeholder="" /></div>
            </li>
            <li class="clearfix">
                <div class="label"><label for="wechat_id"><span class="lang-cn">微信号：</span><span class="lang-en">WhatsApp ID: </span></label></div>
                <div class="field"><input name="wechat_id" class="input-text" type="text" placeholder="" /></div>
            </li>
            <li class="clearfix" style="height: 175px;">
                <div class="label"><label for="remark"><span class="lang-cn">主题：</span><span class="lang-en">Subject: </span></label></div>
                <div class="field"><textarea name="remark" class="input-text" type="text" placeholder="请填下您的详细需求，以便我们和您及时联系。"></textarea></div>
            <
6c9
/li>
            <li class="clearfix">
                <div class="label"></div>
                <div class="field">
                    <input type="checkbox" name="agree" />
                    <span class="lang-cn">我已阅读并同意<a href="/privacy" target="_blank">隐私政策</a></span>
                    <span class="lang-en">I agree to the terms of <a href="/privacy" target="_blank">Privacy Policy</a></span>
                </div>
            </li>
            <li class="clearfix">
                <div class="label hide-small"><input type="hidden" name="siteid" value="910" /></div>
                <div class="field"><button type="button" class="input-btn" data-submit><span class="lang-cn">提交信息</span><span class="lang-en">Submit</span></button></div>
            </li>
            </ul>
        </div>
        <div id="app-result" class="app-form hide">
            <div class="close-btn"></div>
            <p class="title"><span class="lang-cn">提交成功，感谢您的申请！</span><span class="lang-en">Successfully submitted. Thanks for your application.</span></p>
            <p><span class="lang-cn">请添加以下微信与我们联系</span><span class="lang-en">Please add the following wechat work for further contact.</span></p>
            <div class="wechat-qrcode">
                <img src="https://parking.taoming.com/images/vip_qrcode.jpg" />
            </div>
            <p><span class="lang-cn">扫描以上二维码</span>Scan the qrcode<span class="lang-en"></span></p>
            <p><span class="lang-cn">或添加微信号</span><span class="lang-en">Or add wechat work by number:</span> 18520056026</p>
        </div>
    </div>
</body>
</html>

0

