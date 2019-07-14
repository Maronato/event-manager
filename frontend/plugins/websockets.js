import Vue from 'vue'
import { GenericSubscription, SelfSubscription, ModelSubscription } from './model_sockets/subscription'

const ws = {}

ws.install = function (Vue) {
    Vue.prototype.$ws = {
        generic: GenericSubscription,
        self: SelfSubscription,
        model: ModelSubscription,
    }
}

Vue.use(ws)
