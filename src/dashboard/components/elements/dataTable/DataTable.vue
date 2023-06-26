<template>
  <div>
    <b-form-group label-for="filter-input">
      <b-input-group size="md">
        <b-form-input id="filter-input" v-model="filter" type="search" placeholder="Type to Search"></b-form-input>

        <b-input-group-append>
          <b-button variant="outline-primary" :disabled="!filter" @click="filter = ''">Clear</b-button>
        </b-input-group-append>
      </b-input-group>
    </b-form-group>
    <b-table
      small
      :fields="columns"
      :items="data"
      :current-page="page"
      :per-page="pageSize"
      :filter="filter"
      responsive="sm"
      outlined
      hover
      head-variant="light"
      @row-clicked="onRowClicked"
      @Filter="onFiltered"
      show-empty
    >
      <template #empty>
        <div class="text-center">No book for this author.</div>
      </template>
      <template #emptyfiltered>
        <div class="text-center">No book match.</div>
      </template>
    </b-table>
    <b-row align-v="center">
      <b-col lg="2" class="my-1">
        <b-form-group label-for="per-page-select" label-align-sm="right" label-size="md" class="mb-0">
          <b-form-select id="per-page-select" v-model="pageSize" :options="pageOptions" size="md"></b-form-select>
        </b-form-group>
      </b-col>
      <b-col lg="4" class="my-1 ml-auto">
        <b-pagination
          v-model="page"
          :total-rows="data.length"
          :per-page="pageSize"
          size="md"
          class="my-0 float-right"
        ></b-pagination>
      </b-col>
    </b-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
interface IColumn {
  key: string;
  name: string;
}

export default defineComponent({
  name: 'DataTable',
  data() {
    return {
      page: 1 as Number,
      pageSize: 10,
      pageOptions: [
        { text: '10', value: 10 },
        { text: '15', value: 15 },
        { text: '20', value: 20 },
      ],
      filter: '',
      total: 0,
    };
  },
  props: {
    columns: {
      type: Array as PropType<Array<IColumn>>,
      default: [],
      required: true,
    },
    data: {
      type: Array as PropType<Array<Object>>,
      default: [],
      required: true,
    },
  },
  mounted() {
    this.total = this.data.length;
  },
  methods: {
    onFiltered(filteredItems: Array<Object>) {
      this.total = filteredItems.length;
      this.page = 1;
    },
    onRowClicked(item: Object) {
      this.$emit('rowClicked', { item });
    },
  },
});
</script>
