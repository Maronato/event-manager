export const state = () => ({
    registeredSockets: {}
})
export const mutations = {
    register(state, payload) {
        if (typeof state.registeredSockets[payload.uid] === 'undefined') {
            state.registeredSockets[payload.uid] = []
        }
        state.registeredSockets[payload.uid].push(payload.sub)
    },
    unregister(state, payload) {
        if (Array.isArray(state.registeredSockets[payload.uid])) {
            const idx = state.registeredSockets[payload.uid].findIndex(x => x === payload.sub)
            payload.sub.disconnect()
            state.registeredSockets[payload.uid].splice(idx, 1)
        }
    },
    disconnect(state, uid) {
        if (Array.isArray(state.registeredSockets[uid])) {
            state.registeredSockets[uid].forEach(sub => {
                sub.disconnect()
            })
            delete state.registeredSockets[uid]
        }
    }
}

