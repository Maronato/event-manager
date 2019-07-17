<template>
    <div>
        <v-divider />
        <br />
        <div class="header divided big-title">
            Lembretes
        </div>
        <p style="text-align: center;">
            Criamos um mini-app pra você não esquecer de levar nada!<br>
            Salvamos seus itens em cookies, então eles não serão sincronizados entre navegadores<br>
            Sinta-se livre pra usar durante o evento também 🙂
        </p>
        <v-container style="max-width: 500px">
            <v-text-field
                v-model="text"
                label="O que você não pode esquecer?"
                solo
                @keydown.enter="create">
                <v-fade-transition v-slot:append>
                    <v-icon v-if="text" @click="create">add_circle</v-icon>
                </v-fade-transition>
            </v-text-field>

            <v-divider class="mt-3"></v-divider>

            <v-layout my-1 align-center>
                <strong class="mx-3 info--text text--darken-3">Restantes: {{ remainingTasks }}</strong>

                <v-divider vertical></v-divider>

                <strong class="mx-3 black--text">Completos: {{ completedTasks }}</strong>

                <v-spacer></v-spacer>

                <v-progress-circular :value="progress" :color="color" class="mr-2"></v-progress-circular>
            </v-layout>

            <v-divider class="mb-3"></v-divider>

            <v-card v-if="tasks.length > 0">
                <v-slide-x-transition
                    class="py-0"
                    group
                    tag="v-list"
                    leave-absolute>
                    <template v-for="(task, i) in tasks">
                        <v-divider v-if="i !== 0" :key="`${i}-divider`"></v-divider>

                        <v-list-item :key="`${i}-${task.text}`">
                            <v-list-item-action>
                                <v-checkbox
                                    :input-value="task.done"
                                    color="info darken-3"
                                    @click.native="toggle(i)">
                                    <template v-slot:label>
                                        <div
                                            :class="task.done && 'grey--text' || 'text--primary'"
                                            class="ml-3"
                                            v-text="task.text"
                                        ></div>
                                    </template>
                                </v-checkbox>
                            </v-list-item-action>

                            <v-spacer></v-spacer>

                            <v-scroll-x-transition leave-absolute>
                                <v-icon v-if="task.done" color="success">check</v-icon>
                            </v-scroll-x-transition>
                            <v-scroll-x-transition leave-absolute>
                                <v-icon v-if="!task.done" color="red" @click="remove(i)">delete</v-icon>
                            </v-scroll-x-transition>
                        </v-list-item>
                    </template>
                </v-slide-x-transition>
            </v-card>
        </v-container>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                text: null
            }
        },
        computed: {
            completedTasks() {
                return this.tasks.filter(task => task.done).length
            },
            progress() {
                return (this.completedTasks / this.tasks.length) * 100
            },
            remainingTasks() {
                return this.tasks.length - this.completedTasks
            },
            tasks() {
                return this.$store.state.reminders.list
            },
            color() {
                if (this.progress <= 25) {
                    return 'red'
                } else if (this.progress <= 50) {
                    return 'orange'
                } else if (this.progress <= 75) {
                    return 'blue'
                } else {
                    return 'green'
                }
            }
        },
        methods: {
            toggle(index) {
                this.$store.commit('reminders/toggle', index)
            },
            remove(index) {
                this.$store.commit('reminders/remove', index)
            },
            create() {
                if (!this.text) return
                this.$store.commit('reminders/create', this.text)
                this.text = null
            }
        }
    }
</script>
