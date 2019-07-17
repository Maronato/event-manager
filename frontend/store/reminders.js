export const state = () => ({
    list: [
        {
            text: "RG",
            done: false
        },
        {
            text: 'RA',
            done: false
        }
    ]
})
export const mutations = {
    create(state, reminder) {
        state.list.push({
            text: reminder,
            done: false
        })
    },
    toggle(state, index) {
        state.list[index].done = !state.list[index].done
    },
    remove(state, index) {
        state.list.splice(index, 1)
    }
}

