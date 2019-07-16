import Vue from 'vue'
import { GenericSubscription, SelfSubscription, ModelSubscription } from './model_sockets/subscription'


const WSockets = {}

WSockets.install = function (Vue, options) {
    // Global list of subscription managers

    Vue.prototype.$ws = {
        generic: () => new GenericSubscription(arguments),
        self: () => new SelfSubscription(arguments),
        model: () => new ModelSubscription(arguments),
    }

    Vue.mixin({
        beforeDestroy() {
            if (typeof this.$store !== 'undefined') {
                this.$store.commit('ws/disconnect', this._uid)
            }
        },
        methods: {
            $genericWS({ url, debug = false, callback = null } = {}) {
                const sub = this.$ws.generic(url, debug)
                this.$store.commit('ws/register', {
                    uid: this._uid,
                    sub: sub
                })
                if (callback) {
                    sub.subscribe(callback)
                }
            },
            $selfWS({ signal = 'update', debug = false, callback = null } = {}) {
                const sub = this.$ws.self(signal, debug)
                this.$store.commit('ws/register', {
                    uid: this._uid,
                    sub: sub
                })
                if (callback) {
                    sub.subscribe(callback)
                }
            },
            $modelWS({ app, model, signal, debug = false, callback = null } = {}) {
                const sub = this.$ws.model(app, model, signal, debug)
                this.$store.commit('ws/register', {
                    uid: this._uid,
                    sub: sub
                })
                if (callback) {
                    sub.subscribe(callback)
                }
            }
        },
    })
}

Vue.use(WSockets)
