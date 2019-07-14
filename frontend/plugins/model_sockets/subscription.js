import WebSocketBridge from "./ws_wrapper";

const globalSockets = {}

export class BaseSubscription {
    constructor(url, debug) {
        this.listeners = [];
        this.debug = false;
        if (debug !== "undefined") this.debug = debug;
        this.url = url.startsWith("http") ? url : process.env.baseURL + url;
        this.webSocketBridge = new WebSocketBridge();
        this.connected = false;
        this.allowSend = true;
    }

    connect() {
        if (this.connected) return
        if (this.debug) console.debug("Connecting");
        this.webSocketBridge.connect(this.url);
        const self = this;
        this.webSocketBridge.listen(function(action, stream) {
            self.onmessage(action);
        });
        if (this.debug) console.debug("Connected");
        this.connected = true;
    }

    onmessage(action) {
        if (this.debug) console.debug("Message received");
        for (const listener in this.listeners) {
            this.listeners[listener](action);
        }
    }

    subscribe(callback) {
        if (!this.connected) {
            console.error(
                "Can't subscribe, websocket disconnected! Call .connect()"
            );
            return;
        }
        this.listeners.push(callback);
        if (this.debug) console.debug("Subscribed to " + this.url);
    }

    unsubscribe(callback) {
        this.listeners.splice(this.listeners.indexOf(callback), 1);
        if (this.debug) console.debug("Unsubscribed from " + this.url);
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
        if (this.debug) console.debug("Payload send to " + this.url);
    }

    disconnect() {
        this.webSocketBridge.close();
        if (this.debug) console.debug("Disconnected");
        this.connected = false;
    }
}

function getOrCreate(url, debug) {
    if (globalSockets[url]) {
        if (debug) console.debug("Connecting to exisitng Socket");
        return globalSockets[url]
    } else {
        if (debug) console.debug("Creating new Socket");
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
        this.url = url.startsWith("http") ? url : process.env.baseURL + url;
        this.socketConnection = getOrCreate(url, debug);
        this.connected = false;
        this.allowSend = false;
        if (allowSend !== "undefined") this.allowSend = allowSend;
    }

    connect() {
        if (this.connected) return
        if (this.debug) console.debug("Connecting to socket");
        this.socketConnection.connect(this.url);
        const self = this;
        this.socketConnection.subscribe(function(action) {
            self.onmessage(action);
        });
        if (this.debug) console.debug("Connected to socket");
        this.connected = true;
    }

    onmessage(action) {
        if (this.debug) console.debug("Message received. Passing to socket");
        for (const listener in this.listeners) {
            if (action.signal_name === this.signal) {
                this.listeners[listener](action.data);
            }
        }
    }

    subscribe(callback) {
        if (!this.connected) {
            console.error(
                "Can't subscribe, websocket disconnected! Call .connect()"
            );
            return;
        }
        this.listeners.push(callback);
        if (this.debug) console.debug("Subscribed to " + this.url);
    }

    unsubscribe(callback) {
        this.listeners.splice(this.listeners.indexOf(callback), 1);
        if (this.debug) console.debug("Unsubscribed from " + this.url);
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
        if (this.debug) console.debug("Payload send to " + this.url);
    }

    disconnect() {
        this.socketConnection.unsubscribe(this.onmessage)
        if (this.debug) console.debug("Disconnected");
        this.connected = false;
    }
}

export class ModelSubscription extends SubscriptionManager {
    constructor(app, model, signal, debug) {
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
    constructor(signal, debug) {
        const url = "/ws/subscriptions/instances/me/" + signal + "/";
        super(url, debug, false, signal);
    }
}

export class GenericSubscription extends SubscriptionManager {
    constructor(url, debug) {
        super(url, debug, true);
    }
}
