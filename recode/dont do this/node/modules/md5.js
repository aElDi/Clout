
const _meta = {
    name: 'MD5 Scanner',
    short_name: 'md5',
    desc: 'Scan files by cache.chs file md5 caches',
};

function scan_file(filename){
    return [true, filename];
};

module.exports = {_meta, scan_file};