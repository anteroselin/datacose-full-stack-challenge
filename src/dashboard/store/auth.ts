import { getterTree, mutationTree, actionTree } from 'typed-vuex';

export const state = () => ({
  isAuthenticated: false as boolean,
});

export const getters = getterTree(state, {});

export const mutations = mutationTree(state, {
  setIsAuthenticated(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated;
  },
});

export const actions = actionTree(
  { state, getters, mutations },
  {
    async login({ commit }, { formData }) {
      await this.$axios
        .$post('/login', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        .then(({ access_token }) => {
          commit('setIsAuthenticated', true);
          localStorage.setItem('access-token', access_token);
          this.$router.push('/authors');
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async logout({ commit }) {
      // Clear the user and token from the store
      localStorage.setItem('access-token', '');
      commit('setIsAuthenticated', false);
    },
  }
);
