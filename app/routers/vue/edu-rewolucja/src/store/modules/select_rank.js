
const state = () => ({
    data: undefined
  })

const mutations = {
    set (state, data) {
        state.data = data
    }
}

export default {
    state,
    mutations
}