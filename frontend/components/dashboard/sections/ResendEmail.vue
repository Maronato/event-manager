<template>
    <div>
        <v-divider />
        <br />
        <p>Enviamos um email de confirmação para {{ $auth.user.email }}. Use-o para completar sua inscrição.</p>
        <p v-if="$auth.user.is_hacker">
            <b>Você tem até {{ reg_close }} para fazer isso</b>
        </p>
        <p>Não recebeu ou não é o seu email?</p>
        <v-form @submit.prevent="resendEmail()">
            <p v-if="errors.length">{{ errors }}</p>
            <v-flex
                xs12
                sm10
                md6
                offset-md3
                offset-sm1>
                <v-text-field
                    v-model="email"
                    solo
                    :error="!emailIsValid"
                    :error-messages="errorMessage"
                    type="email"
                    :loading="emailLoading"
                    :disabled="emailLoading"
                    placeholder="Digite seu email"
                    required
                />
            </v-flex>
            <v-btn
                :loading="emailLoading"
                :disabled="emailLoading || !emailIsValid"
                color="red"
                tile
                class="white--text"
                @click="resendEmail"
                v-text="`Reenviar email`"
            />
        </v-form>
        <br />
    </div>
</template>
<script>
    export default {
        data() {
            return {
                errors: "",
                emailLoading: false,
                typedEmail: null
            }
        },
        computed: {
            reg_close() {
                return this.$moment(
                    this.$store.state.settings.settings.registration_close_seconds
                ).calendar()
            },
            email: {
                get() {
                    if (this.typedEmail === null) return this.$auth.user.email
                    return this.typedEmail
                },
                set(email) {
                    this.typedEmail = email
                }
            },
            emailIsValid() {
                return this.validEmail(this.email)
            },
            errorMessage() {
                if (!this.emailIsValid) {
                    return 'Email inválido'
                }
                return ''
            }
        },
        methods: {
            resendEmail() {
                this.errors = ""
                this.emailLoading = true
                this.$auth
                    .request({
                        method: "post",
                        url: "api/profiles/change_email/",
                        data: {
                            email: this.email
                        }
                    })
                    .then(data => {
                        this.$toast("Enviado", data.message, "success")
                        this.emailLoading = false
                    })
                    .catch(error => {
                        this.$toast("Opa!", "Algo de errado aconteceu :(", "error")
                        this.emailLoading = false
                        return Promise.reject(error)
                    })
            },
            validEmail: function(email) {
                const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                return re.test(email)
            }
        }
    }
</script>
