<template>
  <div class="animated fadeIn input-item">
    <b-card >
      <div slot="header">INPUT - ITEM BARANG  
        <div class="card-header-actions">
          <b-button variant="danger mr-1" @click="close()" > <i class="fa fa-close"></i> Close</b-button>
        </div>
      </div>
      <b-row no-gutter>
        <b-col lg="5">
            <CameraCapture3 :key="resetCamera" @image-captured="handleImageCaptured" 
            @image2-captured="handleImage2Captured" 
            @image3-captured="handleImage3Captured" class="mb-2"/>            
        </b-col>
        <b-col lg="7">
            <b-row no-gutter>
                <b-col cols="6">
                    <b-input-group v-if="(capturedImage)">
                        <b-input-group-prepend><label style="width:70px;">Gambar#1</label></b-input-group-prepend>
                        <b-input-group-append>
                                <b-button class="btn btn-danger" @click="capturedImage=null" size="sm"> <i class="fa fa-times"></i></b-button>
                        </b-input-group-append>
                    </b-input-group>
                    <div style="width:300px;height:300px">
                        <img :src="capturedImage" alt="Gambar#1" width="300" />
                    </div>
                </b-col>
                <b-col cols="6">
                    <b-input-group v-if="(capturedImage2)">
                        <b-input-group-prepend><label style="width:70px;">Gambar#2</label></b-input-group-prepend>
                        <b-input-group-append>
                                <b-button class="btn btn-danger" @click="capturedImage2=null" size="sm"> <i class="fa fa-times"></i></b-button>
                        </b-input-group-append>
                    </b-input-group>
                    <img :src="capturedImage2" alt="Gambar#2" width="300" />
                </b-col>
                <b-col cols="6">
                    
                    <b-input-group v-if="(capturedImage3)">
                        <b-input-group-prepend><label style="width:70px;">Gambar#3</label></b-input-group-prepend>
                        <b-input-group-append size="sm">
                                <b-button class="btn btn-danger " @click="capturedImage3=null" size="sm"> <i class="fa fa-times"></i></b-button>
                        </b-input-group-append>
                    </b-input-group>
                    <img :src="capturedImage3" alt="Gambar#3" width="300" />
                </b-col>
                <b-col cols="">
                    <b-card class="mt-2">
                        <b-input-group>
                            <b-input-group-prepend><label>Nama Barang</label></b-input-group-prepend>
                            <b-form-input  v-model="frmdata.item_name" :state="!$v.frmdata.item_name.$error"></b-form-input>
                        </b-input-group>
                                <b-input-group >
                                    <b-input-group-prepend><label>Harga Barang</label></b-input-group-prepend>
                                    <my-number class="form-control text-right" separator=","  :precision="2"  v-model="frmdata.item_price" :state="!$v.frmdata.item_price.$error" ></my-number>
                                </b-input-group>
                        <b-row >
                            <b-col cols="7">
                                <b-input-group >
                                    <b-input-group-prepend><label>Jml. Stock</label></b-input-group-prepend>
                                    <b-form-input v-model="frmdata.item_stock" type="number" :min="1" :state="!$v.frmdata.item_stock.$error"></b-form-input>                                        
                                </b-input-group>
                            </b-col>
                        </b-row>                      
                        <b-row class="justify-content-center mt-2 ">
                            <b-button class="btn btn-success ml-1" @click="submitItem">Simpan</b-button>
                            <b-button class="btn btn-secondary ml-2" @click="resetForm">Kosongkan/ Input Item lain</b-button>
                        </b-row>
                    </b-card>
                </b-col>
            </b-row>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<style lang="scss">
  .input-item {
      .input-group {
          padding-bottom:2px;
          .input-group-prepend {
              label {
                  padding-top: 5px;
                  padding-right: 5px;
                  width: 100px;
              }
          }
      }

  }

</style>

<script>
import items from "../apis/items";
import Loading from 'vue-loading-overlay';
import myNumber from "../components/my-number";
import CameraCapture3 from "../components/CameraCapture3.vue";
import { validationMixin } from "vuelidate";
import { required} from "vuelidate/lib/validators";
import toastr from "mini-toastr";
toastr.init();

export default {
  components: {Loading,myNumber,CameraCapture3},
  mixins: [validationMixin],
  validations: {
        frmdata: {
            item_name: { required },
            item_price: { required },
            item_stock: { required },
        },
  }, 
  data() {
    return {
      itemsApi:items,
      resetCamera: false,
        frmdata: {
            item_name: '',
            item_price: 0,
            item_stock: 1,
        },
      model:{},
      capturedImage:null,
      capturedImage2:null,
      capturedImage3:null,

      isLoading:false,
    };
  },
  methods: {
    handleImageCaptured(imageData) {
      this.capturedImage = imageData;
    },
    handleImage2Captured(imageData) {
        console.log("handleImage2Captured")
      this.capturedImage2 = imageData;
    },
    handleImage3Captured(imageData) {
        console.log("handleImage3Captured")
      this.capturedImage3 = imageData;
    },
    async submitItem() {
      try {
        const frm = {...this.frmdata};
        frm.image= this.capturedImage
        frm.image2= this.capturedImage2
        frm.image3= this.capturedImage3
        console.log("this.capturedImage2:",this.capturedImage2)
        console.log("this.capturedImage3:",this.capturedImage3)
        const response = await items.insert(frm);
        toastr.success("Item berhasil disimpan!");
        // this.resetForm();
      } catch (error) {
        console.error("Error saving item:", error);
        toastr.error("Gagal menyimpan item!");
      }
    }, 
    resetForm(){
      //this.resetCamera = !this.resetCamera;
      this.frmdata.item_name= '';
      this.frmdata.item_price= 0;
      this.frmdata.item_stock= 1;
      this.capturedImage=null
      this.capturedImage2=null
      this.capturedImage3=null
    },
    close(){
      router.push({name :"app.itemlist"});
    },    
  }
};
</script>
