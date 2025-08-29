import fs from 'fs';

export const buildManifest = (manifest, bundlePath) => {
    return Object.entries(manifest).reduce((manifestMap, manifestEntry) => {
        const [key, value] = manifestEntry;
        // console.log('\n'.padStart(220, '='), `key: ${key}\n`, `value: ${value}\n`, '\n'.padEnd(220, '='));

        if (key.endsWith('.map')) {
            return manifestMap;
        }

        let bundleKey;
        let [_, app, ext] = key.match(/(.*)\.(js|ts|tsx)/)!;
        // console.log('\n'.padStart(220, '='), `_: ${_}\napp: ${app}\next: ${ext}\n`, '\n'.padEnd(220, '='));
        if (['react-vendors', 'nlpssaVendor', 'nlpssaCommon'].includes(app)) {
            app = 'common';
            const bundle = key.includes('Common') ? 'common' : 'vendor';
            bundleKey = ext === 'js' || ext === 'ts' ? `${bundle}Js` : `${bundle}Css`;
        } else {
            bundleKey = ext === 'js' || ext === 'ts' ? 'appJs' : 'appCss';
        }

        if (!manifest.hasOwnProperty(app)) {
            manifestMap[app] = {};
        }

        manifestMap[app][bundleKey] = `${bundlePath}/${value}`;

        return manifestMap;
    }, {});
};

export const manifestMiddleware = (req, res, next) => {
    // TODO: should use CDN path from app-level config
    // const bundlePath = '/nlp-ssa/public';
    const bundlePath = '/dist/bundles';
    const manifestFromJson = JSON.parse(fs.readFileSync('./dist/bundles/assets-manifest.json', { encoding: 'utf-8' }));
    res.locals.manifest = buildManifest(manifestFromJson, bundlePath);
    next();
};
