import { getterTree, mutationTree, actionTree } from 'typed-vuex';
import { IBook } from './book';

export interface IAuthor {
  id?: number;
  name: string;
  books: IBook[];
}

export interface ICustomAuthor extends IAuthor {
  books_count: number;
}

export const state = () => ({
  selectedAuthor: {} as IAuthor,
  allAuthors: [] as IAuthor[],
});

export const getters = getterTree(state, {});

export const mutations = mutationTree(state, {
  setSelectAuthor(state, author: IAuthor) {
    state.selectedAuthor = author;
  },
  setAllAuthors(state, authors: IAuthor[]) {
    state.allAuthors = authors;
  },
});

export const actions = actionTree(
  { state, getters, mutations },
  {
    async getAllAuthors({ commit }) {
      await this.$axios
        .get('/authors')
        .then(({ data }) => {
          commit('setAllAuthors', data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getAuthorById({ commit }, author_id: Number) {
      await this.$axios
        .get(`/authors/${author_id}`)
        .then(({ data }) => {
          commit('setSelectAuthor', data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async createAuthor({}, data) {
      await this.$axios.post('/authors', data).catch((error) => {
        console.log(error);
      });
    },
    async updateAuthor({}, data) {
      const response = await this.$axios.put(`/authors/${data.id}`, data);
    },
    resetSelectedAuthor({ commit }) {
      commit('setSelectAuthor', {} as IAuthor);
    },
  }
);
