<template>
  <div>
    <h1>Books</h1>
    <DataTable class="my-3" :columns="tableColumns" :data="allBooks" @rowClicked="handleEditBook" />
    <BooksModal :isOpen="modalShow" :book="selectedBook" @closeModal="onCloseModal" :mode="bookEvent" />
    <b-button variant="primary" class="float-right" @click="onCreate()">Create</b-button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { BookModalMode } from '~/components/books/Modal.vue';
import DataTable from '~/components/elements/dataTable/DataTable.vue';
import { IBook } from '~/store/book';

export default defineComponent({
  name: 'books',
  middleware: 'authenticated',
  data() {
    return {
      searchQuery: '',
      modalShow: false,
      selectedBook: {} as IBook,
      tableColumns: [
        { name: 'Title', key: 'title' },
        { name: 'Pages', key: 'pages' },
        { name: 'Author', key: 'author_name' },
      ],
      bookEvent: BookModalMode.Create as BookModalMode,
    };
  },
  components: {
    DataTable,
  },
  mounted() {
    this.$accessor.book.getAllBooks();
  },
  computed: {
    allBooks() {
      return this.$accessor.book.allBooks;
    },
  },
  methods: {
    handleEditBook({ item }: { item: IBook }) {
      this.bookEvent = BookModalMode.Update;
      this.selectedBook = item;
      this.modalShow = true;
    },
    onCloseModal() {
      this.modalShow = false;
      //   this.selectedBook = this.$accessor.book.selectedBook;
    },
    onCreate() {
      this.bookEvent = BookModalMode.Create;
      this.modalShow = true;
    },
  },
});
</script>
