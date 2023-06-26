<template>
  <b-modal v-model="isModalOpen" :title="mode" @hidden="onCancel">
    <form ref="form" @submit.stop.prevent="onSubmit">
      <b-form-group label="Title" label-for="title-input" invalid-feedback="Title is required" :state="titleState">
        <b-form-input id="title-input" v-model="bookData.title" :state="titleState" required></b-form-input>
      </b-form-group>
      <b-form-group label="Page" label-for="page-input" invalid-feedback="Page is required" :state="pageState">
        <b-form-input
          type="number"
          id="page-input"
          v-model="bookData.pages"
          :state="pageState"
          min="0"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group label="Author" label-for="author-select" invalid-feedback="Author is required" :state="authorState">
        <TreeSelect
          id="author-select"
          :options="
            allAuthors.map((author) => ({
              id: author.id,
              label: author.name,
            }))
          "
          v-model="bookData.author_id"
          :disabled="disable"
        >
          <div slot="author-label" slot-scope="{ node }">{{ node.raw.customLabel }}</div>
        </TreeSelect>
      </b-form-group>
    </form>
    <template #modal-footer>
      <b-button size="sm" variant="primary" @click="onSubmit()"> Save </b-button>
      <b-button size="sm" variant="outline-primary" @click="onCancel()"> Cancel </b-button>
    </template>
  </b-modal>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { IBook } from '~/store/book';
import TreeSelect from '@riophae/vue-treeselect';
import '@riophae/vue-treeselect/dist/vue-treeselect.css';

export enum BookModalMode {
  Create = 'Create a Book',
  Update = 'Update a Book',
}

export default defineComponent({
  components: {
    TreeSelect,
  },
  data() {
    return {
      pageState: null as Boolean | null,
      titleState: null as Boolean | null,
      authorState: null as Boolean | null,
      bookData: {
        id: 0,
        title: '',
        pages: 0,
        author_id: null as Number | null,
      } as IBook,
      isModalOpen: false as Boolean,
    };
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
    book: {
      type: Object as PropType<IBook>,
      default: {},
    },
    disable: {
      type: Boolean,
      default: false,
    },
    mode: {
      type: String as PropType<BookModalMode>,
      default: BookModalMode.Create,
    },
  },
  watch: {
    book: function (val) {
      if (this.mode === BookModalMode.Update) this.bookData = { ...val };
      console.log(this.bookData);
    },

    isOpen: function (val) {
      this.isModalOpen = val;
    },
  },
  computed: {
    allAuthors() {
      return this.$accessor.author.allAuthors;
    },
  },
  methods: {
    checkFormValidity() {
      const form = this.$refs.form as HTMLFormElement;
      const valid = form.checkValidity();
      this.titleState = valid;
      this.pageState = this.bookData.pages > 0;
      this.authorState = !!this.bookData.author_id && this.bookData.author_id > 0;
      return valid && this.pageState && this.authorState;
    },
    onCancel() {
      this.titleState = null;
      this.pageState = null;
      this.$emit('closeModal');
    },
    async onSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }
      if (this.mode === BookModalMode.Create) await this.$accessor.book.createBook(this.bookData);
      else if (this.mode === BookModalMode.Update) await this.$accessor.book.updateBook(this.bookData);
      this.bookData = {
        title: '',
        pages: 0,
        author_id: null,
      };
      this.$emit('closeModal');
    },
  },
});
</script>
