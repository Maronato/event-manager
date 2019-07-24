<template>
    <component
        :is="tableComponent"
        v-model="list"
        :identifier="_uid"
        :list-size.sync="listSize"
        :item-unique-key="itemUniqueKey"
        v-on="$listeners"
    />
</template>
<script>
    import ClientTable from "./ClientTable"
    import ServerTable from "./ServerTable"

    export default {
        components: { ClientTable, ServerTable },
        props: {
            listSizeThreshold: {
                type: Number,
                default: 250
            },
            value: {
                type: Array,
                default: () => []
            }
        },
        data() {
            return {
                listSize: 0,
                fullServerListSize: 0,
                itemUniqueKey: 'unique_id'
            }
        },
        computed: {
            list: {
                get() {
                    return this.value
                },
                set(value) {
                    this.$emit('input', value)
                }
            },
            tableComponent() {
                if (this.belowThreshold) {
                    return ClientTable
                }
                return ServerTable
            },
            belowThreshold() {
                return this.fullServerListSize <= this.listSizeThreshold
            }
        },
        mounted() {
            this.fetchList()
            this.listSub()
        },
        methods: {
            fetchList() {
                this.$auth
                    .request("/api/profiles/all/count/")
                    .then(response => {
                        this.listSize = response.count
                        this.fullServerListSize = response.count
                        let url = "/api/profiles/all/"
                        if (!this.belowThreshold) {
                            url += "?limit=" + 50
                        }
                        return this.$auth.request(url).then(response => {
                            if (this.belowThreshold) {
                                this.list = response
                            } else {
                                this.list = response.results
                            }
                        })
                    })
                    .catch(() => {
                        this.$toast(
                            "Opa!",
                            "Não conseguimos carregar a lista de usuários",
                            "error"
                        )
                    })
            },
            pushToList(object) {
                this.$eventBus.$emit("add-user-" + this._uid)
                this.fullServerListSize++
                if (this.belowThreshold) {
                    this.list.push(object)
                }
            },
            updateOnList(object) {
                this.$eventBus.$emit("update-user-" + this._uid)
                const idx = this.list.findIndex(
                    obj => obj[this.itemUniqueKey] === object[this.itemUniqueKey]
                )
                if (idx >= 0) {
                    this.list.splice(idx, 1, object)
                }
            },
            removeFromList(object) {
                this.$eventBus.$emit("remove-user" + this._uid)
                this.fullServerListSize--
                const idx = this.list.findIndex(
                    obj => obj[this.itemUniqueKey] === object[this.itemUniqueKey]
                )
                if (idx >= 0) {
                    this.list.splice(idx, 1)
                }
            },
            listSub() {
                this.$modelWS({
                    app: "user_profile",
                    model: "Profile",
                    signal: "create",
                    callback: this.pushToList
                })
                this.$modelWS({
                    app: "user_profile",
                    model: "Profile",
                    signal: "update",
                    callback: this.updateOnList
                })
                this.$modelWS({
                    app: "user_profile",
                    model: "Profile",
                    signal: "delete",
                    callback: this.removeFromList
                })
            }
        }
    }
</script>
