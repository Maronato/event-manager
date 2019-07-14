<template>
    <div class="viewTeam">
        <div class="ui">
            <div class="title">
                <b>{{ team.name }}</b>
            </div>
            <div id="teammates_anchor">
                <p v-for="member in team.members">
                    {{ member }}
                </p>
            </div>
            <sui-divider />
            <div class="content">
                <sui-checkbox label="Atualizar em tempo real" toggle v-model="receiveUpdates"/>
                <br>
                <br>
                <div class="subtitle">Descreva seu projeto</div>
                <textarea class="clean" placeholder="Nosso projeto faz isso e aquilo..."
                v-model="description"
                :error="descriptionTooBig"
                rows="5"
                @keyup="receiveUpdates = false"/>
                <br>
                <div class="subtitle">Onde vocês estão?</div>
                <sui-input placeholder="Mesa 42 / Perto da saída"
                v-model="location"
                :error="locationTooBig"
                @keyup="receiveUpdates = false"/>
                <br>
                <div class="subtitle">URL do projeto no GitHub</div>
                <sui-input type="url" placeholder="https://github.com/equipe/projeto/"
                v-model="project_url"
                :error="urlTooBig"
                @keyup="receiveUpdates = false"/>
                <br>
                <br>
                <sui-checkbox label="Permitir a entrada de novos membros?" toggle v-model="allowNew"
                @click="receiveUpdates = false"/>
                <br>
                <br>
            </div>
            <sui-button
            fluid
            positive
            content="Salvar"
            :disabled="descriptionTooBig || saving || locationTooBig || urlTooBig"
            :loading="saving"
            @click="saveChanges()"/>
            <sui-divider />
            <sui-button
            fluid
            negative
            content="Sair da equipe"
            :loading="saving"
            @click="leaveTeam()"/>
        </div>
    </div>
</template>

<script>
    import axios from "project/js/axios_csrf";
    import toast from "project/js/notifications";
    import swal from "sweetalert";

    export default {
        props: ['team', 'team_context'],
        data() {
            return {
                description: '',
                location: '',
                project_url: '',
                allowNew: true,
                saving: false,
                receiveUpdates: true,
                loaded: false
            }
        },
        computed: {
            descriptionTooBig() {
                return this.description.length > 256
            },
            locationTooBig() {
                return this.location.length > 32
            },
            urlTooBig() {
                let expr = /http(s)?:\/\/.?(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi
                let regex = new RegExp(expr)
                return this.project_url.length > 200 || (!this.project_url.match(regex) && this.project_url.length > 0)
            }
        },
        methods: {
            saveChanges() {
                this.saving = true
                axios.patch(
                    this.team_context.api.update_team + this.team.id + '/', {
                        description: this.description,
                        location: this.location,
                        project_url: this.project_url,
                        allow_new: this.allowNew
                    }
                    ).then(data => {
                        this.saving = false
                        this.receiveUpdates = true
                        toast("Pronto!", "Alterações salvas", "success")
                    }).catch(error => {
                        this.saving = false
                        console.error(error);
                        toast("Opa!", "Algo de errado aconteceu :(", "error")
                    })
                },
                leaveTeam() {
                    this.saving = true
                    swal({
                        title: 'Sair da equipe?',
                        text: 'Tem certeza de que deseja sair de ' + this.team.name + '?',
                        icon: "info",
                        buttons: ["Não", "Sair"]
                    }).then(keepGoing => {
                    // Ask if user wants to keep going or stop
                    if (keepGoing) {
                        axios.post(
                            this.team_context.api.leave_team
                            ).then(data => {
                                this.saving = false
                                this.receiveUpdates = false
                                this.$emit('leaveTeam')
                            }).catch(error => {
                                this.saving = false
                                console.error(error);
                                toast("Opa!", "Algo de errado aconteceu :(", "error")
                            })
                        } else {
                            this.saving = false
                        }
                    });
                }
            },
            watch: {
                team(n) {
                    this.description = n.description
                    this.location = n.location
                    this.project_url = n.project_url
                    this.allowNew = n.allow_new
                },
                receiveUpdates(n) {
                    this.$emit('receiveUpdates', n)
                }
            },
            mounted() {
                this.description = this.team.description
                this.location = this.team.location
                this.project_url = this.team.project_url
                this.allowNew = this.team.allow_new
            }
        }
    </script>
    <style>
    .viewTeam {
        text-align: center;
    }
    .viewTeam .title {
        font-size: 1.5em;
        line-height: 1.5em;
        margin-bottom: 12px;
        text-transform: inherit;
        letter-spacing: inherit;
        font-family: inherit;
        font-weight: inherit;
    }
    .viewTeam .subtitle {
        font-size: 1.2em;
        line-height: 1.2em;
        margin-top: 5px;
        text-transform: inherit;
        letter-spacing: inherit;
        font-family: inherit;
        font-weight: inherit;
    }

    .viewTeam .content {
        font-size: 1.1em;
    }
    .viewTeam .ui.input {
        width: 100%;
    }
    .viewTeam .ui.input > input, textarea {
        width: 100%;
        max-width: 30em;
        background: #fafafa;
        padding: 0.5em;
        font-size: 1em;
        border: none;
        border-bottom: 1px solid #c6c6c6;
        margin: 8px auto;
        text-align: center;
    }
    .viewTeam textarea {
        text-align: left;
    }
    .viewTeam .ui.input > input:focus, textarea:focus {
        outline: none;
    }
    .viewTeam button.button {
        max-width: 30em;
        font-size: 1.1em;
        text-transform: uppercase;
        font-weight: 700;
        padding: 0.7em 1em;
        margin: 8px auto;
        text-align: center;
    }
    .viewTeam .ui.divider {
        margin: 8px auto;
        text-align: center;
        max-width: 36em;
    }
</style>
