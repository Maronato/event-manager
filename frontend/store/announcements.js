export const state = () => ({
    list: [],
    latest: {}
})
export const mutations = {
    update(state, list) {
        list.sort((a, b) => {
            return new Date(b.created) - new Date(a.created)
        })
        state.list = list
        state.latest = list[0] || null
    },
    push(state, announcement) {
        state.list.push(announcement)
        state.list.sort((a, b) => {
            return new Date(b.created) - new Date(a.created)
        })
        state.latest = state.list[0] || null
    }
}

