<template>
    <div>
        <div class="ui form">
            <div class="fields">
                <slot name="search">
                    <div v-if="search" class="eleven wide field">
                        <div class="ui left icon fluid input">
                            <i class="search icon"></i>
                            <input
                                v-model="searchTextModel"
                                type="text"
                                class="searchText"
                                placeholder="Pesquisar por nome"
                            />
                        </div>
                    </div>
                </slot>
                <slot name="filter">
                    <div v-if="filter" class="five wide field">
                        <sui-dropdown
                            v-model="filterTextModel"
                            text="Filtrar"
                            icon="filter"
                            floating
                            labeled
                            button
                            fluid
                            class="icon"
                            :menu-header="{
                                icon: '',
                                content: 'Header',
                            }"
                            :options="filterOptions"
                        />
                    </div>
                </slot>
            </div>
        </div>
        <slot name="table">
            <sui-table striped tablet stackable>
                <sui-table-header full-width>
                    <sui-table-row>
                        <slot name="table-header"></slot>
                    </sui-table-row>
                </sui-table-header>
                <sui-table-header-cell v-if="loading" colspan="6">
                    <v-progress-linear
                        indeterminate
                        height="6"
                    ></v-progress-linear>
                </sui-table-header-cell>
                <sui-table-body>
                    <sui-table-row v-for="item in list" :key="item[itemUniqueKey]">
                        <slot name="table-body" :item="item"></slot>
                    </sui-table-row>
                </sui-table-body>
                <sui-table-footer full-width>
                    <sui-table-row>
                        <slot name="table-footer">
                            <sui-table-header-cell colspan="3">
                                <div class="ui left floated">
                                    <sui-dropdown
                                        v-model="pageSizeModel"
                                        selection
                                        :options="pageSizeOptions"
                                    />
                                </div>
                            </sui-table-header-cell>
                            <sui-table-header-cell colspan="3">
                                <div class="ui right floated pagination menu">
                                    <a
                                        v-for="page in pages"
                                        :key="page"
                                        class="item"
                                        :class="{active: page === selectedPage}"
                                        @click="$emit('update:selectedPage', page)"
                                    >{{ page }}</a>
                                </div>
                            </sui-table-header-cell>
                        </slot>
                    </sui-table-row>
                </sui-table-footer>
            </sui-table>
        </slot>
    </div>
</template>
<script>
    export default {
        props: {
            list: {
                type: Array,
                default: () => []
            },
            listLength: {
                type: Number,
                default: 0
            },
            filterOptions: {
                type: Array,
                default: () => []
            },
            searchText: {
                type: String,
                default: ""
            },
            filterText: {
                type: String,
                default: ""
            },
            search: Boolean,
            filter: Boolean,
            loading: Boolean,
            selectedPage: {
                type: Number,
                default: 1
            },
            pageSize: {
                type: Number,
                default: 10
            },
            itemUniqueKey: {
                type: String,
                default: 'id'
            }
        },
        data() {
            return {
                pageSizeOptions: [
                    { value: 10, text: "10" },
                    { value: 20, text: "20" },
                    { value: 50, text: "50" },
                    { value: 100, text: "100" }
                ]
            }
        },
        computed: {
            // Two way binding models
            searchTextModel: {
                get() {
                    return this.searchText
                },
                set(value) {
                    this.$emit("update:searchText", value)
                }
            },
            filterTextModel: {
                get() {
                    return this.filterText
                },
                set(value) {
                    this.$emit("update:filterText", value)
                }
            },
            pageSizeModel: {
                get() {
                    return this.pageSize
                },
                set(value) {
                    this.$emit("update:pageSize", value)
                }
            },

            // Pagination stuff
            maxPage() {
                return Math.max(Math.ceil(this.listLength / this.pageSize), 1)
            },
            pages() {
                if (this.maxPage < 7)
                    return Array.from({ length: this.maxPage }, (x, i) => i + 1)
                if (this.selectedPage <= 4) return [1, 2, 3, 4, 5, 6, this.maxPage]
                if (this.selectedPage + 2 < this.maxPage)
                    return [
                        1,
                        this.selectedPage - 2,
                        this.selectedPage - 1,
                        this.selectedPage,
                        this.selectedPage + 1,
                        this.selectedPage + 2,
                        this.maxPage
                    ]
                return [
                    1,
                    this.maxPage - 5,
                    this.maxPage - 4,
                    this.maxPage - 3,
                    this.maxPage - 2,
                    this.maxPage - 1,
                    this.maxPage
                ]
            }
        },
        watch: {
            searchText: function(val) {
                this.$emit("update:selectedPage", 1)
            },
            pageSize: function(val) {
                this.$emit("update:selectedPage", 1)
            },
            filterText: function(val) {
                this.$emit("update:selectedPage", 1)
            }
        }
    }
</script>
<style scoped>
    .ui.button {
        border-radius: 0.28571429rem;
    }
    .ui.icon.input > i.icon:not(.link) {
        margin-top: 7px;
    }
    .dropdown,
    .ui.form .fields .field .ui.input input,
    .ui.form .field .ui.input input {
        margin-top: 10px;
    }
    .ui.table {
        font-size: 0.8em;
    }
</style>
