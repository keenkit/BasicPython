
$(function(){

    var locked = false;
    var commentTips = {
        updating: "正在提交评论...",
        success: "评论成功，正在更新评论列表...",
        miss: "评论失败，请填写所有必填信息，谢谢你。",
        fail: "评论失败，请确保全部信息填写正确，谢谢你。",
        nochn: "评论失败，评论中必须包含中文！",
        notrobot: "评论失败，请点击\"我不是机器人\"按钮！",
        toofast: "评论别太快哦。。请先喝杯咖啡再说:)",
        internalError: "服务器出现错误，请尝试重新提交，谢谢你。",
        praiseOnlyOnce: "您已经给过赞了哦，谢谢支持！"
    };

    var commentHelper = {
        sp_comment_a: " <a href='网址'>网址</a> ",
        sp_comment_p: " <p>换行的文字</p> ",
        sp_comment_b: " <b>加粗的字</b> ",
        sp_comment_strong: " <strong>加粗的字</strong> ",
        sp_comment_pre: " <pre>您的代码</pre> "
    };

    // Crockford's supplant method (poor man's templating)
    if (!String.prototype.supplant) {
        String.prototype.supplant = function (o) {
            return this.replace(/{([^{}]*)}/g,
                function (a, b) {
                    var r = o[b];
                    return typeof r === 'string' || typeof r === 'number' ? r : a;
                }
            );
        };
    }
    String.prototype.replaceAll = function(s1,s2) {
        return this.replace(new RegExp(s1, "gm"), s2);
    }

    // Comment submit event
	$("#commentForm").ajaxForm({
		beforeSubmit: checkComment,
		success: dealResponse
	});

	$('div.reply').on('click', function() {
		var name = $.trim($(this).siblings('header').children('cite').text());
		var id = $.trim($(this).parents('li:first').attr('id'));
		var commentId = id.split('-')[1];

		$('form#commentform input[type=button]:last')
			.val('取消对' + name + '回应').show();
		$('html, body').scrollTop($('#commentform').offset().top);
		$('#id_reply_to_comment').val(commentId);
	});
	$('form#commentform input[type=button]:last').click(function() {
		var $hideId = $('#id_reply_to_comment');
		var commentId = $hideId.val();
		$hideId.val('');
		$(this).hide();
		//$('html, body').scrollTop($('#comment-'+commentId).offset().top);
	});


    // Comment API
    var uriGetComments = '/service/comments/'+ $('#article_id').val() +'/',
    $messageLength = $('#messageLength'),
    $commentList = $('#commentList'),
    rowTemplate = ' <li> \
                        <div class="commenterImage">    \
                            <span class="glyphicon glyphicon-user" aria-hidden="true"></span>   \
                            <span class="commenterUserName">{userName}</span>   \
                        </div>  \
                        <div class="commentText">   \
                            <p>{messageContent}</p><span class="date sub-text">on {created}</span> \
                        </div>  \
                    </li>';

    //http://blog.stevenlevithan.com/archives/date-time-format
    function formatComment(comment) {
        return $.extend(comment, {
           created : dateFormat(comment.created, "yyyy-mm-dd, h:MM:ss TT")
        });
    }

    // Comments
    function initComments() {
        $.getJSON(uriGetComments)
            .done(function (data) {
                $commentList.empty();
                $.each(data, function () {
                    var comment = formatComment(this);
                    $commentList.append(rowTemplate.supplant(comment));
                });
                $messageLength.text(data.length == 0 ? '没有评论' : data.length + '条评论:');
                prettyCode();
            });
    }

    function prettyCode() {
        $('pre').addClass('prettyprint linenums').attr('style', 'overflow:auto');
        prettyPrint();
    }

    // Evaluation
    // Evaluation API
    function initEvaluation(){
        var uriPost = '/service/evaluation/' + $('#article_id').val() + '/';
        var formData=$("#commentForm").serialize();
        formData = formData + '&type=view';
        $.post( uriPost,formData, function(data) {
            $('#spanThumbsUp').text(data.praiseCount);
            $('#spanEyeOpen').text(data.viewCount);
        });
    }

    // Load Announcement
    function initAnnouncement(){
        var uriAnn = '/service/announcement/';
        $.getJSON(uriAnn)
            .done(function (data) {
                if (data != null && data.announcement != "") {
                    $('.announcement').html(data.announcement + '<span id="sp_close_announcement">X</span>');
                    handle_announcement();

                    $('#sp_close_announcement').click(function () {
                        $.cookie('announcement-close', 'true', { expires: 2, path: '/' });
                        $('.announcement').slideUp();
                    })
                }
            });
    }

    function handle_announcement() {
        if ($.cookie('announcement-close') != null) {
            $('.announcement').slideUp();
        } else {
            $('.announcement').slideDown();
        }
    }

    // block invalid submit
    function block(msg) {
        $.blockUI({
            message: msg,
            css: {
                width: '350px',
                border: 'none',
                padding: '15px 5px',
                backgroundColor: '#000',
                '-webkit-border-radius': '3px',
                '-moz-border-radius': '3px',
                'border-radius': '3px',
                opacity: .6,
                color: '#fff' ,
                'font-weight': 'bold'
            }
        });
    }

    function checkComment(arr, $form, options) {
        if(locked)
            return false;

        for(itm in arr) {
            var obj = arr[itm];

            var name = obj.name;
            var value = obj.value;

            if(name == 'userName'|| name=='messageContent') {
                if(value == '' || typeof value == undefined) {
                    block(commentTips['miss']);
                    setTimeout($.unblockUI, 1500);
                    return false;
                }
            }
        }

        if(!locked)
            locked = true;
    }

    function dealResponse(responseText, statusText){
        block(commentTips['updating']);
        var uriPost = '/service/comments/' + $('#article_id').val() + '/';
        var formData=$("#commentForm").serialize();
        $.post( uriPost,formData, function(data) {

            if (data === '201') {
                block(commentTips['success']);
                initComments();
                $('#messageContent').val('');
                $('#commentReview').html('');
                $.unblockUI();
            } else if (data === '406') {
                block(commentTips['toofast']);
                setTimeout($.unblockUI, 1500);
            } else {
                block(commentTips['internalError']);
                setTimeout($.unblockUI, 1500);
            }
        });
        if(locked) locked = false;
    }
    // Animation for praise
    $('.glyphicon-thumbs-up').click(function(e) {
        var uriPost = '/service/evaluation/' + $('#article_id').val() + '/';
        var formData=$("#commentForm").serialize();
        formData = formData + '&type=praise';
        $.post( uriPost,formData, function(data) {
            if (data === '400') {
                block(commentTips['internalError']);
                setTimeout($.unblockUI, 1500);
                return

            } else if (data === '406') {
                block(commentTips['praiseOnlyOnce']);
                setTimeout($.unblockUI, 1500);
                return
            } else {
                $('#spanThumbsUp').text(data.praiseCount);

                var $i = $("<b>").text("+"+1);
                var x = e.pageX, y = e.pageY;
                $i.css({top:y-20,left:x,position:"absolute",color:"#E94F06"});
                $("body").append($i);
                $i.animate({top:y-180,opacity:0,"font-size":"1.4em"},1500,function(){
                    $i.remove();
                });
                e.stopPropagation();
            }
        });
	});

    //Html review function when comment
    $('#messageContent').keyup(function(e) {
        var xssComment = $('#messageContent').val().replace(/<script/g, '&lt;script').replace(/script>/g, 'script&gt;');
        $('#commentReview').html(xssComment);
    });

    $("#messageContent").bind('focus',function (){
        var time = setInterval( function(){ $('#commentReview').html($('#messageContent').val()); }, 1000);
        $(this).bind('blur',function(){
            clearInterval(time);      //失去焦点的时候清楚定时器
        });
    });

    $('.commentTips span').css('cursor','pointer').css('color', 'gray').css('font-weight','bold');
    $('.commentTips span').click(function() {
        var msg = $('#messageContent').val();
        msg = msg + commentHelper[this.id];
        $('#messageContent').val(msg);
    });



    // Page load Comments and Evaluations and Announcements
    if ($('#messageLength').length > 0 ) {
        initComments();
        initEvaluation();
    }
    initAnnouncement();
    prettyCode();



});
