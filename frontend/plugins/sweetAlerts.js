import Vue from 'vue'
import swal from 'sweetalert';

const swaller = {}

swaller.install = function (Vue) {
    Vue.prototype.$swal = swal
}

Vue.use(swaller)
