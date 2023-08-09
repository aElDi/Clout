const fs = require('node:fs');
const path = require('path')

async function find_plugins() {
    let PATH = './modules';
    let plugins = [];
    console.log('[Clout] Module scanning...');
    for (let file of fs.readdirSync(PATH)) {
        let plugin = await import(PATH + '/' + file);
        console.log(`[Clout] Imported module: ${plugin._meta.name}`);
        plugins.push(plugin.scan_file)
    };
    return plugins;
}

function files_in_dir(dir) {
    let data = fs.readdirSync(dir);
    let files = [];
    for (var point of data) {
        let url = path.join(dir, point)
        if (fs.lstatSync(url).isDirectory()) {
            files = files.concat(files_in_dir(url));
        }
        else {
            files.push(url);
        };
    };
    return files
}

module.exports = { find_plugins, files_in_dir };