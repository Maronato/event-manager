import WebSocketBridge from "./ws_wrapper";
const consola = require('consola')

const globalSockets = {}

export class BaseSubscription {
    constructor(url, debug) {
        this.listeners = [];
        this.debug = false;
        if (debug !== "undefined") this.debug = debug;
        this.url = url.startsWith("http") ? url : "ws://localhost:8000" + url;
        this.webSocketBridge = new WebSocketBridge();
        this.connected = false;
        this.allowSend = true;
    }

    connect() {
        if (this.connected) return
        if (this.debug) consola.log("Connecting");
        this.webSocketBridge.connect(this.url);
        const self = this;
        this.webSocketBridge.listen(function (action, stream) {
            self.onmessage(action);
        });
        if (this.debug) consola.log("Connected");
        this.connected = true;
    }

    onmessage(action) {
        if (this.debug) consola.log("Message received");
        for (const listener in this.listeners) {
            this.listeners[listener](action);
        }
    }

    subscribe(callback) {
        if (!this.connected) {
            this.connect()
        }
        this.listeners.push(callback);
        if (this.debug) consola.log("Subscribed to " + this.url);
    }

    unsubscribe(callback) {
        this.listeners.splice(this.listeners.indexOf(callback), 1);
        if (this.debug) consola.log("Unsubscribed from " + this.url);
        if (this.listeners.length === 0) {
            if (this.debug) consola.log("No listeners. Disconnecting from socket... ");
            this.disconnect()
        }
    }

    send(payload) {
        if (!this.allowSend) {
            console.error("This socket does not accept messages");
            return;
        }
        if (!this.connected) {
            console.error("Can't send messages to a disconnected socket");
            return;
        }
        this.webSocketBridge.send(payload);
        if (this.debug) consola.log("Payload send to " + this.url);
    }

    disconnect() {
        this.webSocketBridge.close();
        if (this.debug) consola.log("Disconnected");
        this.connected = false;
    }
}

function getOrCreate(url, debug) {
    if (globalSockets[url]) {
        if (debug) consola.log("Connecting to exisitng Socket");
        return globalSockets[url]
    } else {
        if (debug) consola.log("Creating new Socket");
        const newSocket = new BaseSubscription(url, debug);
        globalSockets[url] = newSocket;
        return newSocket;
    }
}

export class SubscriptionManager {
    constructor(url, debug, allowSend, signal) {
        this.listeners = [];
        this.signal = signal || 'universal';
        this.debug = debug || false;
        this.url = url.startsWith("http") ? url : "ws://localhost:8000" + url;
        this.socketConnection = getOrCreate(url, debug);
        this.connected = false;
        this.allowSend = false;
        if (allowSend !== "undefined") this.allowSend = allowSend;
    }

    connect() {
        if (this.connected) return
        if (this.debug) consola.log("Connecting to socket");
        this.socketConnection.connect(this.url);
        const self = this;
        this.socketConnection.subscribe(function (action) {
            self.onmessage(action);
        });
        if (this.debug) consola.log("Connected to socket");
        this.connected = true;
    }

    onmessage(action) {
        if (this.debug) consola.log("Message received. Passing to socket");
        for (const listener in this.listeners) {
            if (action.signal_name === this.signal) {
                this.listeners[listener](action.data);
            }
        }
    }

    subscribe(callback) {
        if (!this.connected) {
            this.connect()
        }
        this.listeners.push(callback);
        if (this.debug) consola.log("Subscribed to " + this.url);
    }

    unsubscribe(callback) {
        this.listeners.splice(this.listeners.indexOf(callback), 1);
        if (this.debug) consola.log("Unsubscribed from " + this.url);
        if (this.listeners.length === 0) {
            if (this.debug) consola.log("No listeners. Unsubscribing from socket connection... ");
            this.disconnect()
        }
    }

    send(payload) {
        if (!this.allowSend) {
            console.error("This socket does not accept messages");
            return;
        }
        if (!this.connected) {
            console.error("Can't send messages to a disconnected socket");
            return;
        }
        this.socketConnection.send(payload);
        if (this.debug) consola.log("Payload send to " + this.url);
    }

    disconnect() {
        this.socketConnection.unsubscribe(this.onmessage)
        if (this.debug) consola.log("Disconnected");
        this.connected = false;
    }
}

export class ModelSubscription extends SubscriptionManager {
    constructor({ app, model, signal, debug = false } = {}) {
        const url =
            "/ws/subscriptions/models/" +
            app +
            "/" +
            model +
            "/universal/";
        super(url, debug, false, signal);
    }
}

export class SelfSubscription extends SubscriptionManager {
    constructor({ signal = 'update', debug = false } = {}) {
        const url = "/ws/subscriptions/instances/me/" + signal + "/";
        super(url, debug, false, signal);
    }
}

export class GenericSubscription extends SubscriptionManager {
    constructor({ url, debug = false } = {}) {
        super(url, debug, true);
    }
}
