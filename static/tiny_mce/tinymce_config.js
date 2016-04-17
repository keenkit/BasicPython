/**
 * Created by will on 15-3-8.
 */

var saveDraftIntervalId;
tinyMCE.init({
    selector : "textarea",
    language: "en",
    mode: "exact",
    elements: "id_content",
    width: "80%",
    height: 400,
    theme: "advanced",
	//template,emotions,layer
    plugins: "lists,spellchecker,pagebreak,style,layer,table,save,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template,insertcode,uploadImage",//syntaxHighlighter,uploadImage,",
    theme_advanced_buttons1: "forecolor,backcolor,|,bold,italic,underline,strikethrough,|,bullist,numlist,outdent,indent,blockquote,|,hr,sub,sup,charmap,|, justifyleft, justifycenter, justifyright,|,search,replace,|,insertdate,inserttime,preview",
	theme_advanced_buttons2: "link,unlink,anchor,|,removeformat,cleanup,|,image,uploadImage,media,|,insertcode,syntaxHighlighter,|,code,fullscreen,|,formatselect,fontselect,fontsizeselect,|,undo,redo, advimage", //
    theme_advanced_buttons3: "table,tablecontrols",
    theme_advanced_resizing: true,
    theme_advanced_resize_horizontal: false,
    theme_advanced_toolbar_location: "top",
    theme_advanced_toolbar_align: "left",
    theme_advanced_statusbar_location: "bottom",
    theme_advanced_fonts: "宋体=宋体;微软雅黑=Microsoft YaHei;黑体=黑体;仿宋=仿宋;楷体=楷体;隶书=隶书;幼圆=幼圆;Arial=arial,helvetica,sans-serif;Comic Sans MS=comic sans ms,sans-serif;Courier New=courier new,courier;Tahoma=tahoma,arial,helvetica,sans-serif;Times New Roman=times new roman,times;Verdana=verdana,geneva;Webdings=webdings;Wingdings=wingdings,zapf dingbats",
    theme_advanced_font_sizes: "12px=12px,13px=13px,14px=14px,15px=15px,16px=16px,18px=18px,4(14pt)=14pt,5(18pt)=18pt",
    forced_root_block: "p",
    convert_fonts_to_spans: true,
    remove_trailing_nbsp: true,
    convert_newlines_to_brs: false,
    force_br_newlines: false,
    force_p_newlines: true,
    remove_linebreaks: false,
    verify_html: true,
    convert_urls: true,
    relative_urls: false,
    remove_script_host: false,
    paste_auto_cleanup_on_paste: true,
    paste_preprocess: function (pl, o) {
        o.content = htmlFilter(o.content);
    },
    paste_postprocess: function (pl, o) {
        var content = o.node.innerHTML;
        content = content.replace(/<\/?span\s*>/gi, '');
        o.node.innerHTML = content;
    },
    extended_valid_elements: "pre[name|class],style",
	valid_children : "+body[style]",
	content_css: "/static/css/blog_mce.css",
    handle_event_callback: "MCECheckIndent",
    whitespace_elements: "pre,script,style,textarea,br",
    cleanup: true,
    setup: function (ed) {
        ed.onInit.add(function (editor) {
            var loadingText = "编辑器加载中...";
            var content = editor.getContent();
            if (content == loadingText || content == '<p>' + loadingText + '</p>') {
                editor.setContent('');
            }

        });
        if (window.navigator.userAgent.indexOf("MSIE ") > 0 &&
            window.navigator.userAgent.indexOf("MSIE 8") < 0) {
            try {
                document.execCommand("AutoUrlDetect", false, false);
            } catch (e) { }
        }
    }

});

function CustomSetupContent(editor_id, body, doc) {
	var loadingText = "编辑器加载中...";
    if (body.innerHTML == loadingText || body.innerHTML == '<p>'+loadingText+'</p>' || (body.inner.innerHTML < 30 && HTMLbody.innerHTML.indexOf(loadingText) >= 0)) {
        body.innerHTML = '';
    }
}


function MCECheckIndent(e) {
    if (e.type == 'keydown' && e.keyCode == 9) {
        tinyMCE.execCommand('mceInsertContent', false, '　　');
        try {
            return tinymce.dom.Event.cancel(e);
        }
        catch (e) {
            return false;
        }
    }
}

function InsertToEditor(content) {
    tinyMCE.execCommand('mceInsertContent', false, content);
}

function htmlFilter(content) {
    if (/style=".*?-webkit-text-stroke-width.*?"/gi.test(content)) {
        content = content.replace(/style="([^"]*)"/g, '');
    }
    var background_color_regex = /(style=".*?)background-color:[^;]+;(.*?")/gi;
    if (background_color_regex.test(content))
    {
        content = content.replace(background_color_regex, '$1$2');
    }
    return content;
}


