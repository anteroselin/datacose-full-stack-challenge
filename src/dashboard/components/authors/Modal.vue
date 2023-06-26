<template>
  <b-modal v-model="isModalOpen" :title="mode" @hidden="onCancel">
    <form ref="form" @submit.stop.prevent="onSubmit">
      <b-form-group label="Name" label-for="name-input" invalid-feedback="Name is required" :state="nameState">
        <b-form-input id="name-input" v-model="authorData.name" :state="nameState" required></b-form-input>
      </b-form-group>
      <b-form-group label="Books" label-for="books" v-if="mode === AuthorModalMode.Update">
        <b-table
          small
          :fields="['title', 'pages', 'action']"
          :items="authorData.books"
          responsive="sm"
          outlined
          hover
          show-empty
        >
          <template #cell(title)="data">
            {{ data.item.title }}
          </template>
          <template #cell(pages)="data"> {{ data.item.pages }} </template>
          <template #cell()="data">
            <b-button size="sm" variant="outline-primary" @click="onEditBook(data)"> Edit </b-button>
            <b-button size="sm" variant="outline-primary" @click="onDeleteBook(data)"> Delete </b-button>
            <!-- </div> -->
          </template>
          <template #empty>
            <div class="text-center">No book for this author.</div>
          </template>
        </b-table>
        <BooksModal
          :isOpen="modalShow"
          :book="selectedBook"
          :disable="true"
          :mode="bookMode"
          @closeModal="onCloseModal"
        />
      </b-form-group>
    </form>
    <template #modal-footer>
      <b-button size="md" variant="primary" @click="onSubmit()"> Save </b-button>
      <b-button size="md" variant="outline-primary" @click="onCancel()"> Cancel </b-button>
    </template>
  </b-modal>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { IAuthor } from '~/store/author';
import { BookModalMode } from '~/components/books/Modal.vue';
import { IBook } from '~/store/book';

export enum AuthorModalMode {
  Create = 'Create a Author',
  Update = 'Update a Author',
}

export default defineComponent({
  name: 'AuthorModal',
  data() {
    return {
      name: '' as String,
      nameState: null as Boolean | null,
      modalShow: false,
      isModalOpen: false as Boolean,
      selectedBook: {
        id: 0,
        title: '',
        pages: 0,
        author_id: null as Number | null,
      } as IBook,
      bookMode: BookModalMode.Create,
      authorData: {} as IAuthor,
      AuthorModalMode,
    };
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
    mode: {
      type: String as PropType<AuthorModalMode>,
      default: AuthorModalMode.Create,
    },
  },
  computed: {
    author() {
      return this.$accessor.author.selectedAuthor ?? {};
    },
  },
  watch: {
    isOpen: function (val) {
      this.isModalOpen = val;
    },
    author: function (val) {
      this.authorData = { ...val };
    },
  },
  methods: {
    onEditBook({ item }: { item: IBook }) {
      this.bookMode = BookModalMode.Update;
      this.selectedBook = item;
      this.modalShow = true;
    },
    async onDeleteBook({ item }: { item: IBook }) {
      if (item.id) this.$accessor.book.deleteBook(item.id);
    },
    checkFormValidity() {
      const valid = (this.$refs.form as HTMLFormElement).checkValidity();
      this.nameState = valid;
      return valid;
    },
    onCancel() {
      this.$accessor.author.resetSelectedAuthor();
      this.$emit('closeModal');
    },
    async onSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }

      if (this.mode === AuthorModalMode.Create) {
        await this.$accessor.author.createAuthor(this.authorData);
      } else {
        await this.$accessor.author.updateAuthor(this.authorData);
      }
      this.$accessor.author.getAllAuthors();
      this.$accessor.author.resetSelectedAuthor();
      this.$emit('closeModal');
      this.nameState = null;
    },
    onCloseModal() {
      this.modalShow = false;
    },
  },
});
</script>
