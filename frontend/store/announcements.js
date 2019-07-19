export const state = () => ({
    list: [],
    latest: {}
})
export const mutations = {
    setList(state, list) {
        state.list = list
    },
    pushToList(state, obj) {
        state.list.push(obj)
    },
    sortList(state) {
        state.list.sort((a, b) => {
            return new Date(b.created) - new Date(a.created)
        })
    },
    setLatest(state) {
        state.latest = state.list[0] || null
    }
}

export const actions = {
    update({ commit }, list) {
        commit('setList', list)
        commit('sortList')
        commit('setLatest')
    },
    push({ commit }, announcement) {
        commit('pushToList', announcement)
        commit('sortList')
        commit('setLatest')
    }
}
