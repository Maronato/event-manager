<template>
    <Table
        search
        filter
        :search-text.sync="search"
        :filter-text.sync="filter"
        :filter-options="options"
        :selected-page.sync="selectedPage"
        :list="list"
        :page-size.sync="pageSize"
        :list-length="listLength"
        :loading="loading"
        :item-unique-key="itemUniqueKey"
    >
        <template slot="table-header">
            <sui-table-header-cell>ID</sui-table-header-cell>
            <sui-table-header-cell>Nome</sui-table-header-cell>
            <sui-table-header-cell>Email</sui-table-header-cell>
            <sui-table-header-cell>Estado</sui-table-header-cell>
            <sui-table-header-cell>Atributos</sui-table-header-cell>
            <sui-table-header-cell></sui-table-header-cell>
        </template>
        <template v-slot:table-body="{ item }">
            <sui-table-cell>{{ item.unique_id }}</sui-table-cell>
            <sui-table-cell>
                <strong>{{ item.full_name }}</strong>
            </sui-table-cell>
            <sui-table-cell>{{ item.email }}</sui-table-cell>
            <sui-table-cell>
                <strong>{{ item.state | mapState }}</strong>
            </sui-table-cell>
            <sui-table-cell>
                <v-icon v-if="item.is_verified" size="large" color="green">fas fa-check</v-icon>
                <v-icon v-if="item.has_facebook" size="large" color="blue">fab fa-facebook</v-icon>
                <v-icon v-if="item.has_github" size="large" color="black">fab fa-github</v-icon>
                <v-icon v-if="item.has_google" size="large" color="red">fab fa-google</v-icon>
            </sui-table-cell>
            <sui-table-cell collapsing class="text-xs-right">
                <sui-button
                    class="actionbuttons"
                    size="tiny"
                    content="Hacker"
                    :class="{blue: item.is_hacker, basic: !item.is_hacker }"
                    @click="$emit('toggle-hacker', item)"
                />
                <sui-button
                    class="actionbuttons"
                    size="tiny"
                    content="Staff"
                    :class="{blue: item.is_staff, basic: !item.is_staff }"
                    @click="$emit('toggle-staff', item)"
                />
                <sui-button
                    class="actionbuttons"
                    size="tiny"
                    content="Admin"
                    :class="{blue: item.is_admin, basic: !item.is_admin }"
                    @click="$emit('toggle-admin', item)"
                />
                <br />
                <sui-button
                    class="actionbuttons"
                    size="tiny"
                    content="Mentor"
                    :class="{blue: item.is_mentor, basic: !item.is_mentor }"
                    @click="$emit('toggle-mentor', item)"
                />
                <sui-button
                    class="actionbuttons"
                    size="tiny"
                    color="red"
                    content="Apagar"
                    @click="$emit('delete-user', item)"
                />
            </sui-table-cell>
        </template>
    </Table>
</template>
<script>
    import Table from "~/components/generic/tables/Table"
    import BaseTableMixin from "~/components/generic/tables/BaseTableMixin"

    export default {
        components: { Table },
        filters: {
            mapState: function(state) {
                const map = {
                    unverified: "Não verificado",
                    verified: "Verificado",
                    incomplete: "Incompleto",
                    submitted: "Submetido",
                    late: "Atrasado",
                    declined: "Recusado",
                    admitted: "Admitido",
                    waitlist: "Fila de espera",
                    withdraw: "Desistente",
                    confirmed: "Confirmado",
                    checkedin: "Checkin"
                }
                return map[state]
            }
        },
        mixins: [BaseTableMixin],
        props: {
            itemUniqueKey: {
                type: String,
                default: 'id'
            }
        },
        data() {
            return {
                options: [
                    {
                        text: "Todos",
                        key: "Todos",
                        label: { color: "red", empty: true, circular: true },
                        value: "all"
                    },
                    {
                        text: "Hacker",
                        key: "Hacker",
                        label: { color: "blue", empty: true, circular: true },
                        value: "is_hacker"
                    },
                    {
                        text: "Staff",
                        key: "Staff",
                        label: { color: "yellow", empty: true, circular: true },
                        value: "is_staff"
                    },
                    {
                        text: "Mentor",
                        key: "Mentor",
                        label: { color: "orange", empty: true, circular: true },
                        value: "is_mentor"
                    },
                    {
                        text: "Admin",
                        key: "Admin",
                        label: { color: "green", empty: true, circular: true },
                        value: "is_admin"
                    }
                ]
            }
        }
    }
</script>
<style scoped>
    .actionbuttons {
        margin-top: 5px;
        margin-bottom: 5px;
        border-radius: 0.28571429rem;
    }
</style>
