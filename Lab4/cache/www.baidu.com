HTTP/1.1 200 OK
Accept-Ranges: bytes
Cache-Control: no-cache
Content-Length: 29306
Content-Type: text/html
Date: Sun, 24 Nov 2024 03:01:44 GMT
P3p: CP=" OTI DSP COR IVA OUR IND COM "
P3p: CP=" OTI DSP COR IVA OUR IND COM "
Pragma: no-cache
Server: BWS/1.1
Set-Cookie: BAIDUID=84666868B6F1819DB3F285205B3AAAA7:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BIDUPSID=84666868B6F1819DB3F285205B3AAAA7; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: PSTM=1732417304; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com
Set-Cookie: BAIDUID=84666868B6F1819D289DA742B624B3F9:FG=1; max-age=31536000; expires=Mon, 24-Nov-25 03:01:44 GMT; domain=.baidu.com; path=/; version=1; comment=bd
Traceid: 1732417304243026407410484407224064035423
Vary: Accept-Encoding
X-Ua-Compatible: IE=Edge,chrome=1
X-Xss-Protection: 1;mode=block
Connection: close

<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <meta content="always" name="referrer" />
    <meta
        name="description"
        content="全球领先的中文搜索引擎、致力于让网民更便捷地获取信息，找到所求。百度超过千亿的中文网页数据库，可以瞬间找到相关的搜索结果。"
    />
    <link rel="shortcut icon" href="//www.baidu.com/favicon.ico" type="image/x-icon" />
    <link
        rel="search"
        type="application/opensearchdescription+xml"
        href="//www.baidu.com/content-search.xml"
        title="百度搜索"
    />
    <title>百度一下，你就知道</title>
    <style type="text/css">
        body {
            margin: 0;
            padding: 0;
            text-align: center;
            background: #fff;
            height: 100%;
        }

        html {
            overflow-y: auto;
            color: #000;
            overflow: -moz-scrollbars;
            height: 100%;
        }

        body, input {
            font-size: 12px;
            font-family: "PingFang SC", Arial, "Microsoft YaHei", sans-serif;
        }

        a {
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        img {
            border: 0;
            -ms-interpolation-mode: bicubic;
        }

        input {
            font-size: 100%;
            border: 0;
        }

        body, form {
            position: relative;
            z-index: 0;
        }

        #wrapper {
            height: 100%;
        }

        #head .s-ps-islite {
            _padding-bottom: 370px;
        }

        #head_wrapper.s-ps-islite {
            padding-bottom: 370px;
        }

        #head_wrapper.s-ps-islite .s_form {
            position: relative;
            z-index: 1;
        }

        #head_wrapper.s-ps-islite .fm {
            position: absolute;
            bottom: 0;
        }

        #head_wrapper.s-ps-islite .s-p-top {
            position: absolute;
            bottom: 40px;
            width: 100%;
            height: 181px;
        }

        #head_wrapper.s-ps-islite #s_lg_img {
            position: static;
            margin: 33px auto 0 auto;
            left: 50%;
        }

        #form {
            z-index: 1;
        }

        .s_form_wrapper {
            height: 100%;
        }

        #lh {
            margin: 16px 0 5px;
            word-spacing: 3px;
        }

        .c-font-normal {
            font: 13px/23px Arial, sans-serif;
        }

        .c-color-t {
            color: #222;
        }

        .c-btn,
        .c-btn:visited {
            color: #333 !important;
        }

        .c-btn {
            display: inline-block;
            overflow: hidden;
            font-family: inherit;
            font-weight: 400;
            text-align: center;
            vertical-align: middle;
            outline: 0;
            border: 0;
            height: 30px;
            width: 80px;
            line-height: 30px;
            font-size: 13px;
            border-radius: 6px;
            padding: 0;
            background-color: #f5f5f6;
            *zoom: 1;
            cursor: pointer;
        }

        .c-btn:hover {
            background-color: #315efb;
            color: #fff !important;
        }

        a.c-btn {
            text-decoration: none;
        }
        .c-btn-mini {
            height: 24px;
            width: 48px;
            line-height: 24px;
        }

        .c-btn-primary,
        .c-btn-primary:visited {
            color: #fff !important;
        }

        .c-btn-primary {
            background-color: #4e6ef2;
        }

        .c-btn-primary:hover {
            background-color: #315efb;
        }

        a:active {
            color: #f60;
        }

        #wrapper {
            position: relative;
            min-height: 100%;
        }

        #head {
            padding-bottom: 100px;
            text-align: center;
            *z-index: 1;
        }

        #wrapper {
            min-width: 1250px;
            height: 100%;
            min-height: 600px;
        }

        #head {
            position: relative;
            padding-bottom: 0;
            height: 100%;
            min-height: 600px;
        }

        .s_form_wrapper {
            height: 100%;
        }

        .quickdelete-wrap {
            position: relative;
        }

        .tools {
            position: absolute;
            right: -75px;
        }

        .s-isindex-wrap {
            position: relative;
        }

        #head_wrapper.head_wrapper {
            width: auto;
        }

        #head_wrapper {
            position: relative;
            height: 30%;
            min-height: 314px;
            max-height: 510px;
            width: 1000px;
            margin: 0 auto;
        }

        #head_wrapper .s-p-top {
            height: 60%;
            min-height: 185px;
            max-height: 310px;
            position: relative;
            z-index: 0;
            text-align: center;
        }

        #head_wrapper input {
            outline: 0;
            -webkit-appearance: none;
        }

        #head_wrapper .s_btn_wr,
        #head_wrapper .s_ipt_wr {
            display: inline-block;
            *display: inline;
            zoom: 1;
            background: 0 0;
            vertical-align: top;
            *vertical-align: middle;
        }

        #head_wrapper .s_ipt_wr {
            position: relative;
            width: 546px;
        }

        #head_wrapper .s_btn_wr {
            width: 108px;
            height: 44px;
            position: relative;
            z-index: 2;
        }

        #head_wrapper .s_ipt_wr:hover #kw {
            border-color: #a7aab5;
        }

        #head_wrapper #kw {
            width: 512px;
            height: 16px;
            padding: 12px 16px;
            font-size: 16px;
            margin: 0;
            vertical-align: top;
            outline: 0;
            box-shadow: none;
            border-radius: 10px 0 0 10px;
            border: 2px solid #c4c7ce;
            background: #fff;
            color: #222;
            overflow: hidden;
            box-sizing: content-box;
        }

        #head_wrapper #kw:focus {
            border-color: #4e6ef2 !important;
            opacity: 1;
            filter: alpha(opacity=100)\9
        }

        #head_wrapper .s_form {
            width: 654px;
            height: 100%;
            margin: 0 auto;
            text-align: left;
            z-index: 100;
        }

        #head_wrapper .s_btn {
            cursor: pointer;
            width: 108px;
            height: 44px;
            line-height: 45px;
            line-height: 44px\9;
            padding: 0;
            background: 0 0;
            background-color: #4e6ef2;
            border-radius: 0 10px 10px 0;
            font-size: 17px;
            color: #fff;
            box-shadow: none;
            font-weight: 400;
            border: none;
            outline: 0;
        }

        #head_wrapper .s_btn:hover {
            background-color: #4662d9;
        }

        #head_wrapper .s_btn:active {
            background-color: #4662d9;
        }

        #head_wrapper .quickdelete-wrap {
            position: relative;
        }

        #s_top_wrap {
            position: absolute;
            z-index: 99;
            min-width: 1000px;
            width: 100%;
        }

        #s-hotsearch-wrapper.s-hotsearch-wrapper {
            margin: 45px auto 0;
        }

        #s-hotsearch-wrapper .s-hotsearch-title {
            height: 24px;
            width: 100%;
        }

        #s-hotsearch-wrapper .s-hotsearch-title .title-text {
            float: left;
            user-select: none;
            color: #222;
            font: 14px / 24px Arial, sans-serif;
        }

        #s-hotsearch-wrapper .s-hotsearch-content {
            text-align: left;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .hotsearch-item .title-content-top-icon {
            display: none;
        }

        #s-hotsearch-wrapper
            .s-hotsearch-content
            .hotsearch-item[data-index='0']
            .title-content-index {
            display: none;
        }

        #s-hotsearch-wrapper
            .s-hotsearch-content
            .hotsearch-item[data-index='0']
            .title-content-top-icon {
            display: inline-block;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .hotsearch-item {
            width: 306px;
            float: left;
            height: 36px;
            line-height: 36px;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .hotsearch-item.odd {
            margin-right: 20px;
            clear: both;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .hotsearch-item.even {
            margin-left: 20px;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .title-content {
            display: block;
            float: left;
            height: 36px;
            line-height: 36px;
            font-size: 14px;
            width: 100%;
            color: #222;
            text-decoration: none;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .title-content:hover {
            color: #315efb;
            text-decoration: underline;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .tag-width {
            max-width: 282px;
            width: auto;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .title-content-top-icon {
            transform: rotate(180deg);
            height: 18px;
            width: 18px;
            display: inline-block;
            vertical-align: middle;
            line-height: 18px;
            position: relative;
            top: -2px;
            left: -3px;
            font-size: 18px;
            color: #f63051;
            margin-right: 8px;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .title-content-index {
            margin-right: 4px;
            width: 22px;
            font-family: Arial, sans-serif;
            font-size: 18px;
            line-height: 18px;
            position: relative;
            top: 1px;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .title-content-title {
            font-size: 16px;
        }

        #s-hotsearch-wrapper .s-hotsearch-content .title-content-mark {
            margin-left: 6px;
            position: relative;
            top: -2px;
            display: inline-block;
            padding: 0 2px;
            text-align: center;
            vertical-align: middle;
            font-style: normal;
            color: #fff;
            overflow: hidden;
            line-height: 16px;
            height: 16px;
            font-size: 12px;
            border-radius: 4px;
            font-weight: 200;
        }

        #s-hotsearch-wrapper .c-text-hot {
            background-color: #f60;
        }

        #s-hotsearch-wrapper .c-index-single {
            display: inline-block;
            background: 0 0;
            color: #9195a3;
            letter-spacing: -1px;
        }

        #s-hotsearch-wrapper .c-index-single-hot1 {
            color: #fe2d46;
        }

        #s-hotsearch-wrapper .c-index-single-hot2 {
            color: #f60;
        }

        #s-hotsearch-wrapper .c-index-single-hot3 {
            color: #faa90e;
        }

        #s-hotsearch-wrapper blockquote,
        body,
        button,
        dd,
        dl,
        dt,
        fieldset,
        form,
        h1,
        h2,
        h3,
        h4,
        h5,
        h6,
        hr,
        input,
        legend,
        li,
        ol,
        p,
        pre,
        td,
        textarea,
        th,
        ul {
            margin: 0;
            padding: 0;
        }

        #s-hotsearch-wrapper form,
        li,
        p,
        ul {
            list-style: none;
        }

        .c-icon {
            font-family: cIconfont !important;
            font-style: normal;
            -webkit-font-smoothing: antialiased;
        }

        .s-top-left {
            position: absolute;
            left: 0;
            top: 0;
            z-index: 100;
            height: 60px;
            padding-left: 24px;
        }

        .s-top-left .mnav {
            margin-right: 31px;
            margin-top: 19px;
            display: inline-block;
            position: relative;
        }

        .s-top-left .mnav:hover .s-bri,
        .s-top-left a:hover {
            color: #315efb;
            text-decoration: none;
        }

        .s-top-left .s-top-more-btn {
            padding-bottom: 19px;
        }

        .s-top-left .s-top-more-btn:hover .s-top-more {
            display: block;
        }

        .s-top-right {
            position: absolute;
            right: 0;
            top: 0;
            z-index: 100;
            height: 60px;
            padding-right: 24px;
        }

        .s-top-right .s-top-right-text {
            margin-left: 32px;
            margin-top: 19px;
            display: inline-block;
            position: relative;
            vertical-align: top;
            cursor: pointer;
        }

        .s-top-right .s-top-right-text:hover {
            color: #315efb;
        }

        .s-top-right .s-top-login-btn {
            display: inline-block;
            margin-top: 18px;
            margin-left: 32px;
            font-size: 13px;
        }

        .s-top-right a:hover {
            text-decoration: none;
        }

        #bottom_layer {
            width: 100%;
            position: fixed;
            z-index: 302;
            bottom: 0;
            left: 0;
            height: 39px;
            padding-top: 1px;
            overflow: hidden;
            zoom: 1;
            margin: 0;
            line-height: 39px;
            background: #fff;
        }

        #bottom_layer .lh {
            display: inline;
            margin-right: 20px;
        }

        #bottom_layer .lh:last-child {
            margin-left: -2px;
            margin-right: 0;
        }

        #bottom_layer .lh.activity {
            font-weight: 700;
            text-decoration: underline;
        }

        #bottom_layer a {
            font-size: 12px;
            text-decoration: none;
        }

        #bottom_layer .text-color {
            color: #bbb;
        }

        #bottom_layer a:hover {
            color: #222;
        }

        #bottom_layer .s-bottom-layer-content {
            text-align: center;
        }

        @font-face {
            font-family: cIconfont;
            src: url('https://pss.bdstatic.com/static/superman/font/iconfont-cdfecb8456.eot');
            src: url('https://pss.bdstatic.com/static/superman/font/iconfont-cdfecb8456.eot?#iefix')
                    format('embedded-opentype'),
                url('https://pss.bdstatic.com/static/superman/font/iconfont-fa013548a9.woff2')
                    format('woff2'),
                url('https://pss.bdstatic.com/static/superman/font/iconfont-840387fb42.woff')
                    format('woff'),
                url('https://pss.bdstatic.com/static/superman/font/iconfont-4530e108b6.ttf')
                    format('truetype'),
                url('https://pss.bdstatic.com/static/superman/font/iconfont-74fcdd51ab.svg#iconfont')
                    format('svg');
        }
    </style>
