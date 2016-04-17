tinyMCEPopup.requireLangPack();

var InsertCodeDialog = {
    init: function () {
        document.forms[0].code.value = tinyMCEPopup.editor.selection.getContent({ format: 'text' });
    },

    insert: function () {

        var select = document.getElementById("languages");
        var language = select.options[select.selectedIndex].value;
        var code = document.forms[0].code.value;

        code = code.replace(/</g, "<");
        code = code.replace(/>/g, ">");

        if (language == "") {
            alert(document.getElementById("languagealert").value);
            return;
        }
        if (code.replace(/(^\s*)|(\s*$)/g, "") == "") {
            alert(document.getElementById("codealert").value);
            return;
        }

        code = code.replace(/&/g, "&amp;");
        code = code.replace(/</g, "&lt;");
        code = code.replace(/>/g, "&gt;");

        var html = "<div class=\'cnblogs_code\'><pre class=\"brush:" + language + ";";

        if (document.getElementById("collapse").checked == true) {
            html += "collapse:true;";
        }

        if (document.getElementById("show-line-number").checked == false) {
            html += "gutter:false;";
        }

        html += "\">" + code + "</pre></div>";

        tinyMCEPopup.editor.execCommand('mceInsertContent', false, html);
        tinyMCEPopup.close();
    }
};

tinyMCEPopup.onInit.add(InsertCodeDialog.init, InsertCodeDialog);
