import { getAccessorType, mutationTree, actionTree } from 'typed-vuex';
import * as auth from '~/store/auth';
import * as book from '~/store/book';
import * as author from '~/store/author';

export const accessorType = getAccessorType({
  modules: {
    auth,
    book,
    author,
  },
});
