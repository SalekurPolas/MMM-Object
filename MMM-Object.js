'use strict';

Module.register('MMM-Object', {
	defaults: {
		model: 'modules/MMM-Object/efficientdet_lite0.tflite',
		userName: 'loading'
	},

	getDom: function() {
		var Wrapper = document.createElement("div");
		var UserName = document.createElement("span");
		UserName.innerHTML = this.config.userName;
		Wrapper.appendChild(UserName);
		return Wrapper;
	},
	getHeader: function() {
		return 'Detected Object';
	},
	notificationReceived: function(notification, payload, sender) {
		if (notification === 'DOM_OBJECTS_CREATED') {
		    this.sendSocketNotification("CONFIG", this.config);
		}
	},

	socketNotificationReceived: function(notification, payload) {
		if(notification === "OBJECT_DETECTED") {
			this.config.userName = "Detected: " + payload;
			this.updateDom();
		}
	},
});