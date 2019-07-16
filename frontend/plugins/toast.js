import Vue from 'vue'
import iziToast from "izitoast";

function desktopNotify(message) {
    const title = process.env.EVENT_NAME
    const icon = "/img/logo.png"
    if (Notification.permission === "granted") {
        const notification = new Notification(title, {
            icon: icon,
            body: message
        });
        notification.onclick = function () {
            window.focus();
        };
    }
}

function toast(
    title,
    message,
    type = 'info',
    timeout = 5000,
    theme = "light",
    position = "topRight"
) {
    if (document && document.hidden) {
        desktopNotify(message);
    }
    return iziToast[type]({
        title: title,
        message: message,
        type: type,
        timeout: timeout,
        theme: theme,
        position: position
    });
}

const notify = {}

notify.install = function (Vue) {
    Vue.prototype.$toast = toast
    Vue.prototype.$izitoast = iziToast
}

Vue.use(notify)
