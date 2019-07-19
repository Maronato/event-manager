<template>
    <div id="application" class="page">
        <div class="divided big-title">Aplicação</div>
        <v-form ref="form" v-model="valid" class="form">
            <div class="overline text-xs-center">* Obrigatório</div>
            <v-container>
                <div class="divided big-title">Informações Básicas</div>
                <v-layout wrap>
                    <v-flex xs12 md4>
                        <v-text-field
                            ref="first_name"
                            v-model="application.first_name"
                            :error-messages="manualErrors.first_name"
                            :rules="requiredRules"
                            label="Primeiro Nome*"
                            required
                            @change="clearManualError('first_name')"
                        ></v-text-field>
                    </v-flex>
                    <v-flex xs12 md4>
                        <v-text-field
                            ref="last_name"
                            v-model="application.last_name"
                            :error-messages="manualErrors.last_name"
                            :rules="requiredRules"
                            label="Sobrenome*"
                            required
                            @change="clearManualError('last_name')"
                        ></v-text-field>
                    </v-flex>
                    <v-flex xs12 md4>
                        <v-text-field
                            ref="age"
                            v-model="application.age"
                            :error-messages="manualErrors.age"
                            :rules="ageRules"
                            label="Idade*"
                            required
                            type="number"
                            @change="clearManualError('age')"
                        ></v-text-field>
                    </v-flex>

                    <v-flex xs12 md6>
                        <v-text-field
                            ref="email"
                            v-model="application.email"
                            :error-messages="manualErrors.email"
                            :rules="emailRules"
                            placeholder="seu@email.com"
                            label="Email*"
                            required
                            @change="clearManualError('email')"
                        ></v-text-field>
                    </v-flex>
                    <v-flex xs12 md6>
                        <v-text-field
                            ref="phone"
                            v-model="application.phone"
                            v-mask="phoneMask"
                            :error-messages="manualErrors.phone"
                            :rules="phoneRules"
                            placeholder="(99) 91234-5678"
                            label="Telefone (com DDD)*"
                            required
                            @change="clearManualError('phone')"
                        ></v-text-field>
                    </v-flex>

                    <v-flex xs12 md6>
                        <v-select
                            ref="gender"
                            v-model="application.gender"
                            :error-messages="manualErrors.gender"
                            :items="genderOptions"
                            :rules="requiredRules"
                            label="Gênero*"
                            required
                            @change="clearManualError('gender')"
                        />
                    </v-flex>
                    <v-flex xs12 md6>
                        <v-text-field
                            ref="cpf"
                            v-model="application.cpf"
                            v-mask="cpfMask"
                            :error-messages="manualErrors.cpf"
                            :rules="cpfRules"
                            placeholder="123.456.789-00"
                            label="CPF*"
                            required
                            @change="clearManualError('cpf')"
                        ></v-text-field>
                    </v-flex>
                </v-layout>
                <div class="divided big-title mt-4">Educação</div>
                <v-layout wrap>
                    <v-flex xs12 md6>
                        <v-select
                            ref="education"
                            v-model="application.education"
                            :error-messages="manualErrors.education"
                            :items="educationOptions"
                            :rules="requiredRules"
                            label="Educação*"
                            required
                            @change="clearManualError('education')"
                        />
                    </v-flex>
                    <v-flex xs12 md6>
                        <v-text-field
                            ref="enroll_year"
                            v-model="application.enroll_year"
                            v-mask="yearMask"
                            :error-messages="manualErrors.enroll_year"
                            :rules="yearRules"
                            placeholder="2018"
                            label="Ano de ingresso*"
                            required
                            @change="clearManualError('enroll_year')"
                        ></v-text-field>
                    </v-flex>
                    <v-flex v-if="higherEducation" xs12 md6>
                        <v-combobox
                            ref="school"
                            v-model="application.school"
                            :error-messages="manualErrors.school"
                            :items="schoolsOptions"
                            :rules="requiredRules"
                            label="Faculdade*"
                            hint="Não achou a sua? Digite o nome para criar!"
                            auto-select-first
                            required
                            :return-object="false"
                            @change="clearManualError('school')"
                        />
                    </v-flex>
                    <v-flex v-if="higherEducation" xs12 md6>
                        <v-combobox
                            ref="course"
                            v-model="application.course"
                            :error-messages="manualErrors.course"
                            :items="coursesOptions"
                            :rules="requiredRules"
                            label="Curso*"
                            hint="Não achou a sua? Digite o nome para criar!"
                            auto-select-first
                            required
                            :return-object="false"
                            @change="clearManualError('course')"
                        />
                    </v-flex>
                </v-layout>

                <div class="divided big-title mt-4">Currículo</div>
                <v-layout wrap>
                    <v-flex xs12 md6>
                        <v-select
                            ref="cv_type"
                            v-model="application.cv_type"
                            :error-messages="manualErrors.cv_type"
                            :items="cvTypes"
                            label="Tipo de currículo"
                            clearable
                            @change="clearCV()"
                        />
                    </v-flex>
                    <v-flex v-if="application.cv_type !== 'UP'" xs12 md6>
                        <v-text-field
                            v-if="application.cv_type"
                            ref="cv"
                            v-model="application.cv"
                            :error-messages="manualErrors.cv"
                            :rules="requiredRules"
                            :prefix="cvPrefix"
                            placeholder=" "
                            label="Currículo"
                            required
                            @change="clearManualError('cv')"
                        ></v-text-field>
                    </v-flex>
                    <v-flex v-else xs12 md6>
                        <v-file-input
                            ref="file_cv"
                            v-model="application.file_cv"
                            :error-messages="manualErrors.file_cv"
                            :rules="fileRules"
                            required
                            accept="application/pdf"
                            prepend-icon="fas fa-file-pdf"
                            label="Arquivo do seu currículo"
                            @change="clearManualError('file_cv')"
                        />
                    </v-flex>
                    <v-flex v-if="application.cv || application.file_cv" xs12 md6>
                        <v-select
                            ref="cv2_type"
                            v-model="application.cv2_type"
                            :error-messages="manualErrors.cv2_type"
                            :items="cv2Types"
                            label="Outro currículo"
                            clearable
                            @change="clearCV2()"
                        />
                    </v-flex>
                    <v-flex v-if="application.cv || application.file_cv" xs12 md6>
                        <v-text-field
                            v-if="application.cv2_type"
                            ref="cv2"
                            v-model="application.cv2"
                            :error-messages="manualErrors.cv2"
                            :rules="requiredRules"
                            :prefix="cv2Prefix"
                            placeholder=" "
                            required
                            label="Currículo"
                            @change="clearManualError('cv2')"
                        ></v-text-field>
                    </v-flex>
                </v-layout>

                <div class="divided big-title mt-4">Interesses</div>
                <v-layout wrap>
                    <v-flex xs12 md6>
                        <v-text-field
                            ref="dream_company"
                            v-model="application.dream_company"
                            :error-messages="manualErrors.dream_company"
                            label="Empresa dos sonhos"
                            @change="clearManualError('dream_company')"
                        />
                    </v-flex>
                    <v-flex xs12 md6>
                        <v-combobox
                            ref="interests"
                            v-model="interests"
                            :error-messages="manualErrors.interests"
                            label="Interesses"
                            :search-input.sync="interestsSearch"
                            placeholder="Consultoria, bancos, engenharia..."
                            multiple
                            small-chips
                            deletable-chips
                            @change="clearManualError('interests')"
                        >
                            <template
                                v-if="interestsSearch && interestsSearch.length > 2"
                                v-slot:no-data
                            >
                                <v-list-item>
                                    <v-list-item-content>
                                        <v-list-item-title>
                                            Aperte
                                            <kbd>enter</kbd> para adicionar
                                            <v-chip small>{{ interestsSearch }}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </template>
                        </v-combobox>
                    </v-flex>
                </v-layout>

                <div class="divided big-title mt-4">{{ eventName }}</div>
                <v-layout wrap>
                    <v-flex xs12 md6>
                        <v-text-field v-model="application.referrer" label="Como soube de nós?" placeholder="Amigos, Facebook, estrelas..." />
                    </v-flex>
                    <v-flex xs12 md6>
                        <v-checkbox v-model="application.first_timer" label="É a sua primeira vez?"></v-checkbox>
                    </v-flex>
                </v-layout>

                <div class="divided big-title mt-4">Nos conte mais</div>
                <p
                    class="text-xs-center"
                >Todos os campos abaixo são opcionais, mas recomendamos que você os preencha pois eles aumentam suas chances de conseguir um estágio/emprego!</p>
                <v-layout wrap>
                    <v-flex xs12 md4>
                        <v-autocomplete
                            ref="country"
                            v-model="application.country"
                            :error-messages="manualErrors.country"
                            :items="countryOptions"
                            label="País"
                            hint="Não achou a sua? Digite o nome para criar!"
                            auto-select-first
                            @change="clearManualError('country')"
                        />
                    </v-flex>
                    <v-flex xs12 md4>
                        <v-text-field
                            ref="state"
                            v-model="application.state"
                            :error-messages="manualErrors.state"
                            label="Estado"
                            @change="clearManualError('state')"
                        />
                    </v-flex>
                    <v-flex xs12 md4>
                        <v-text-field
                            ref="city"
                            v-model="application.city"
                            :error-messages="manualErrors.city"
                            label="Cidade"
                            @change="clearManualError('city')"
                        />
                    </v-flex>
                    <v-flex xs12 md6>
                        <v-checkbox
                            v-model="application.can_move"
                            label="Poderia se mudar pra trabalhar?"
                        ></v-checkbox>
                    </v-flex>
                    <v-flex xs12 md6>
                        <v-text-field
                            ref="time_slots"
                            v-model="application.time_slots"
                            :error-messages="manualErrors.time_slots"
                            label="Quais são os melhores horários pra você trabalhar?"
                            placeholder="De manhã nas quartas e à tarde no resto"
                            @change="clearManualError('time_slots')"
                        />
                    </v-flex>
                    <v-flex xs12 md4>
                        <v-select
                            ref="english_level"
                            v-model="application.english_level"
                            :error-messages="manualErrors.english_level"
                            :items="experienceOptions"
                            label="Nível de inglês"
                            required
                            @change="clearManualError('english_level')"
                        />
                    </v-flex>
                    <v-flex xs12 md4>
                        <v-text-field
                            ref="other_languages"
                            v-model="application.other_languages"
                            :error-messages="manualErrors.other_languages"
                            label="Que outras línguas você fala?"
                            placeholder="Dothraki básico, Klingon avançado"
                            @change="clearManualError('other_languages')"
                        />
                    </v-flex>
                    <v-flex xs12 md4>
                        <v-select
                            ref="excel_level"
                            v-model="application.excel_level"
                            :error-messages="manualErrors.excel_level"
                            :items="experienceOptions"
                            label="Nível de inglês"
                            required
                            @change="clearManualError('excel_level')"
                        />
                    </v-flex>
                    <v-flex xs12>
                        <v-textarea
                            ref="extra_courses"
                            v-model="application.extra_courses"
                            :error-messages="manualErrors.extra_courses"
                            label="Você tem algum curso ou experiência que considere relevante? Nos conte tudo!"
                            @change="clearManualError('extra_courses')"
                        ></v-textarea>
                    </v-flex>
                </v-layout>
                <v-container>
                    <v-divider class="my-5"></v-divider>
                    <v-layout
                        row
                        wrap
                        align-center
                        justify-center>
                        <v-flex xs12 text-xs-center>
                            <v-alert
                                v-show="!valid"
                                dense
                                type="info"
                            >Você ainda não preencheu todos os campos obrigatórios</v-alert>
                            <v-btn
                                :disabled="!valid"
                                :loading="loading"
                                x-large
                                block
                                rounded
                                color="blue"
                                class="white--text"
                                elevation="10"
                                @click="submitApplication"
                            >Enviar aplicação</v-btn>
                        </v-flex>
                    </v-layout>
                </v-container>
            </v-container>
        </v-form>
    </div>
