const clout = require('./clout.js');

(async () => {

    let plugins = await clout.find_plugins();

    let files = clout.files_in_dir('C:\\Users\\aElDi\\Desktop\\Clout\\');

    for (let file of files) {
        for (let plugin of plugins) {
            // console.log(plugin(file));
        }
    }

})()