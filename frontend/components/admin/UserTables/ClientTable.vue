<script>
    import BaseTable from "./BaseTable"
    import ClientTableMixin from "~/components/generic/tables/ClientTableMixin"

    export default {
        extends: BaseTable,
        mixins: [ ClientTableMixin ],
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
                if (this.filter && this.filter !== "all") {
                    list = list.filter(object => object[this.filter])
                }
                return list
            }
        }
    }
</script>
