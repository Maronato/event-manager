<template>
    <Announcement v-if="show" :announcement="announcement" />
</template>
<script>
    import Announcement from "./Announcement"
    export default {
        components: { Announcement },
        computed: {
            announcement() {
                return this.$store.state.announcements.latest
            },
            show() {
                return this.announcement && Object.keys(this.announcement).length > 0
            }
        }
    }
</script>
