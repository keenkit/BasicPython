(function () {
    tinymce.create('tinymce.plugins.insertCode', {
        init: function (ed, url) {
            ed.addCommand('mceInsertCode', function () {
                ed.windowManager.open({
                    file: url + '/insertcode.htm',
                    width: 600,
                    height: 480,
                    inline: 1
                }, {
                    plugin_url: url
                });
            });

            ed.addButton('insertcode', {
                title: 'insert code',
                cmd: 'mceInsertCode', 
                image: url + '/img/code.png'
            });
        },

        getInfo: function () {
            return {
                longname: 'insert code',
                author: 'Timothy',
                authorurl: 'http://www.susucms.com',
                infourl: 'http://www.susucms.com',
                version: '1.0'
            };
        }
    });

    tinymce.PluginManager.add('insertcode', tinymce.plugins.insertCode);
})();