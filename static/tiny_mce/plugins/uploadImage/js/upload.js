tinyMCEPopup.requireLangPack();

var UploadDialog = {
    init: function () {
        //document.forms[0].code.value = tinyMCEPopup.editor.selection.getContent({ format: 'text' });
    },

    insert: function () {
        var html = "<p><img " +
            "width=\"" + document.getElementById('spUploadWidth').innerText + "\" " +
            "height=\"" + document.getElementById('spUploadHeight').innerText + "\" class=\"lazy\" " +
            "src=\"/media/" + document.getElementById('spUploadImgUrl').innerText +
            "\" alt=\"\" /></p>";

        tinyMCEPopup.editor.execCommand('mceInsertContent', false, html);
        tinyMCEPopup.close();
    }
};

tinyMCEPopup.onInit.add(UploadDialog.init, UploadDialog);
