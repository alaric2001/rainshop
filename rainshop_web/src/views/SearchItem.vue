<template>
  <div class="animated fadeIn list-item">
    <b-card >
      <div slot="header">CARI BARANG  
        <div class="card-header-actions">
          <b-button variant="primary mr-1" @click="close()" > <i class="fa fa-close"></i> Close</b-button>
        </div>
      </div>

      <CameraCapture @image-captured="searchItem" />
      <div v-if="searchResults.length" class="p-1">
        <h3>Hasil Pencarian:</h3>
            <b-table
              class="mb-0 text-nowrap"
              ref="tblHasil"
              responsive
              striped hover 
              style="font-size:large;" 
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
                    <img :src="data.item.image1" @click="openZoomImage(data.item.image1)" class="img-fluid" alt />
            </template>
            <template v-slot:cell(image2)="data">
                    <img :src="data.item.image2" @click="openZoomImage(data.item.image2)" class="img-fluid" alt />
            </template>
            <template v-slot:cell(image3)="data">
                    <img :src="data.item.image3" @click="openZoomImage(data.item.image3)" class="img-fluid" alt />
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
    </b-card>
    <b-modal v-model="showZoomGambar"  header-bg-variant="primary" title="Zoom Gambar Barang" size="md" :centered="true" ok-only  >
            <img :src="zoomImage" :key="zoomImage" class="img-fluid" width="640" height="480" alt />
    </b-modal>
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
        zoomImage:null,
        showZoomGambar:false
    };
  },
  methods: {
    openZoomImage: function(gambar) {
        this.zoomImage=gambar
        this.showZoomGambar=true;
    },
    async searchItem(imageData) {
      try {
        const response = await items.search({
          image: imageData,  // Base64 image
        });
        this.searchResults = response.data;
        console.log('searchItem response.data: ', this.searchResults);
      } catch (error) {
        console.error("Error searching item:", error);
        toastr.error("Gagal mencari item!");
      }
    },
    close(){
      router.push("/");
    },    
  },
};
</script>