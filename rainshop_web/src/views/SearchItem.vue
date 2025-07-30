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
            :items="searchResults"
            :fields="fields"
          >
          <template v-slot:cell(isactive)="data">
            <span v-if="(data.item.isactive==1)">Yes</span>
          </template>
          <!-- <template v-slot:cell(modified)="data">
            <span v-if="(data.item.modified)">{{ data.item.modified | moment("DD-MMM-YY") }}</span>
          </template> -->
          <template v-slot:cell(item_price)="data">
            {{(data.item.item_price)|numFormat}}
          </template>
          <template v-slot:cell(image1)="data">
                  <img :src="data.item.image1" class="img-fluid" alt />
          </template>
          <template v-slot:cell(image2)="data">
                  <img :src="data.item.image2" class="img-fluid" alt />
          </template>
          <template v-slot:cell(image3)="data">
                  <img :src="data.item.image3" class="img-fluid" alt />
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

<style lang="scss">
    .input-group {
        padding-bottom:2px;
        .input-group-prepend {
            label {
                padding-top: 5px;
                padding-right: 5px;
                width: 130px;
            }
        }
    }

      .item {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 0 0 20px;
        position: absolute;
        top: 5px;
        left: 8px;
        bottom: 5px;
        right: 8px;
        transition: 1.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;

        .price {
          font-size: 13px;
          margin-top: 5px;
          color: #ff5722;

          .price-discount {
            margin-left: 10px;
            font-size: 11px;
            background: #f02222;
            padding: 3px 7px;
            color: #fff;
            border-radius: 2px;
            margin-top: -10px;
          }
        }

        img {
          border-radius: 5px 5px 0 0;
        }

        &:hover {
          background-color: rgba(0, 0, 0, 0.1);
        }
      }    
</style>

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
            key: "image1",
            thStyle: "width:150px",
            label: "Image",
            tdClass: "text-center"
          },
          {
            key: "image2",
            thStyle: "width:150px",
            label: "Image",
            tdClass: "text-center"
          },
          {
            key: "image3",
            thStyle: "width:150px",
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