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
              <b-button v-if="((capturedImage) && (searchResults.length==0))" variant="warning" @click="searchItem" > <i class="fa fa-search"></i> Lihat apakah gambar sudah pernah didaftarkan</b-button>
            <div v-if="searchResults.length" class="p-1">
                  <b-table
                    class="mb-0 text-nowrap"
                    style="font-size:smaller;" 
                    ref="tblHasil"
                    responsive
                    striped hover 
                    :items="searchResults"
                    :fields="fields"
                  >
                  <template v-slot:cell(item_name)="data">
                      <h3>{{(data.item.item_name)}}</h3>
                        <span style="font-size: larger;">Harga: RP. {{(data.item.item_price)|numFormat}}</span>
                        <div style="float:right; text-align: right; margin-top:-15px; margin-right: -20px;">
                            <b-button variant="warning" @click="rowEditGambar(data.item)" >edit</b-button>
                        </div>

                  </template>
                  <template v-slot:cell(modified)="data">
                    <p  v-if="(data.item.modified)" class="m-0 p-0">{{ data.item.modified | moment("DD-MMM-YYYY") }}</p>
                    <span  v-if="(data.item.modified)"><i class="fa fa-clock-o"></i> {{ data.item.modified | moment("HH:mm") }}</span>
                  </template>

                  <template v-slot:cell(image)="data">
                          <img :src="data.item.image" :key="data.item.image" @click="openZoomImage(data.item.image)" class="img-fluid" alt />
                  </template>

                </b-table>

            </div>

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
    <b-modal v-model="showZoomGambar"  header-bg-variant="primary" title="Zoom Gambar Barang" size="md" :centered="true" ok-only  >
            <img :src="zoomImage" :key="zoomImage" class="img-fluid" width="640" height="480" alt />
    </b-modal>
    <b-modal v-model="showEditGambar"  header-bg-variant="primary" title="Form Edit - Gambar  Barang" size="lg" :centered="true" hide-footer >
      <b-card>
              <b-input-group>
                  <b-input-group-prepend><label>Nama Barang</label></b-input-group-prepend>
                  <b-form-input  v-model="model.item_name" disabled></b-form-input>
              </b-input-group>
              <b-row v-if="modeCaptureCamera==false">
                  <b-col cols="4" v-for="(row,imgIdx) in images" :key="row.image_id">
                      <b-input-group>
                          <b-input-group-prepend><label class="text-right">Gambar#{{imgIdx+1 }}</label></b-input-group-prepend>
                          <b-input-group-append>
                              <b-button variant="primary mr-1" @click="ShowCaptureCamera(imgIdx)">Edit <i class="fa fa-camera"></i></b-button>
                          </b-input-group-append>                    
                      </b-input-group>
                      <img :src="row.image" :key="row.image" class="img-fluid" alt />
                  </b-col>
              </b-row>
               <CameraCapture v-else @image-captured="handleImageCaptured" class="mb-2"/>

            <b-row class="justify-content-center mt-1 mb-2">
                  <b-button class="btn btn-success mr-1" @click="submitEditGambar">Simpan</b-button>
                  <b-button class="btn btn-warning ml-1" @click="closeEditGambar">Batal/Close</b-button>
            </b-row>
      </b-card>      
    </b-modal>

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
      table {
        td {
          .dropdown-item {
            padding: 0.1rem 1.5rem !important;
            font-size: smaller !important;
          }
        }
      }

  }

</style>

<script>
import items from "../apis/items";
import Loading from 'vue-loading-overlay';
import myNumber from "../components/my-number";
import CameraCapture from "../components/CameraCapture.vue";
import CameraCapture3 from "../components/CameraCapture3.vue";
import { validationMixin } from "vuelidate";
import { required} from "vuelidate/lib/validators";
import toastr from "mini-toastr";
toastr.init();

