<template>
  <div class="animated fadeIn">
    <b-card v-show="showList">
      <div slot="header">Restaurant Menu  
        <div class="card-header-actions">
          <b-button variant="primary mr-1" @click="add">Add</b-button>
          <!-- <b-button variant="primary mr-1" @click="edit">Edit</b-button>
          <b-button variant="primary mr-1" @click="deleteConfirm">Delete</b-button>
          <b-button variant="primary mr-1" @click="exportxls()"><i class="fa fa-file-excel-o"></i>Export</b-button>-->
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
            @row-clicked="selectMenu"
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
        <b-modal v-model="showForm"  header-bg-variant="primary" title="Form Input -  Item Barang" size="lg" :centered="true" hide-footer >
          <b-card>
                <CameraCapture @image-captured="handleImageCaptured" @image2-captured="handleImage2Captured" @image3-captured="handleImage3Captured" class="mb-2"/>
                
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
import items from "../apis/items";
import Loading from 'vue-loading-overlay';
import myNumber from "../components/my-number";
import CameraCapture from "../components/webcam.vue";
import toastr from "mini-toastr";
import { validationMixin } from "vuelidate";
import { required} from "vuelidate/lib/validators";
toastr.init();

export default {
  components: {Loading,myNumber,CameraCapture},
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
      tblData: {
        page: 1,
        limit: 10,
        total: 0,
        sortBy: null,
        sortDesc: false, item_name:''
      },
        frmdata: {
            item_name: '',
            item_price: 1,
            item_stock: 1,
        },
      model:{},
      isLoading:false,
      showDelConfirm: false,
      showFilter:false,
      showForm:false,
      showList:true,
      showReport:false,
      reportUrl: `${location.origin}/#load`,
        activeStatus : [{ value: '', text: '-- ALL --' },, { value: '0', text: 'Yes' },{ value: '1', text: 'No' }],

    };
  },
  methods: {
    handleImageCaptured(imageData) {
      this.capturedImage = imageData;
    },
    handleImage2Captured(imageData) {
      this.capturedImage2 = imageData;
    },
    handleImage3Captured(imageData) {
      this.capturedImage3 = imageData;
    },
    async submitItem() {
      try {
        const frm = {...this.frmdata};
        frm.image= this.capturedImage
        frm.image2= this.capturedImage2
        frm.image3= this.capturedImage3
        const response = await items.save(frm);
        alert("Item berhasil disimpan!");
        // this.resetForm();
      } catch (error) {
        console.error("Error saving item:", error);
        alert("Gagal menyimpan item!");
      }
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
    selectMenu(record,index) {
      if ((this.model) && (this.model._rowVariant)) {
          delete this.model._rowVariant;
      }
      this.model = record;
      record._rowVariant= 'info';
      this.$forceUpdate();
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
      this.showForm=true
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
    closeForm: function() {
      this.showList=true;
      this.showForm=false
    },
    close(){
      router.push("/");
    },    
  }
};
</script>