</head>
<body>
    <div id="wrapper" class="wrapper_new">
        <div id="head">
            <div id="s-top-left" class="s-top-left s-isindex-wrap">
                <a href="//news.baidu.com/" target="_blank" class="mnav c-font-normal c-color-t">新闻</a>
                <a href="//www.hao123.com/" target="_blank" class="mnav c-font-normal c-color-t">hao123</a>
                <a href="//map.baidu.com/" target="_blank" class="mnav c-font-normal c-color-t">地图</a>
                <a href="//live.baidu.com/" target="_blank" class="mnav c-font-normal c-color-t">直播</a>
                <a href="//haokan.baidu.com/?sfrom=baidu-top" target="_blank" class="mnav c-font-normal c-color-t">视频</a>
                <a href="//tieba.baidu.com/" target="_blank" class="mnav c-font-normal c-color-t">贴吧</a>
                <a href="//xueshu.baidu.com/" target="_blank" class="mnav c-font-normal c-color-t">学术</a>
                <div class="mnav s-top-more-btn">
                    <a href="//www.baidu.com/more/" name="tj_briicon" class="s-bri c-font-normal c-color-t" target="_blank">更多</a>
                </div>
            </div>
            <div id="u1" class="s-top-right s-isindex-wrap">
                <a
                    class="s-top-login-btn c-btn c-btn-primary c-btn-mini lb"
                    style="position:relative;overflow: visible;"
                    name="tj_login"
                    href="//www.baidu.com/bdorz/login.gif?login&amp;tpl=mn&amp;u=http%3A%2F%2Fwww.baidu.com%2f%3fbdorz_come%3d1"
                >登录</a>
            </div>
            <div id="head_wrapper" class="head_wrapper s-isindex-wrap s-ps-islite">
                <div class="s_form">
                    <div class="s_form_wrapper">
                        <div id="lg" class="s-p-top">
                            <img
                                hidefocus="true"
                                id="s_lg_img"
                                class="index-logo-src"
                                src="//www.baidu.com/img/flexible/logo/pc/index.png"
                                width="270"
                                height="129"
                                usemap="#mp"
                            />
                            <map name="mp">
                                <area
                                    style="outline: none"
                                    hidefocus="true"
                                    shape="rect"
                                    coords="0,0,270,129"
                                    href="//www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E7%83%AD%E6%90%9C&amp;sa=ire_dl_gh_logo_texing&amp;rsv_dl=igh_logo_pcs"
                                    target="_blank"
                                    title="点击一下，了解更多"
                                />
                            </map>
                        </div>
                        <a href="//www.baidu.com/" id="result_logo"></a>
                        <form id="form" name="f" action="//www.baidu.com/s" class="fm">
                            <input type="hidden" name="ie" value="utf-8" />
                            <input type="hidden" name="f" value="8" />
                            <input type="hidden" name="rsv_bp" value="1" />
                            <input type="hidden" name="rsv_idx" value="1" />
                            <input type="hidden" name="ch" value="" />
                            <input type="hidden" name="tn" value="baidu" />
                            <input type="hidden" name="bar" value="" />
                            <span class="s_ipt_wr quickdelete-wrap">
                                <input
                                    id="kw"
                                    name="wd"
                                    class="s_ipt"
                                    value=""
                                    maxlength="255"
                                    autocomplete="off"
                                /></span
                            ><span class="s_btn_wr">
                                <input
                                    type="submit"
                                    id="su"
                                    value="百度一下"
                                    class="bg s_btn"
                                />
                            </span>
                            <input type="hidden" name="rn" value="" />
                            <input type="hidden" name="fenlei" value="256" />
                            <input type="hidden" name="oq" value="" />
                            <input type="hidden" name="rsv_pq" value="b9ff093e0000e419" />
                            <input
                                type="hidden"
                                name="rsv_t"
                                value="3635FYbdbC8tlWmudZmYaUnaucNe+RzTzNEGqg/JuniQU10WL5mtMQehIrU"
                            />
                            <input type="hidden" name="rqlang" value="cn" />
                            <input type="hidden" name="rsv_enter" value="1" />
                            <input type="hidden" name="rsv_dl" value="ib" />
                        </form>
                    </div>
                    <div id="s-hotsearch-wrapper" class="s-hotsearch-wrapper">
                        <div class="s-hotsearch-title">
                            <a
                                href="https://top.baidu.com/board?platform=pc&amp;sa=pcindex_entry"
                                target="_blank"
                            >
                                <div
                                    class="title-text c-font-medium c-color-t"
                                    aria-label="百度热搜"
                                >
                                    <i class="c-icon"></i>
                                    <i class="c-icon arrow"></i>
                                </div>
                            </a>
                        </div>
                        <ul class="s-hotsearch-content" id="hotsearch-content-wrapper">
                            
