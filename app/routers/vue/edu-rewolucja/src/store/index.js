// Wzór jak to powinno wyglądać: https://github.com/vuejs/vuex/tree/main/examples/classic/shopping-cart


import { createStore } from 'vuex'
import select_rank from './modules/select_rank'

const store = createStore({
    modules: {
        select_rank: select_rank
    },
})

export {store}