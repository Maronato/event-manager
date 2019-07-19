export default function ({ store }) {
    return store.dispatch('settings/fetch')
}