</template>
<script>
    export default {
        head() {
            return { title: "Aplicação" }
        },
        data() {
            return {
                eventName: process.env.EVENT_NAME,
                valid: false,
                loading: false,
                interestsSearch: "",
                interests: [],
                educationOptions: [],
                schoolsOptions: [],
                coursesOptions: [],
                countryOptions: [],
                genderOptions: [
                    { text: "Masculino", value: "M" },
                    { text: "Feminino", value: "F" },
                    { text: "Outro", value: "O" },
                    { text: "Prefiro não dizer", value: "NA" }
                ],
                cvTypes: [
                    { text: "LinkedIn", value: "LI" },
                    { text: "GitHub", value: "GH" },
                    { text: "Upload de arquivo", value: "UP" },
                    { text: "Seu site", value: "WS" },
                    { text: "Outro", value: "OT" }
                ],
                experienceOptions: [
                    { value: "basic", text: "Básico" },
                    { value: "intermediate", text: "Intermediário" },
                    { value: "advanced", text: "Avançado" }
                ],

                requiredRules: [v => !!v || "Campo obrigatório"],
                emailRules: [
                    v => !!v || "Campo obrigatório",
                    v =>
                        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
                            v
                        ) || "Email inválido"
                ],
                ageRules: [
                    v => !!v || "Campo obrigatório",
                    v =>
                        parseInt(v) >= 18 ||
                        "Você deve ser maior de 18 para participar"
                ],
                phoneMask: "(##) #####-####",
                phoneRules: [
                    v => !!v || "Campo obrigatório",
                    v =>
                        /^\(?0?\d{2}\)?\s?\d{4,5}-?\s?\d{4}$/.test(v) ||
                        "Telefone inválido"
                ],
                cpfRules: [
                    v => !!v || "Campo obrigatório",
                    v =>
                        /^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$/.test(v) ||
                        "CPF inválido",
                    v => this.validateCPF(v) || "CPF inválido"
                ],
                cpfMask: "###.###.###-##",
                yearRules: [
                    v => !!v || "Campo obrigatório",
                    v =>
                        (parseInt(v) > this.$moment().year() - 50 &&
                        parseInt(v) <= this.$moment().year()) ||
                        "Ano inválido"
                ],
                yearMask: "####",
                fileRules: [
                    v => !!v || "Campo obrigatório",
                    v =>
                        (v || {}).type === "application/pdf" ||
                        "Arquivo deve ser um PDF",
                    v =>
                        (v || {}).size < 10485760 ||
                        "Arquivo deve ter menos que 10MB"
                ]
            }
        },
        computed: {
            higherEducation() {
                const ignore = ["Ensino Fundamental", "Ensino Médio"]
                return (
                    this.application.education &&
                    ignore.indexOf(this.application.education) < 0
                )
            },
            cvPrefix() {
                const map = {
                    LI: "linkedin.com/in/",
                    GH: "github.com/",
                    WS: "https://",
                    OT: "https://"
                }
                return map[this.application.cv_type] || ""
            },
            cv2Types() {
                return this.cvTypes.filter(t => t.value !== "UP")
            },
            cv2Prefix() {
                const map = {
                    LI: "linkedin.com/in/",
                    GH: "github.com/",
                    WS: "https://",
                    OT: "https://"
                }
                return map[this.application.cv2_type] || ""
            }
        },
        watch: {
            interests(n) {
                this.application.interests = n.join(" ")
            }
        },
        asyncData({ app }) {
            return app.$auth
                .request("/api/hackers/application/")
                .then(application => {
                    application.file_cv = null
                    return {
                        application: application,
                        manualErrors: Object.keys(application).reduce((res, field) => {
                            res[field] = []
                            return res
                        }, {})
                    }
                })
        },
        mounted() {
            // Rebuild interests
            this.interests =
                this.application.interests.length > 0
                    ? this.application.interests.split(" ")
                    : []
            // Rebuild cv urls
            this.application.cv = this.formatCVURL(this.application.cv, this.application.cv_type)
            this.application.cv2 = this.formatCVURL(this.application.cv2, this.application.cv2_type)
            // Load form options
            this.getFormOptions("education")
            this.getFormOptions("schools")
            this.getFormOptions("courses")
            this.getFormOptions("country")
        },
        methods: {
            getFormOptions(option) {
                return this.$auth
                    .request(
                        "/api/hackers/application/form_options/" + option + "/"
                    )
                    .then(response => {
                        this[option + "Options"] = response.results
                    })
                    .catch(error => {
                        this.$toast(
                            "Erro puxando dados",
                            "Algo de errado aconteceu!",
                            "error"
                        )
                        return Promise.reject(error)
                    })
            },
            validateCPF(cpf) {
                cpf = [
                    ...cpf
                        .split(".")
                        .join("")
                        .split("-")
                        .join("")
                ]
                let firstSum = 0
                let secondSum = 0
                cpf.forEach((number, i) => {
                    if (i < 9) {
                        firstSum += parseInt(number) * (10 - i)
                    }
                    if (i < 10) {
                        secondSum += parseInt(number) * (11 - i)
                    }
                })
                firstSum = ((firstSum * 10) % 11) % 10
                secondSum = ((secondSum * 10) % 11) % 10
                return (
                    firstSum === parseInt(cpf[9]) && secondSum === parseInt(cpf[10])
                )
            },
            clearCV() {
                this.clearManualError('cv_type')
                this.application.cv = ""
                this.application.file_cv = null
            },
            clearCV2() {
                this.clearManualError('cv2_type')
                this.application.cv2 = ""
            },
            formatCVURL(url, type) {
                if (!url) {
                    return ''
                }
                if (type === 'GH') {
                    return (new URL(url)).pathname.slice(1)
                }
                if (type === 'LI') {
                    return (new URL(url)).pathname.slice(4)
                }
                if (type === 'WS' || type === 'OT') {
                    const u = new URL(url)
                    return u.host + u.pathname
                }
                return ''
            },
            clearManualError(field) {
                console.log('clearing', field)
                while (this.manualErrors[field] && this.manualErrors[field].length > 0) {
                    this.manualErrors[field].splice(0, 1)
                }
            },
            submitApplication() {
                this.loading = true
                const data = new FormData();
                for (const key in this.application) {
                    if (this.application[key])
                        data.append(key, this.application[key])
                }
                this.$auth.request({
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    method: 'post',
                    url: '/api/hackers/application/',
                    data: data
                }).then(response => {
                    this.loading = false
                    this.$auth.redirect('home')
                }).catch(error => {
                    this.loading = false
                    const data = error.response.data
                    for (const field in data) {
                        for (const i in data[field]) {
                            this.manualErrors[field].push(data[field][i])
                        }
                    }
                    return Promise.reject(error)
                })
            }
        },
        permissions: args => {
            return args.app.$perms.application(args)
        }
    }
</script>