export default {
  components: {Loading,myNumber,CameraCapture,CameraCapture3},
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
      isLoading:false,
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
      searchResults: [],
      fields: [
          { key: "item_name" , 
            label: "Nama yg pernah didaftarkan",
          },
          {
            key: "image",
            thStyle: "width:100px",
            label: "Gambar",
            thClass: "text-center",
            tdClass: "text-center"
          },
          {
            key: "modified",
            label: "Tgl & Jam",
            thStyle: "width:80px",
            thClass: "text-center",
            tdClass: "text-center"
          },
      ],
        zoomImage:null,
        showZoomGambar:false,
      showEditGambar:false,
      modeCaptureCamera:false,
      editImageIdx:null,
    };
  },
  methods: {
    handleImageCaptured(imageData) {
      this.capturedImage = imageData;
      this.searchResults=[]
    },
    handleImage2Captured(imageData) {
        console.log("handleImage2Captured")
      this.capturedImage2 = imageData;
    },
    handleImage3Captured(imageData) {
        console.log("handleImage3Captured")
      this.capturedImage3 = imageData;
    },
    openZoomImage: function(gambar) {
        this.zoomImage=gambar
        this.showZoomGambar=true;
    },
    async searchItem() {
      try {
        const list = await items.imageSearch({
          image: this.capturedImage,  // Base64 image
        });
        list.forEach(el => {
          el.image='';
          items.imageItem(el.image_id).then((imgBase64) => {
            el.image=imgBase64          
          })
        });
        this.searchResults = list;
        this.showWebcam=false;
      } catch (error) {
        console.error("Error searching item:", error);
        alert("Gagal mencari item!");
      }
    },
    async rowEditGambar(record) {
      try {
        const dataSvr = await items.detail(record)
        this.images = dataSvr.images;
        for (let index = 0; index < this.images.length; index++) {
          const el = this.images[index];
          const imgBase64 = await items.imageItem(el.image_id)
          el.image=imgBase64          
        }        
        if (this.images.length<3) {
           for (let index = this.images.length; index < 3; index++) {
            this.images.push({})
           }
        }
        this.modeCaptureCamera=false;
        this.editImageIdx='';
        this.showEditGambar=true;
      } catch (error) {
          console.log('error : ', error);
          if (error.sql) {
            toastr.error(error.sql, 'ERROR MESSAGE', 10000);
          } else if (error.sqlMessage) {
            toastr.error(error.sqlMessage, 'ERROR MESSAGE', 10000);
          } else if (error.message) {
            toastr.error(error.message, 'ERROR MESSAGE', 10000);
          } else {
            toastr.error(JSON.stringify(error), 'ERROR MESSAGE', 10000);
          }        
      }
    },
    ShowCaptureCamera(imageIdx) {
        this.editImageIdx=imageIdx;
        this.modeCaptureCamera=true;
    },
    async submitEditGambar() {
      try {
        if (this.capturedImage) {
            const frm = {
              image:this.capturedImage
            }
            const editedImage= this.images[this.editImageIdx]
            if (editedImage.image_id) {
                frm.image_id=editedImage.image_id;
                await items.updateImage(frm);
            } else {
                frm.item_id=this.model.item_id;
                const hasil = await items.insertImage(frm);
                editedImage.image_id=hasil.data.image_id;
            }
            editedImage.image=this.capturedImage;
            toastr.success("Item berhasil disimpan!");
            this.modeCaptureCamera=false;
          } else {
            toastr.error("Ambil Gambar dulu baru klik simpan", 'ERROR', 10000);
          }
      } catch (error) {
        console.error("Error saving item:", error);
        toastr.error("Gagal menyimpan item!", 'ERROR MESSAGE', 10000);
      }
    }, 
    closeEditGambar: function() {
      this.showEditGambar=false
    },

    async submitItem() {
      try {
        if ( this.capturedImage || this.capturedImage2 || this.capturedImage3) {
            const frm = {...this.frmdata};
            frm.image= this.capturedImage
            frm.image2= this.capturedImage2
            frm.image3= this.capturedImage3
            await items.insert(frm);
            toastr.success("Item berhasil disimpan!");
            // this.resetForm();
        } else {
            toastr.error('Minimal Ambil satu gambar', 'ERROR', 10000);
        }  
      } catch (error) {
        toastr.error("Gagal menyimpan item!");
        console.log('error : ', error);
        if (error.sql) {
            toastr.error(error.sql, 'ERROR MESSAGE', 10000);
        } else if (error.sqlMessage) {
            toastr.error(error.sqlMessage, 'ERROR MESSAGE', 10000);
        } else if (error.message) {
            toastr.error(error.message, 'ERROR MESSAGE', 10000);
        } else {
            toastr.error(JSON.stringify(error), 'ERROR MESSAGE', 10000);
        }        
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
