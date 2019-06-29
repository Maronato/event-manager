import WebSocketBridge from "./ws_wrapper";

var global_sockets = {}

export class BaseSubscription {
    constructor(url, debug) {
        this.listeners = [];
        this.debug = false;
        if (debug !== "undefined") this.debug = debug;
        this.url = url;
        this.webSocketBridge = new WebSocketBridge();
        this.connected = false;
        this.allow_send = true;
    }
    connect() {
        if (this.connected) return
        if (this.debug) console.debug("Connecting");
        this.webSocketBridge.connect(this.url);
        var self = this;
        this.webSocketBridge.listen(function(action, stream) {
            self.onmessage(action);
        });
        if (this.debug) console.debug("Connected");
        this.connected = true;
    }
    onmessage(action) {
        if (this.debug) console.debug("Message received");
        for (let listener in this.listeners) {
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
        if (!this.allow_send) {
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

function get_or_create(url, debug) {
    if (global_sockets[url]) {
        if (debug) console.debug("Connecting to exisitng Socket");
        return global_sockets[url]
    } else {
        if (debug) console.debug("Creating new Socket");
        var newSocket = new BaseSubscription(url, debug);
        global_sockets[url] = newSocket;
        return newSocket;
    }
}

export class SubscriptionManager {
    constructor(url, debug, allow_send) {
        this.listeners = [];
        this.debug = false;
        if (debug !== "undefined") this.debug = debug;
        this.url = url;
        this.socketConnection = get_or_create(url, debug);
        this.connected = false;
        this.allow_send = false;
        if (allow_send !== "undefined") this.allow_send = allow_send;
    }
    connect() {
        if (this.connected) return
        if (this.debug) console.debug("Connecting to socket");
        this.socketConnection.connect(this.url);
        var self = this;
        this.socketConnection.subscribe(function(action) {
            self.onmessage(action);
        });
        if (this.debug) console.debug("Connected to socket");
        this.connected = true;
    }
    onmessage(action) {
        if (this.debug) console.debug("Message received. Passing to socket");
        for (let listener in this.listeners) {
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
        if (!this.allow_send) {
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
        var url =
            "/ws/subscriptions/models/" +
            app +
            "/" +
            model +
            "/" +
            signal +
            "/";
        super(url, debug);
    }
}

export class SelfSubscription extends SubscriptionManager {
    constructor(signal, debug) {
        var url = "/ws/subscriptions/instances/me/" + signal + "/";
        super(url, debug);
    }
}

export class GenericSubscription extends SubscriptionManager {
    constructor(url, debug) {
        super(url, debug, true);
    }
}
