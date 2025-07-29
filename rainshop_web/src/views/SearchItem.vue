<template>
  <div>
    <h1>Cari Item Barang</h1>
    <CameraCapture @image-captured="searchItem" />
    <div v-if="searchResults.length">
      <h3>Hasil Pencarian:</h3>
          <b-table
            class="mb-0 text-nowrap"
            ref="tblHasil"
            responsive
            striped hover 
            style="font-size:smaller;" 
            :items="searchResults"
            :fields="fields"
          >
          <template v-slot:cell(isactive)="data">
            <span v-if="(data.item.isactive==1)">Yes</span>
          </template>
          <template v-slot:cell(modified)="data">
            <span v-if="(data.item.modified)">{{ data.item.modified | moment("DD-MMM-YY") }}</span>
          </template>
          <template v-slot:cell(item_price)="data">
            {{(data.item.item_price)|numFormat}}
          </template>
          <template v-slot:cell(menuimage)="data">
              <div style="width:50%; margin: -10px; position: relative;">
                  <img :src="data.item.menuimg" class="img-fluid" alt />
              </div>
          </template>

          <template v-slot:cell(action)="data">
            <div class="text-center">
            <a href="javascript:void(0)" @click="edit(data.item)">
              <i class="fa fa-pencil"></i>
            </a>
            |
            <a href="javascript:void(0)" class="text-danger" @click="deleteConfirm(data.item)">
              <i class="fa fa-trash"></i>
            </a>
            </div>
          </template>

          </b-table>
    </div>
  </div>
</template>

<script>
import CameraCapture from "../components/CameraCapture.vue";
import items from "../apis/items";

export default {
  components: { CameraCapture },
  data() {
    return {
      searchResults: [],
      fields: [
          { key: "item_name" , 
            label: "Nama Item Barang",
            sortable: true
          },
          {
            key: "item_price",
            label: "Harga Jual",
            sortable: true
          },
          {
            key: "item_stock",
            label: "Jml. Stock",
            thClass: "text-center",
            tdClass: "text-center",
            sortable: true
          },
          {
            key: "isactive",
            thStyle: "width:100px",
            label: "Active",
            tdClass: "text-center",
            sortable: true
          },
          {
            key: "menuimage",
            thStyle: "width:20px",
            label: "Image",
            tdClass: "text-center"
          },
      ],

    };
  },
  methods: {
    async searchItem(imageData) {
      try {
        const response = await items.search({
          image: imageData,  // Base64 image
        });
        this.searchResults = response.data;
        console.log('searchItem response.data: ', this.searchResults);
      } catch (error) {
        console.error("Error searching item:", error);
        alert("Gagal mencari item!");
      }
    },
  },
};
</script>