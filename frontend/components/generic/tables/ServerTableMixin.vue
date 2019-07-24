<script>
    import debounce from "lodash/debounce"

    export default {
        props: {
            listSize: {
                type: Number,
                default: 0
            }
        },
        computed: {
            serverListLength: {
                get() {
                    return this.listSize
                },
                set(value) {
                    this.$emit("update:listSize", value)
                }
            },
            list() {
                return this.filteredList
            },
            listLength() {
                return this.serverListLength
            }
        },
        watch: {
            search: debounce(function(){
                this.selectedPage = 1
                this.fetchList()
            }, 500),
            filter: debounce(function(){
                this.selectedPage = 1
                this.fetchList()
            }, 500),
            initialListSize(value) {
                this.serverListLength = this.serverListLength || value
            },
            pageSize: debounce(function(){
                this.selectedPage = 1
                this.fetchList()
            }, 500),
            selectedPage: debounce(function(){
                this.fetchList()
            }, 500),
        }
    }
</script>
