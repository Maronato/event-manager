<template>
    <div class="createTeam">
        <div class="ui">
            <div class="title">
                Crie ou entre em uma equipe!
            </div>
            <div class="content">
                <p>
                    Digite o nome de uma equipe nova para criá-la ou o nome da equipe de seus amigos para entrar nela.
                </p>
                <input class="clean" placeholder="Nome da equipe"
                v-model="name"
                :error="nameTooBig"
                @keyup.enter="!nameTooBig ? createTeam() : ''">
            </div>
            <sui-button
            fluid
            positive
            content="Criar/Entrar!"
            :disabled="nameTooBig || creating"
            :loading="creating"
            @click="createTeam()"/>
        </div>
    </div>
</template>

<script>
    import axios from "project/js/axios_csrf";
    import toast from "project/js/notifications";

    export default {
        props: ['team_context'],
        data() {
            return {
                name: '',
                creating: false
            }
        },
        computed: {
            nameTooBig() {
                return this.name.length > 32 && this.name.length > 0
            }
        },
        methods: {
            createTeam() {
                this.creating = true
                axios.post(
                    this.team_context.api.create_team, {
                        name: this.name
                    }
                ).then(data => {
                    this.$emit('teamCreated', data.data)
                    this.creating = false
                }).catch(error => {
                    console.error(error.response)
                    toast("Opa!", "Equipe cheia, fechada ou inválida!", "error")
                    this.creating = false
                })
            }
        }
    }
</script>
<style scoped>
.createTeam {
    text-align: center;
}
.title {
    font-size: 1.5em;
    line-height: 1.5em;
    margin-bottom: 12px;
    text-transform: inherit;
    letter-spacing: inherit;
    font-family: inherit;
    font-weight: inherit;
}

.content {
    font-size: 1.1em;
}
input.clean {
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
input.clean:focus {
    outline: none;
}
button.button {
    max-width: 30em;
    font-size: 1.1em;
    text-transform: uppercase;
    font-weight: 700;
    padding: 0.7em 1em;
    margin: 8px auto;
    text-align: center;
}
</style>
