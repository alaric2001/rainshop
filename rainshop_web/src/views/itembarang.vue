<template>
  <div class="animated fadeIn list-item">
    <b-card v-show="showList">
      <div slot="header">DAFTAR ITEM BARANG  
        <div class="card-header-actions">
          <b-button variant="primary mr-1" @click="add">Add</b-button>
          <b-button variant="primary mr-1" @click="exportxls()"><i class="fa fa-file-excel-o"></i>Export</b-button>
          <b-button variant="primary mr-1" @click="showFilter=!showFilter"><i class="fa fa-filter"></i> Filter</b-button> 
          <b-button variant="primary mr-1" @click="close()" > <i class="fa fa-close"></i> Close</b-button>
        </div>
      </div>
      <b-row v-if="showFilter" class="ml-2 mr-2">
        <b-col lg="8">
            <b-input-group >
              <b-input-group-prepend><span class="pt-2">Item Name &nbsp;</span></b-input-group-prepend>
              <b-form-input v-model="tblData.item_name" ></b-form-input>
              <b-input-group-append>
                  <b-button class="btn btn-success ml-3" @click="search()" > <i class="fa fa-refresh"></i> Apply Filter</b-button>
              </b-input-group-append>
              <b-input-group-append>
                <b-button class="btn btn-secondary ml-1" @click="clearFilter()" > <i class="fa fa-eraser"></i>Clear Filter</b-button>
              </b-input-group-append>
            </b-input-group>
        </b-col>        
      </b-row>                      
          <b-table
            class="mb-0 text-nowrap"
            ref="tblMenu"
            responsive
            striped hover 
            style="font-size:smaller;" 
            :items="data"
            :fields="fields"
            :current-page="tblData.page"
            :per-page="tblData.limit"
            :sort-by.sync="tblData.sortBy"
            :sort-desc.sync="tblData.sortDesc"
            :key="tblData.limit" 
            @row-clicked="rowClicked"
          >

        <template v-slot:cell(action)="data">
          <b-dropdown dropright variant="outline-secondary" toggle-class="text-decoration-none" no-caret size="sm"
            style="margin:-10px;">
            <template v-slot:button-content>
              <i class="fa fa-play text-primary"></i>
            </template>
            <b-dropdown-item @click="rowEditItem(data.item)" href="#" style="padding:0 !important;"> Edit Nama/Harga/Stok</b-dropdown-item>
            <b-dropdown-item @click="rowEditGambar(data.item)" href="#" style="padding:0 !important;"> Edit Gambar</b-dropdown-item>
          </b-dropdown>
        </template>

          <template v-slot:cell(isactive)="data">
            <span v-if="(data.item.isactive==1)">Yes</span>
          </template>
          <template v-slot:cell(modified)="data">
            <span v-if="(data.item.modified)">{{ data.item.modified | moment("DD-MMM-YY") }}</span>
          </template>
          <template v-slot:cell(item_price)="data">
            {{(data.item.item_price)|numFormat}}
          </template>
        </b-table>
        <b-row class="mt-1">
          <b-col cols="4">
            <div>
              Showing {{(tblData.page - 1) * tblData.limit + 1}}
              to <span v-if="((tblData.page * tblData.limit)>tblData.total)">{{tblData.total}}</span> <span v-else>{{tblData.page * tblData.limit}}</span>
              of {{tblData.total}} entries
            </div>
          </b-col>
          <b-col cols="4" >
              <b-form-group label-cols=3 label="Limit per page"  style="margin-top:0 !important;">
              <b-form-select :options="[10, 15, 20, 25]" :plain="true" v-model="tblData.limit"  size="sm" style="width:80px;"/>
              </b-form-group>
          </b-col>        
          <b-col cols="4">            
            <b-pagination
              align="right"
              :total-rows="tblData.total"
              :per-page="tblData.limit"
              v-model="tblData.page"
            ></b-pagination>
          </b-col>
        </b-row>
    </b-card>

    <loading :active.sync="isLoading" :height="128" :width="128" color="#4b8cf4" ></loading>       
    <b-modal v-model="showDelConfirm" title="Delete Record?" :centered="true" @ok="deleteData">
      <p class="mb-1">1 record is about to be permanently deleted</p>
      <p class="font-weight-bold m-0 text-danger">Are you sure about doing this?</p>
    </b-modal>
    
    <b-modal v-model="showAddForm"  header-bg-variant="primary" title="Form Input -  Item Barang" size="lg" :centered="true" hide-footer >
      <b-card>
            <CameraCapture3 @image-captured="handleImageCaptured" @image2-captured="handleImage2Captured" @image3-captured="handleImage3Captured" class="mb-2"/>
            
              <b-input-group>
                  <b-input-group-prepend><label>Nama Barang</label></b-input-group-prepend>
                  <b-form-input  v-model="frmdata.item_name" :state="!$v.frmdata.item_name.$error"></b-form-input>
              </b-input-group>
            <b-row>
                <b-col lg="6">
                    <b-input-group >
                        <b-input-group-prepend><label>Harga Barang</label></b-input-group-prepend>
                        <my-number class="form-control text-right" separator=","  :precision="2"  v-model="frmdata.item_price" :state="!$v.frmdata.item_price.$error" ></my-number>
                    </b-input-group>
                </b-col>   
                <b-col lg="5">                            
                    <b-input-group >
                        <b-input-group-prepend><label>Jml. Stock</label></b-input-group-prepend>
                        <b-form-input v-model="frmdata.item_stock" type="number" :min="1" :state="!$v.frmdata.item_stock.$error"></b-form-input>                                        
                    </b-input-group>
                </b-col>
            </b-row>                      
            <b-row class="justify-content-center mb-2">
                  <b-button class="btn btn-success mr-1" @click="submitItem">Simpan</b-button>
                  <b-button class="btn btn-warning ml-1" @click="closeForm">Batal</b-button>
                  <b-button class="btn btn-secondary ml-1" @click="resetForm">kosongkan</b-button>
            </b-row>
      </b-card>      
    </b-modal>
    <b-modal v-model="showEditItem"  header-bg-variant="primary" title="Form Edit -  Item Barang" size="lg" :centered="true" hide-footer >
      <b-card>
              <b-input-group>
                  <b-input-group-prepend><label>Nama Barang</label></b-input-group-prepend>
                  <b-form-input  v-model="frmdata.item_name" :state="!$v.frmdata.item_name.$error"></b-form-input>
              </b-input-group>
            <b-row>
                <b-col lg="6">
                    <b-input-group >
                        <b-input-group-prepend><label>Harga Barang</label></b-input-group-prepend>
                        <my-number class="form-control text-right" separator=","  :precision="2"  v-model="frmdata.item_price" :state="!$v.frmdata.item_price.$error" ></my-number>
                    </b-input-group>
                </b-col>   
                <b-col lg="5">                            
                    <b-input-group >
                        <b-input-group-prepend><label>Jml. Stock</label></b-input-group-prepend>
                        <b-form-input v-model="frmdata.item_stock" type="number" :min="1" :state="!$v.frmdata.item_stock.$error"></b-form-input>                                        
                    </b-input-group>
                </b-col>
            </b-row>                      
            <b-row class="justify-content-center mb-2">
                  <b-button class="btn btn-success mr-1" @click="submitEdit">Simpan</b-button>
                  <b-button class="btn btn-warning ml-1" @click="closeEditItem">Batal</b-button>
            </b-row>
      </b-card>      
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
                  <b-button class="btn btn-warning ml-1" @click="closeEditGambar">Batal</b-button>
            </b-row>
      </b-card>      
    </b-modal>

  </div>
