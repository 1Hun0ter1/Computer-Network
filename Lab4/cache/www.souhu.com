HTTP/1.1 200 OK
Server: nginx
Date: Sun, 24 Nov 2024 03:06:40 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: close
Vary: Accept-Encoding

d47
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width">
<title>souhu.com</title>
   <link rel="stylesheet" href="http://www.marksmile.com/asset/lp_style.css" >
</head>
<body>
<div class="main">
<a href="https://mail.365.com/login.html" target="_blank"><img src="/file/mail.png" width="100%" height="auto" alt="365邮箱" style="position: absolute;top:0;left:0;z-index: 1;"></a>
<div class="dm" ><h2 id="domain">souhu.com</h2></div>
<div class="bg"><div class="a"></div><div class="b"></div><div class="c"></div><div class="d"></div></div>
<!--//co-->
<div class="co">
<table align="center" border="0" cellpadding="0" cellspacing="0">
<tr><td align="left">域名托管商:<img src="file/marksmile 1.png" width="76" height="20" alt="名商网" style="position: absolute;margin-left: 7px;" /></td><td align="right" rowspan="4"><div class="wechat">微信客服:<em style="display: block;font-size: 10px;font-style: normal;">（请备注域名）</em><img class="wcode" width="60" height="60" src="http://www.marksmile.com/asset/lp_qrcode.png" id="myImage" /></div></td></tr>
<tr><td align="left"><div class="f14" style="position: relative;top: -5px;">Registrar Agent: <strong>Marksmile<sup>®</sup></strong></div></td></tr>
<tr><td align="left"><div class="f14" style="margin-top: 5px;">电子邮箱 / Email：</div></td></tr>
<tr><td align="left"><a href="mailto:service@marksmile.com"  class="email">service@marksmile.com</a ></td></tr>
</table>
</div>
<!--//about marksmile-->
<div class="cpy">&copy; 2023 <a href="https://www.marksmile.com/" target="_blank">marksmile.com</a ></div>
</div>
<style>
    #enlarged-image {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* 设置背景透明度为0.5 */
    display: flex;
    z-index: 1;
}
 
#enlarged-image img {
    display: block;
    margin: auto;
    max-width: none;
    max-height: none;
}
@media only screen and (max-width: 600px) {
    #enlarged-image img{
        width: 300px;
        height: 300px;
    }
}
</style>
<script src="https://lf6-cdn-tos.bytecdntp.com/cdn/expire-1-M/axios/0.26.0/axios.min.js" type="application/javascript"></script>
<script>
    var image = document.getElementById("myImage"); // 获取图
 
 // 创建并显示放大后的图片容器
 function createEnlargedContainer() {
     var container = document.createElement('div');
     container.id = "enlarged-image";
     
     var enlargedImg = document.createElement('img');
     enlargedImg.src = image.getAttribute('src');
     
     container.appendChild(enlargedImg);
     document.body.appendChild(container);
     container.addEventListener("click",removeEnlargedContainer);
 }
  
 // 移除放大后的图片容器
 function removeEnlargedContainer() {
     var container = document.getElementById("enlarged-image");
     if (container) {
         container.parentNode.removeChild(container);
     }
 }
  
 // 当图片被点击时调用该函数进行放大处理
 function handleClick() {
     createEnlargedContainer();
 }
  
 // 将点击事件绑定到图片上
 image.addEventListener('click', handleClick);
</script>
</body>
</html>
0

