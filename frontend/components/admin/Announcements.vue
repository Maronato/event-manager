<template>
    <div>
        <br />
        <div class="small big-title mb-2">Anúncios</div>
        <h2 class="subtitle-1 font-weight-light text-xs-center mb-5">Aqui você pode criar anúncios que serão vistos por todos os usuários em todo o site</h2>
        <v-layout row wrap>
            <v-spacer></v-spacer>
            <v-flex xs12 md10 offset-md-1>
                <v-text-field
                    v-model="title"
                    placeholder="Meu anúncio"
                    label="Título do anúncio"/>
                <v-textarea v-model="text" placeholder="Texto do meu anúncio" label="Texto do anúncio (HTML e Markdown suportados)"></v-textarea>
                <v-select
                    v-model="level"
                    label="Tipo de anúncio"
                    :items="levelOptions"
                    placeholder="Selecione um tipo"
                    selection
                />
                <v-flex xs12 text-xs-center>
                    <v-btn
                        tile
                        class="white--text"
                        color="blue"
                        :loading="createLoading"
                        :disabled="createLoading || title.length == 0 || text.length == 0 || level.length == 0"
                        @click="createAnnouncement">Criar anúncio</v-btn>
                </v-flex>
                <br />
                <v-divider />
                <br />
                <Announcement
                    v-for="announcement in $store.state.announcements.list"
                    :key="announcement.id"
                    :announcement="announcement"
                    :allow-delete="true"
                />
            </v-flex>
            <v-spacer></v-spacer>
        </v-layout>
    </div>
</template>

<script>
    import Announcement from "../announcements/Announcement"

    export default {
        components: { Announcement },
        data() {
            return {
                levelOptions: [],
                createLoading: false,
                title: "",
                text: "",
                level: ""
            }
        },
        mounted: function() {
            this.getLevelOptions()
        },
        methods: {
            getLevelOptions() {
                this.$auth.request({
                    method: 'options',
                    url: '/api/announcements/'
                }).then(data => {
                    this.levelOptions = data.actions.POST.level.choices.map(
                        choice => {
                            return {
                                key: choice.value,
                                value: choice.value,
                                text: choice.display_name
                            }
                        }
                    )
                })
                    .catch(() => {
                        this.$toast("Opa!", "Algo de errado aconteceu :(", "error")
                    })
            },
            createAnnouncement() {
                this.createLoading = true
                this.$auth.request({
                    method: 'post',
                    url: '/api/announcements/',
                    data: {
                        title: this.title,
                        text: this.text,
                        level: this.level
                    }
                })
                    .then(data => {
                        this.title = ""
                        this.text = ""
                        this.level = ""
                    })
                    .catch(() => {
                        this.$toast("Opa!", "Algo de errado aconteceu :(", "error")
                    })
                    .then(() => {
                        this.createLoading = false
                    })
            },
        }
    }
</script>