</template>
<style lang="scss">
  .list-item {
    table {
      td {
        .dropdown-item {
          padding: 0.1rem 1.5rem !important;
          font-size: smaller !important;
        }
      }
    }
  }
  .modal-form {
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
      fields: [
          {
            key: "action",
            thStyle: "width:50px",
            label:""
          },
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
            key: "modified",
            thStyle: "width:120px",
            label: "Last Update",
            tdClass: "text-center"
          },
      ],
      tblData: {
        page: 1,
        limit: 10,
        total: 0,
        sortBy: null,
        sortDesc: false, item_name:''
      },
        frmdata: {
            item_name: '',
            item_price: 0,
            item_stock: 1,
        },
      model:{},
      images:[],
      isLoading:false,
      showDelConfirm: false,
      showFilter:false,
      showAddForm:false,
      showEditItem:false,
      showEditGambar:false,
      modeCaptureCamera:false,
      showList:true,
      showReport:false,
      reportUrl: `${location.origin}/#load`,
      activeStatus : [{ value: '', text: '-- ALL --' },, { value: '0', text: 'Yes' },{ value: '1', text: 'No' }],
      editImageIdx:''
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
    async submitEdit() {
      try {
        const frm = {...this.frmdata};
        frm.item_id=this.model.item_id;
        const response = await items.update(frm);
        toastr.success("Item berhasil disimpan!");
        // this.resetForm();
      } catch (error) {
        console.error("Error saving item:", error);
        toastr.error("Gagal menyimpan item!");
      }
    }, 
    async submitInsertGambar() {
      try {
        const frm = {...this.frmdata};
        frm.item_id=this.model.item_id;
        await items.insertImage(frm);
        this.refresh();
        toastr.success("Item berhasil disimpan!");
      } catch (error) {
        console.error("Error saving item:", error);
        toastr.error("Gagal menyimpan item!");
      }
    }, 
    async submitEditGambar() {
      try {
        
        const frm = {
          image:this.capturedImage
        }
        const editedImage= this.images[this.editImageIdx]
        if (editedImage.image_id) {
            frm.image_id=editedImage.image_id;
            await items.updateImage(frm);
        } else {
            frm.item_id=this.model.item_id;
            await items.insertImage(frm);
        }
        toastr.success("Item berhasil disimpan!");
      } catch (error) {
        console.error("Error saving item:", error);
        toastr.error("Gagal menyimpan item!", 'ERROR MESSAGE', 10000);
      }
    }, 
    rowClicked(record, index) {
      if (this.model && this.model._rowVariant) {
        delete this.model._rowVariant;
      }
      this.model = record;
      record._rowVariant = "info";
      this.$forceUpdate();
    },
    rowEditItem(record) {
      this.rowClicked(record);
      this.frmdata.item_name= this.model.item_name;
      this.frmdata.item_price= this.model.item_price;
      this.frmdata.item_stock= this.model.item_stock;
      this.frmdata.isactive= this.model.isactive;
      this.showEditItem=true;
    },
    async rowEditGambar(record) {
      this.rowClicked(record);
      try {
        const dataSvr = await items.detail(this.model)
        this.images = dataSvr.images;
        // for (let index = 0; index < this.images.length; index++) {
        //   const el = this.images[index];
        //   const imgBase64 = await items.imageItem(el.image_id)
        //   el.image=imgBase64          
        // }        
        this.images.forEach(el => {
          el.image='';
          items.imageItem(el.image_id).then((imgBase64) => {
            el.image=imgBase64          
          })
        });

        if (this.images.length<2) {
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
    resetForm(){
      this.frmdata.item_name= '';
      this.frmdata.item_price= 1;
      this.frmdata.item_stock= 1;
      this.capturedImage=null
      this.capturedImage2=null
      this.capturedImage3=null
    },
    data: async function(ctx) {
      this.tblData.sortDir = this.tblData.sortDesc ? "desc" : "asc";
      this.lkuLoading = true;
      let list = await items.list(this.tblData);
      this.lkuLoading = false;
      return list;  
    },
    search() {
      this.tblData.page=1;
      this.$refs.tblMenu.refresh();
    },
    refresh() {
      this.$refs.tblMenu.refresh();
    },
    clearFilter(ctx) {
        this.tblData.item_name =  '';
        // this.refresh();
    },    
    saveFilter() {
      const keys = ['item_name'];
      let filtered = false;
      const menuList={};
      for (const key in this.tblData) {
          if (keys.indexOf(key) >= 0 && this.tblData[key]) {
              filtered=true;
              menuList[key]=this.tblData[key];
          }
      }
      if (filtered === true) {
          menuList.page=this.tblData.page;
          menuList.limit=this.tblData.limit;
          menuList.sortBy=this.tblData.sortBy;
          menuList.sortDesc=this.tblData.sortDesc;
          const filter = this.$store.state.filter;
          filter.menuList=menuList;
          this.$store.commit("filter", filter);
      }
    },    


    add: function() {
      this.showList=false;
      this.showAddForm=true
    },
    edit: function() {
        if (this.model) {
          this.saveFilter();
          router.push({name :'resto.adminmenufrm', params: { menuid: this.model.menuid}});
        } else {
            toastr.warn('Please select a row that want to be Edit!');
        }
    },
    deleteConfirm() {
        if (this.model) {
          this.showDelConfirm = true;
        } else {
            toastr.warn('Please select a row that want to be Delete!');
        }
    },
    deleteData: async function() {
      await items.remove(this.model);
      this.refresh();
    },
    exportxls: async function() {
        this.isLoading=true;
        try {
            const response = await items.exportxls(this.tblData);
            this.isLoading=false;    
        } catch (error) {
            this.isLoading=false;
            if (error.message) {
                toastr.error(error.message, 'Error Info',10000);
            } else {
                toastr.error(JSON.stringify(error), 'Error Info',10000);
            }
        }
    },
    closeEditItem: function() {
      this.showList=true;
      this.showEditItem=false
    },
    closeEditGambar: function() {
      this.showList=true;
      this.showEditGambar=false
    },
    closeForm: function() {
      this.showList=true;
      this.showAddForm=false
    },
    close(){
      router.push("/");
    },    
  }
};
</script>
