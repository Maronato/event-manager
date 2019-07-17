<template>
    <v-alert
        v-model="alert"
        transition="fade-transition"
        :dismissible="allowDelete"
        :type="announcement.level"
        :icon="icon">
        <div class="headline font-weight-bold">{{ announcement.title }}</div>
        <p>{{ humanDate }}</p>
        <p>
            <VueMarkdown :source="announcement.text"></VueMarkdown>
        </p>
        <p class="float right">- {{ announcement.creator_name }}</p>
    </v-alert>
</template>

<script>
    import VueMarkdown from "vue-markdown"

    export default {
        components: { VueMarkdown },
        props: {
            announcement: {
                type: Object,
                default: () => ({})
            },
            allowDelete: {
                type: Boolean,
                default: false
            }
        },
        data() {
            return {
                alert: true
            }
        },
        computed: {
            icon() {
                const map = {
                    info: "fas fa-info fa-xs",
                    success: "fas fa-check-circle fa-xs",
                    warning: "fas fa-exclamation fa-xs",
                    error: "fas fa-exclamation-triangle fa-xs"
                }
                return map[this.announcement.level]
            },
            humanDate() {
                return this.$moment(this.announcement.created).calendar()
            }
        },
        watch: {
            alert(n) {
                if (!n) {
                    this.remove()
                }
            }
        },
        methods: {
            remove() {
                this.$auth.request({
                    method: 'delete',
                    url: '/api/announcements/' + this.announcement.id + '/'
                }).then(() => {
                    this.alert = true
                })
            }
        }
    }
</script>
