<template>
    <div>
        <v-divider />
        <br />
        <div class="header divided big-title">Identificação</div>
        <div class="description">Precisa se identificar? Mostre esse código!</div>
        <no-ssr>
            <v-layout align-center justify-center>
                <VueQRCodeComponent :size="size" :text="$auth.user.unique_id || ''" />
            </v-layout>
        </no-ssr>
        <br />
        <pre>Ou diga: {{ $auth.user.unique_id }}</pre>
        <br />
    </div>
</template>

<script>
    export default {
        data() {
            return {
                size: 250
            }
        }
    }
</script>
