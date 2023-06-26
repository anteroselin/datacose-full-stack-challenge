import { getterTree, mutationTree, actionTree } from 'typed-vuex';

export interface IBook {
  id?: number;
  title: string;
  pages: number;
  author_id: number | null;
  author_name?: string;
}

export const state = () => ({
  allBooks: [] as IBook[],
});

export const getters = getterTree(state, {});

export const mutations = mutationTree(state, {
  setAllBooks(state, books: IBook[]) {
    state.allBooks = books;
  },
});

export const actions = actionTree(
  { state, getters, mutations },
  {
    async getAllBooks({ commit }) {
      await this.$axios.get('/books').then(({ data }: { data: IBook[] }) => {
        commit('setAllBooks', data);
      });
    },
    async createBook({ dispatch }, bookData: IBook) {
      await this.$axios
        .post('/books', bookData)
        .then(() => {
          dispatch('getAllBooks');
          const author = this.app.$accessor.author.selectedAuthor;
          if (author) {
            this.app.$accessor.author.getAuthorById(author.id ?? 1);
          }
        })
        .catch((error) => console.log(error));
    },
    async updateBook({ dispatch }, bookData: IBook) {
      await this.$axios
        .put(`/books/${bookData?.id}`, bookData)
        .then(() => {
          dispatch('getAllBooks');
          const author = this.app.$accessor.author.selectedAuthor;
          if (author) {
            this.app.$accessor.author.getAuthorById(author.id ?? 1);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async deleteBook({ dispatch }, book_id: number) {
      await this.$axios
        .delete(`/books/${book_id}`)
        .then(() => {
          dispatch('getAllBooks');
          const author = this.app.$accessor.author.selectedAuthor;
          if (author) {
            this.app.$accessor.author.getAuthorById(author.id ?? 1);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  }
);
