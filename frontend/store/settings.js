export const state = () => ({
    settings: {}
})
export const mutations = {
    set(state, settings) {
        state.settings = settings
    }
}
export const actions = {
    fetch({commit}) {
        return this.$auth.request('/api/settings/').then(response => {
            commit('set', response)
            return response
        }).catch(() => {
            commit('set', {})
        })
    }
}
