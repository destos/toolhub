// webpack configuration for the angular-seed project using the
//angular-webpack-plugin.
var path = require('path');
var AngularPlugin = require('angular-webpack-plugin');

root = 'toolhub/static';

module.exports = {
    // The entrypoint module is 'toolhubApp' in angular module names, but is in the
    // app/js/app.js file - so we have an alias below.
    entry: 'toolhubApp',
    output: {
        path: root+'/js',
        filename: 'main.min.js'
    },
    resolve: {
        root: [
            // We want roots to resolve the app code:
            path.resolve(root, 'js'),
            // and the bower components:
            path.resolve(root, 'bower')],
        alias: {
            // This one first to match just the entrypoint module.
            // We only need this because the module name doesn't match the file name.
            toolhubApp$: 'toolhubApp/main',
            // This one maps all our modules called 'toolhubApp.something' to the app/js
            // directory
            toolhubApp: path.resolve(root, 'js'),
            // This is also needed because the module name doesn't match the file name
            // but we don't need to locate the file because it is a bower component
            // with a file name the same as the directory (component) name:
            //  bower_components/angular-route/angular-route
            // ngRoute$: 'angular-route'
            'ui.bootstrap$': 'angular-bootstrap/ui-bootstrap-tpls'
        }
    },
    plugins: [
        // The angular-webpack-plugin will:
        // - make the angular variable available by importing the 'angular' module
        //   whenever it is seen in the code.
        // - treat angular.module() dependencies as requires
        // - try to resolve modules using angular conventions.
        new AngularPlugin()
    ]
};
