<script>
    export default {
        props: {
            value: {
                type: Array,
                default: () => []
            }
        },
        data() {
            return {
                loading: false,
                selectedPage: 1,
                search: "",
                filter: null,
                pageSize: 10,
            }
        },
        computed: {
            fullList: {
                get() {
                    return this.value
                },
                set(value) {
                    this.$emit("input", value)
                }
            },
            list() {
                return []
            },
            listLength() {
                return 0
            }
        }
    }
</script>
