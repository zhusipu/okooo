const app = {
  state: {
    notifyList: []
  },
  mutations: {
    ADD_NOTIFY: (state, keys) => {
      for (let i = 0; i < keys.length; i++) {
        state.notifyList.push(keys[i])
      }
    }
  },
  actions: {
    addNotify({ commit }, key) {
      commit('ADD_NOTIFY', key)
    }
  }
}

export default app
