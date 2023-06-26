<template>
  <div>
    <h1>Authors</h1>
    <DataTable class="my-3" :columns="tableColumns" :data="allAuthors" @rowClicked="handleEditAuthor" />
    <AuthorsModal :isOpen="modalShow" :author="selectedAuthor" @closeModal="onCloseModal" :mode="authorEvent" />
    <b-button variant="primary" class="float-right" @click="onCreate()">Create</b-button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { IAuthor, ICustomAuthor } from '~/store/author';
import { AuthorModalMode } from '~/components/authors/Modal.vue';
import DataTable from '~/components/elements/dataTable/DataTable.vue';

export default defineComponent({
  name: 'books',
  middleware: 'authenticated',
  data() {
    return {
      searchQuery: '',
      tableColumns: [
        { name: 'Name', key: 'name' },
        { name: 'Books Count', key: 'books_count' },
      ],
      modalShow: false,
      selectedAuthor: {},
      authorEvent: AuthorModalMode.Create as AuthorModalMode,
    };
  },
  components: {
    DataTable,
  },
  async mounted() {
    await this.$accessor.author.getAllAuthors();
  },
  computed: {
    allAuthors() {
      return this.$accessor.author.allAuthors.map(
        (item: IAuthor) =>
          ({
            ...item,
            books_count: item.books.length,
          } as ICustomAuthor)
      );
    },
  },
  methods: {
    async handleEditAuthor({ item }: { item: ICustomAuthor }) {
      this.authorEvent = AuthorModalMode.Update;
      await this.$accessor.author.getAuthorById(item.id ?? 1);
      this.modalShow = true;
    },
    onCloseModal() {
      this.modalShow = false;
      //   this.selectedAuthor = {};
    },
    onCreate() {
      this.authorEvent = AuthorModalMode.Create;
      this.selectedAuthor = {};
      this.modalShow = true;
    },
  },
});
</script>
