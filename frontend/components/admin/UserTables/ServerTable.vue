<script>
    import debounce from "lodash/debounce"
    import BaseTable from "./BaseTable"
    import ServerTableMixin from "~/components/generic/tables/ServerTableMixin"

    export default {
        extends: BaseTable,
        mixins: [ ServerTableMixin ],
        props: {
            identifier: {
                type: [Number, String],
                default: 0
            }
        },
        computed: {
            filteredList() {
                let list = [...this.fullList]
                if (this.search) {
                    list = list.filter(object => {
                        const byName =
                            object.full_name
                                .toLowerCase()
                                .indexOf(this.search.toLowerCase()) > -1
                        const byEmail =
                            object.email
                                .toLowerCase()
                                .indexOf(this.search.toLowerCase()) > -1
                        const byUID =
                            object.unique_id
                                .toLowerCase()
                                .indexOf(this.search.toLowerCase()) > -1
                        return byName || byEmail || byUID
                    })
                }
                if (this.filter && this.filter !== 'all') {
                    list = list.filter(object => object[this.filter])
                }
                return list.slice(0, this.pageSize)
            }
        },
        mounted() {
            this.$eventBus.$on("add-user-" + this.identifier, debounce(this.fetchList, 1000))
            this.$eventBus.$on("remove-user-" + this.identifier, () => {
                this.serverListLength--
            })
        },
        methods: {
            fetchList() {
                const urlParams = new URLSearchParams()
                urlParams.append("limit", this.pageSize)
                urlParams.append("offset", (this.selectedPage - 1) * this.pageSize)
                if (this.search.length) {
                    urlParams.append("search", this.search)
                }
                if (this.filter && this.filter !== "all") {
                    urlParams.append("filter", this.filter)
                }
                const url = "/api/profiles/all/?" + urlParams.toString()
                this.loading = true
                return this.$auth
                    .request(url)
                    .then(response => {
                        this.loading = false
                        this.serverListLength = response.count
                        this.fullList = response.results
                    })
                    .catch(() => {
                        this.loading = false
                        this.$toast(
                            "Opa!",
                            "Não conseguimos carregar a lista de usuários",
                            "error"
                        )
                    })
            }
        }
    }
</script>
