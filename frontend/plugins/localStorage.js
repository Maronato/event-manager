import createPersistedState from 'vuex-persistedstate'

export default ({ store }) => {
    window.onNuxtReady(() => {
        createPersistedState({
            key: 'vuex',
            paths: ['theme', 'reminders', 'announcements']
        })(store)
    })
}