<li class="hotsearch-item odd" data-index="0"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=%E4%B9%A0%E8%BF%91%E5%B9%B3%E5%BC%95%E9%A2%86%E6%9E%84%E5%BB%BA%E7%BD%91%E7%BB%9C%E7%A9%BA%E9%97%B4%E5%91%BD%E8%BF%90%E5%85%B1%E5%90%8C%E4%BD%93&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot0">0</span><span class="title-content-title">习近平引领构建网络空间命运共同体</span></a></li>
<li class="hotsearch-item even" data-index="5"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=%E6%95%85%E6%84%8F%E5%86%B2%E6%92%9E%E7%9F%B3%E5%B1%B1%E8%88%B0+17%E4%BA%BA%E8%A2%AB%E6%8A%93&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot5">5</span><span class="title-content-title">故意冲撞石山舰 17人被抓</span></a></li>
<li class="hotsearch-item odd" data-index="1"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=%E4%BF%9D%E6%97%B6%E6%8D%B7%E5%85%AC%E5%BC%80%E9%81%93%E6%AD%89&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot1">1</span><span class="title-content-title">保时捷公开道歉</span></a><span class="title-content-mark c-text-hot">热</span></li>
<li class="hotsearch-item even" data-index="6"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=%E4%BD%A0%E7%9A%84%E8%BA%AB%E4%BB%BD%E8%AF%81%E5%BF%AB%E5%88%B0%E6%9C%9F%E4%BA%86%E5%90%97&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot6">6</span><span class="title-content-title">你的身份证快到期了吗</span></a></li>
<li class="hotsearch-item odd" data-index="2"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=%E5%93%88%E5%B0%94%E6%BB%A8%E4%B8%AD%E5%A4%AE%E5%A4%A7%E8%A1%97%E9%93%BA%E4%B8%8A%E5%9C%B0%E6%AF%AF%E4%BA%86&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot2">2</span><span class="title-content-title">哈尔滨中央大街铺上地毯了</span></a><span class="title-content-mark c-text-hot">热</span></li>
<li class="hotsearch-item even" data-index="7"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=7%E4%B8%87%E4%BB%B6%E7%BE%BD%E7%BB%92%E6%9C%8D%E7%BB%8F%E6%9F%A5%E5%90%AB%E7%BB%92%E9%87%8F%E4%B8%BA0&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot7">7</span><span class="title-content-title">7万件羽绒服经查含绒量为0</span></a></li>
<li class="hotsearch-item odd" data-index="3"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=%E8%81%86%E5%90%AC%E5%A4%A7%E5%9B%BD%E5%A4%96%E4%BA%A4%E7%9A%84%E9%93%BF%E9%94%B5%E8%B6%B3%E9%9F%B3&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot3">3</span><span class="title-content-title">聆听大国外交的铿锵足音</span></a></li>
<li class="hotsearch-item even" data-index="8"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=%E7%8E%8B%E6%A5%9A%E9%92%A6%E8%AF%B4%E5%BC%A0%E6%9C%AC%E6%99%BA%E5%92%8C%E8%B5%A2%E5%BE%97%E5%BE%88%E7%8B%BC%E7%8B%88&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot8">8</span><span class="title-content-title">王楚钦说张本智和赢得很狼狈</span></a></li>
<li class="hotsearch-item odd" data-index="4"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=%E9%BB%84%E5%9C%A3%E4%BE%9D+%E6%AD%BB%E8%84%91%E5%BF%AB%E6%83%B3%E5%95%8A&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot4">4</span><span class="title-content-title">黄圣依 死脑快想啊</span></a></li>
<li class="hotsearch-item even" data-index="9"><a class="title-content tag-width" href="https://www.baidu.com/s?wd=9%E6%9D%A1%E5%85%B7%E4%BD%93%E6%8E%AA%E6%96%BD%E7%A8%B3%E5%A4%96%E8%B4%B8&sa=ipc_home_hotword_jt&rsv_dl=ipc_home_hotword_jt&from=super&cl=3&tn=baidutop10&fr=top1000&rsv_idx=2&hisfilter=1" target="_blank"><i class="c-icon title-content-top-icon"></i><span class="title-content-index c-index-single c-index-single-hot9">9</span><span class="title-content-title">9条具体措施稳外贸</span></a></li>
                        </ul>
                    </div>
                </div>
            </div>

            <div id="bottom_layer" class="s-bottom-layer s-isindex-wrap">
                <div class="s-bottom-layer-content">
                    <p class="lh"><a class="text-color" href="//home.baidu.com/" target="_blank">关于百度</a></p>
                    <p class="lh"><a class="text-color" href="//ir.baidu.com/" target="_blank">About Baidu</a></p>
                    <p class="lh"><a class="text-color" href="//www.baidu.com/duty" target="_blank">使用百度前必读</a>
                    </p>
                    <p class="lh"><a class="text-color" href="//help.baidu.com/" target="_blank">帮助中心</a></p>
                    <p class="lh"><a class="text-color"
                            href="//www.beian.gov.cn/portal/registerSystemInfo?recordcode=11000002000001"
                            target="_blank">京公网安备11000002000001号</a></p>
                    <p class="lh"><a class="text-color" href="//beian.miit.gov.cn/"
                            target="_blank">京ICP证030173号</a></p>
                    <p class="lh"><span id="year" class="text-color"><noscript>© Baidu</noscript></span></p>
                    <p class="lh"><span class="text-color">互联网药品信息服务资格证书 (京)-经营性-2017-0020</span></p>
                    <p class="lh"><a class="text-color" href="//www.baidu.com/licence/"
                            target="_blank">信息网络传播视听节目许可证 0110516</a></p>
                </div>
            </div>
        </div>
    </div>
    <script type="text/javascript">
        var date = new Date();
        var year = date.getFullYear();
        document.getElementById('year').innerText = '©' + year + ' Baidu ';
    </script>
</body>
</html>
