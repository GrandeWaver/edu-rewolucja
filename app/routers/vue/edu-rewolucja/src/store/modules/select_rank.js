
const state = () => ({
    rank: undefined,
    price: undefined
  })

const mutations = {
    set_rank (state, data) {
        state.rank = data
    },
    set_price (state, data) {
        state.price = data
    }
}

export default {
    state,
    mutations
}