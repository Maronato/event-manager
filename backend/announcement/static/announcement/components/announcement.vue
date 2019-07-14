<template>
    <div>
        <transition name="fade">
            <div v-bind:class="announcement.level" class="ui message">
                <i v-if="allowDelete" @click="$emit('delete-announcement', announcement.id)" class="close icon"></i>
                <div class="header">
                    {{ announcement.title }}
                </div>
                <p>
                    {{ humanDate }}
                </p>
                <p>
                    <VueMarkdown :source="announcement.text"></VueMarkdown>
                </p>
                <p class="float right">
                    - {{ announcement.creator_name }}
                </p>
            </div>
        </transition>
    </div>
</template>

<script>
    import * as mome from "moment";
    import VueMarkdown from 'vue-markdown';
    import "moment/locale/pt-br";

    if ("default" in mome) {
        var moment = mome["default"];
    } else {
        var moment = mome;
    }

    moment.locale("pt-BR");

    export default {
        components: { VueMarkdown },
        props: ['announcement', 'allowDelete'],
        computed: {
            humanDate() {
                return moment(this.announcement.created).calendar();
            }
        }
    }
</script>
