'use strict';

const NodeHelper = require('node_helper');
const { PythonShell } = require('python-shell');
const onExit = require('signal-exit');
const shell = require('shelljs');
var pythonStarted = false;

module.exports = NodeHelper.create({
    pyshell: null,
    python_start: function() {
        const self = this;
        const options = {
            mode: 'json',
            stderrParser: line => JSON.stringify(line),
            args: [
                '--model=' + this.config.model
            ],
        };

        // Start object reco script
        self.pyshell = new PythonShell('modules/' + self.name + '/detect.py', options);

        self.pyshell.on('message', function(message) {
            if (message.hasOwnProperty('detected')) {
                console.log('[' + self.name + '] ' + message.detected.object);
		self.sendSocketNotification("OBJECT_DETECTED", message.detected.object);
            }
        });

        // Shutdown node helper
        self.pyshell.end(function(err) {
            if (err) throw err;
            console.log('[' + self.name + '] ' + 'finished running...');
        });

        onExit(function(code, signal) {
            self.destroy();
        });
    },

    python_stop: function() {
        this.destroy();
    },

    destroy: function() {
        console.log('[' + this.name + '] ' + 'Terminate python');
        this.pyshell.childProcess.kill();
    },

    stop: function() {
        pythonStarted = false;
        this.python_stop();
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === 'CONFIG') {
            this.config = payload;
            if (!pythonStarted) {
                pythonStarted = true;
                this.python_start();
            }
        }
    },
});