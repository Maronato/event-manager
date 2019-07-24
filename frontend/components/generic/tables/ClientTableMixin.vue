<script>
    export default {
        computed: {
            list() {
                return this.paginatedList
            },
            listLength() {
                return this.filteredList.length
            },
            // Pagination stuff
            paginatedList() {
                const objects = this.filteredList
                const lower = (this.selectedPage - 1) * this.pageSize
                const higher = Math.min(
                    this.selectedPage * this.pageSize - 1,
                    objects.length
                )
                return objects.slice(lower, higher)
            }
        }
    }
</script>
