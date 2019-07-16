import Vue from 'vue'
import { GenericSubscription, SelfSubscription, ModelSubscription } from './model_sockets/subscription'


const WSockets = {}

WSockets.install = function (Vue, options) {
    // Global list of subscription managers

    Vue.prototype.$ws = {
        generic: function () {
            return new GenericSubscription(JSON.parse(JSON.stringify(arguments[0])))
        },
        self: function () {
            return new SelfSubscription(JSON.parse(JSON.stringify(arguments[0])))
        },
        model: function () {
            return new ModelSubscription(JSON.parse(JSON.stringify(arguments[0])))
        },
    }

    Vue.mixin({
        beforeDestroy() {
            if (typeof this.$store !== 'undefined') {
                this.$store.commit('ws/disconnect', this._uid)
            }
        },
        methods: {
            $genericWS({ url, debug = false, callback = null } = {}) {
                const sub = this.$ws.generic({ url: url, debug: debug })
                this.$store.commit('ws/register', {
                    uid: this._uid,
                    sub: sub
                })
                if (callback) {
                    sub.subscribe(callback)
                }
            },
            $selfWS({ signal = 'update', debug = false, callback = null } = {}) {
                const sub = this.$ws.self({ signal: signal, debug: debug })
                this.$store.commit('ws/register', {
                    uid: this._uid,
                    sub: sub
                })
                if (callback) {
                    sub.subscribe(callback)
                }
            },
            $modelWS({ app, model, signal, debug = false, callback = null } = {}) {
                const sub = this.$ws.model({ app: app, model: model, signal: signal, debug: debug })
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
