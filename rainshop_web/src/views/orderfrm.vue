<template>
  <div>
                <b-row>
                  <b-col col md="7" sm="12">
                        <div id="orderMenu" class="float-left" >
                            <div class="search-bar" style="padding: 5px;">
                                <div class="menu-subtitle small-text"><span>Cari item Barang</span></div>
                                <b-row>
                                    <b-col>
                                        <b-input-group >
                                         <b-button class="btn btn-success ml-3" @click="showWebcam=true" > Cari Pakai <i class="fa fa-camera"></i></b-button>
                                            <b-input-group-append>
                                                <b-button class="btn btn-danger" @click="showWebcam=false" > <i class="fa fa-times"></i></b-button>
                                            </b-input-group-append>
                                        </b-input-group>
                                    </b-col>
                                    <b-col cols="7">
                                        <b-input-group >
                                            <b-form-input v-model="tblData.item_name" placeholder="Tulis nama barang" @keyup.13.native="getItems()" ></b-form-input>
                                            <b-input-group-append>
                                                <b-button class="btn btn-danger" @click="tblData.item_name=''" > <i class="fa fa-times"></i></b-button>
                                            </b-input-group-append>
                                            <b-input-group-append>
                                                <b-button class="btn-normal safe ml-1" @click="getItems" > Cari pakai nama</b-button>
                                            </b-input-group-append>
                                        </b-input-group>
                                    </b-col>
                                </b-row>

                            </div>
                            <!-- START OF MENU -->
                            <div class="item-list">
                                    <b-table
                                        class="mb-0"
                                        ref="tblHasil"
                                        responsive
                                        striped hover 
                                        :items="itemList"
                                        :fields="fields"
                                        @row-clicked="clickItemDibeli"
                                    >
                                    <template v-slot:cell(item_name)="data">
                                        <h1>{{(data.item.item_name)}}</h1>
                                        <p style="font-size: larger;"> 
                                            <strong >Harga: RP. {{(data.item.item_price)|numFormat}}</strong>
                                            <div style="float:right; text-align: right; margin-top:-25px;">
                                                Stok: {{data.item.item_stock}}
                                            </div>
                                        </p>
                                    </template>
                                    <template v-slot:cell(image1)="data">
                                            <img :src="data.item.image" :key="data.item.image" @click="openZoomImage(data.item.image)" class="img-fluid" alt />
                                    </template>

                                    </b-table>
                            </div>
                            <!-- END OF MENU-->
                        </div>
                  </b-col>
                  <b-col col md="5" sm="12">
                    <div id="orderSummary" >
                        <b-row class="sum-title m-2" no-gutters>
                            <b-col cols="7">
                                <h6 v-if="frmdata.totalitem && frmdata.totalitem!==''" >
                                    {{ frmdata.totalitem }} ( {{frmdata.totalqty}} )
                                </h6>         
                            </b-col>
                            <b-col cols="5">
                                <div class="float-right" :key="frmdata.sales_no">
                                    Struk: {{ frmdata.sales_no }}
                                </div>
                            </b-col>
                        </b-row>
                        <!-- list -->
                        <div class="sum-list" >
                            <b-table-simple hover small caption-top striped responsive>
                                <b-thead head-variant="dark">
                                <b-tr>
                                    <b-th>Item</b-th>
                                    <b-th class="text-center">Quantity</b-th>
                                    <b-th class="text-right">Netto</b-th>
                                    <b-th></b-th>
                                </b-tr>
                                </b-thead>
                                <b-tbody>
                                <b-tr v-for="(m, key) in lineorder" v-bind:key="key">
                                    <b-td width="60%">
                                            <div class="h6  mb-0">{{m.item_name}} 
                                                <b-badge variant="warning">{{m.menunote}}</b-badge> 
                                            </div>
                                            <small class="ml-2 text-muted"> @{{ m.item_price | numFormat('0,0.00') }}
                                            </small>
                                    </b-td>
                                    <b-td class="pt-2">
                                        <div style="width:120px;">
                                            <b-input-group>
                                            <b-input-group-append>
                                                <!-- <b-button variant="outline-dark" @click="decreaseQty(m)" :disabled="((m.campaignid) && (m.termapply===1) && (m.termapplymulti===0))" > <i class="fa fa-minus"></i></b-button> -->
                                                <b-button variant="outline-dark" @click="decreaseQty(m)" > <i class="fa fa-minus"></i></b-button>
                                            </b-input-group-append>
                                            <b-form-input v-model="m.qty" readonly ></b-form-input>
                                            <b-input-group-append>
                                                <!-- <b-button variant="outline-success" @click="increaseQty(m)" :disabled="((m.campaignid) && (m.termapply===1) && (m.termapplymulti===0))"> <i class="fa fa-plus"></i> </b-button> -->
                                                <b-button variant="outline-success" @click="increaseQty(m)" > <i class="fa fa-plus"></i> </b-button>
                                            </b-input-group-append>
                                            </b-input-group>
                                        
                                        </div>    
                                    </b-td>
                                    <b-td class="text-right pt-3">
                                        <h6>{{ (m.qty*m.item_price) | numFormat('0,0.00') }}</h6>
                                    </b-td>
                                    <b-td class="text-right pt-3">
                                            <a href="javascript:void(0)" class="text-danger" @click="deleteItem(m, key)">
                                               <h6><i class="fa fa-trash"></i></h6> 
                                            </a>
                                    </b-td>
                                </b-tr>
                                </b-tbody>
                            </b-table-simple>  
                        </div>
                        <!-- end of list -->
                        <!-- total -->
                        <div class="sum-total">
                            <!-- <b-row >
                                <b-col col md="6" class="text-right">
                                    <h6>Sub Total</h6>
                                </b-col>
                                <b-col col md="6" class="text-right">
                                <h6>{{ frmdata.subtotal | numFormat('0,0.00') }}</h6>
                                </b-col>
                            </b-row> -->
                            <b-row >
                                <b-col col md="6" class="text-right">
                                    <h6>Total Belanja</h6>
                                </b-col>
                                <b-col col md="6" class="text-right pt-2" >
                                    <h6 style="color: rgb(0, 119, 255);">{{ frmdata.sales_total  | numFormat('0,0.00') }}</h6>
                                    <hr/>
                                </b-col>
                            </b-row>
                            <b-row>
                                <b-col col md="6" class="text-right">
                                    <h6>Cara Bayar pakai</h6>
                                </b-col>
                                <b-col col md="6" >
                                    <b-form-radio-group  v-model="frmdata.sales_paym">
                                        <b-form-radio  value="TUNAI">UANG TUNAI</b-form-radio>
                                        <b-form-radio  value="QRIS" class="ml-2">QRIS</b-form-radio>
                                    </b-form-radio-group>

                                </b-col>
                            </b-row>
                            <b-row >
                                <b-col col md="6" class="text-right">
                                    <h6>Uang Pembayaran</h6>
                                </b-col>
                                <b-col col md="6" class="text-right">
                                    <my-number class="form-control text-right pr-1" separator=","  :precision="2"  v-model="frmdata.paid_amount" :state="!$v.frmdata.paid_amount.$error" ></my-number>
                                </b-col>
                            </b-row>
                            <b-row>
                                <b-col col md="6" class="text-right">
                                    <h6>Uang Kembalian</h6>
                                </b-col>
                                <b-col col md="6" class="text-right">
                                    <h6 style="color: red;">{{ frmdata.change_amount  | numFormat('0,0.00') }}</h6>
                                    <hr/>
                                </b-col>
                            </b-row>
                            <b-row class="justify-content-center">
                                <b-button variant="primary" class=" ml-1"  @click="saveOrder()"><i class="fa fa-print"></i> &nbsp;<span>Print Struk</span></b-button>
                                <b-button variant="warning" class="ml-4"  @click="clearForm()"> &nbsp;<span> Kosongkan </span></b-button>
                            </b-row>
                        </div>
                        <!-- end of total -->
                    </div>
                </b-col>
                </b-row>



    <b-modal v-model="showWebcam"  header-bg-variant="primary" title="Cari Barang" size="lg" :centered="true" hide-footer >
        <CameraCapture @image-captured="searchItem" class="mb-2"/>
    </b-modal>
    <b-modal v-model="showZoomGambar"  header-bg-variant="primary" title="Zoom Gambar Barang" size="md" :centered="true" ok-only  >
            <img :src="zoomImage" :key="zoomImage" class="img-fluid" width="640" height="480" alt />
    </b-modal>

  </div>
</template>
<style lang="scss" scoped>
    .row-details-form {
        label {
        text-align: right !important;
        }
        legend {
        text-align: right !important;
        }
      .input-group {
          .input-group-prepend {
              label {
                  width: 130px !important;
                  margin-right:5px;
              }
          }
      }

    }
    .noimage {
        height: 60px;
        width: 60px;
    }
    #orderSummary {
        border: 1px solid silver;
        border-radius: 5px;
        min-height: 460px;
        // overflow: hidden;
        height: auto;
        padding: 5px;
    }
    #orderMenu {
        border: 1px solid silver;
        border-radius: 5px;
        height: 100%;
        width: 100%;
        overflow: hidden;
        position: relative;
    }
     .search-bar {
        border-bottom: 1px solid silver;
        max-height: 90px;
        width: 100%;
        overflow: hide;

    }
    .menu-img {
        float:left;
    }
    .item-list {
        overflow: scroll;
        position: absolute;
        height:500px;
        max-height: 600px;
        width: 100%;
        right: 0;
        top: 90px;
        padding-right: 10px;
        padding-bottom: 10px;
    }
    .menu-item {
        border: none;
        border-radius: none;
    }
    .menu-item > .card {
            height: 100%;
            margin: 0px 5px;
            border: none;
            border-radius: 0;
    }
    .menu-item-tile {
        width: 33%;
        display: inline-block;
        margin-top: 5px;
        cursor: pointer;
    }
    #orderPayment {
        border: 1px solid silver;
        border-radius: 5px;
        height: 460px;
        width: 100%;
        position: relative;
        display: block;
    }
    .payment-amount-list {
        padding: 5px 0 5px 5px;
        border-bottom: 1px solid silver;
        height: 40%;
        width: 100%;
        overflow: scroll;
    }
    .sum-list {
        height: 400px;
        max-height: 400px;
        overflow: scroll;
        margin: 5px -5px;
        min-width: 400px;
    }
    .sum-list>ul {
        width: 100%;
        padding:0px
    }
    .sum-total {
        // background: slategray;
        margin: 5px 20px 0px 20px;
        border-top: 1px solid grey;
        // width: 100%;
        // height: auto;
        padding: 5px;
        font-size: 11px;
    }
    .payment-item-tile {
        width: 24%;
        display: inline-block;
        margin-top: 5px;
        .card-body {
            color: white;
            margin: 5px!important;
            text-align: center;
            padding-top: 15px;
            margin-top: 10px;
            height:45px;
        }
    }

    .payment-method-list {
        padding: 5px;
        // background: #2f353a;
    }

    .payment-item > span:nth-child(1) {
        min-width: 20%;
    }
    .payment-item > span:nth-child(2) {
        width: 50%;
    }

    .payment-item > span:nth-child(3) {
        width: 25%;
    }

    .sum-title {
        border-bottom: 1px solid silver;
        font-size: 16px;
    }
    .action-btn {
        margin: 5px 0 5px 0;
        .btn {
            color: white;
            width: 35px;
            height: 35px;
        }
    }
    .menu-title {
        font-size: 11px;
        font-weight: bold;
    }
    .menu-sub-title {
        margin: 0;
        color: rgb(48, 48, 48)
    }
    .medium-text, .medium-text > .input-group-text, 
    .medium-text > .input-group-prepend > .input-group-text, 

    ul {
        padding-left: 0;

        .sub-link {
            display: block;
            margin-left: 10px;

            i {
                width: 20px;
            }

            li {
                display: block;
                padding-left: 20px;

                i {
                    width: 15px;
                }
            }
        }
    }
</style>


<script>
import CameraCapture from "../components/CameraCapture.vue";
import items from "../apis/items";
import sales from "../apis/sales";
import moment from 'moment';
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import myNumber from "../components/my-number";
import toastr from "mini-toastr";
toastr.init();

export default {
  components: { myNumber,CameraCapture },
    mixins: [validationMixin],
    validations: {
        frmdata: {
            paid_amount: { required },
        },
    }, 
  data() {
    return {
      itemsApi:items,
      showWebcam:false,
      fields: [
          { key: "item_name" , 
            label: "Nama Item Barang",
            sortable: true
          },
          {
            key: "image1",
            thStyle: "width:150px",
            label: "Image",
            tdClass: "text-center"
          },
      ],
        frmdata:{
            sales_id:'', sales_no:'', paid_amount:0, totalitem:'', sales_total:0, change_amount:0, sales_paym:'TUNAI'
        },
        selectedItem:null,
        itemList: [],
        menuIdx: 0,
        lineorder: [],
      tblData: {
        page: 1,
        limit: 10,
        total: 0,
        sortBy: null,
        sortDesc: false, item_name:''
      },
        modeViewOnly:false,
        printer:null,
        zoomImage:null,
        showZoomGambar:false
    };
  },
  created: async function() {
    this.$watch('frmdata.paid_amount', function(newval) {
        if (newval==this.frmdata.paid_amount){
            this.frmdata.change_amount = parseFloat(newval)-parseFloat(this.frmdata.sales_total);
        }
    });
  },
  methods: {
    async searchItem(imageData) {
      try {
        const list = await items.imageSearch({
          image: imageData,  // Base64 image
        });
        list.forEach(el => {
          el.image='';
          items.imageItem(el.image_id).then((imgBase64) => {
            el.image=imgBase64          
          })
        });
        this.itemList = list;
        this.showWebcam=false;
      } catch (error) {
        console.error("Error searching item:", error);
        alert("Gagal mencari item!");
      }
    },
    getItems: async function() {
        const list = await items.list(this.tblData);
        list.forEach(el => {
          el.image='';
          items.imageItem(el.image_id).then((imgBase64) => {
            el.image=imgBase64          
          })
        });
        this.itemList = list;  
    },        
    clickItemDibeli: function(menu) {
        // if (this.modeViewOnly==true) {
        //     toastr.error('View Only, No Data Change allowed');
        //     return;
        // } 
        // if (menu.isactive != 1) {
        //     toastr.error('SOLD OUT ITEM');
        //     return;
        // } 
        // const saiki= (this.frmdata.sales_time) ? moment(this.frmdata.sales_time).format('HH:mm') : moment().format('HH:mm');
        this.selectedItem={};
        for(const key in menu){
            this.selectedItem[key] = menu[key];
        }
        this.selectedItem.qty = 1;
        this.lineorder.push(this.selectedItem);
        this.hitungTotal();
    },

    increaseQty: function(row){
        if (this.modeViewOnly==true) {
            toastr.error('View Only, No Data Change allowed');
            return;
        } 
        row.qty += 1;
        this.hitungTotal();
    },
    decreaseQty: function(row){
        if (this.modeViewOnly==true) {
            toastr.error('View Only, No Data Change allowed');
            return;
        } 
        if (row.qty>1) row.qty -= 1;
        this.hitungTotal();
    },
    deleteItem: function(item, idx) {
        // if (this.modeViewOnly==true) {
        //     toastr.error('View Only, No Data Change allowed');
        //     return;
        // } 
        this.selectedItem = null;
        this.lineorder.splice(idx, 1);
        this.hitungTotal();
    },
    hitungTotal: function(){
            let totalqty = 0, subtotal = 0, discval = 0, netto = 0, serviceval = 0, dpp=0, pb1val = 0, total = 0, paid_amount = 0;
            //const total_qty_description = [];
            this.lineorder.forEach((item_dibeli)=> {
                subtotal += item_dibeli.qty * item_dibeli.item_price;
                item_dibeli.subtotal=item_dibeli.qty * item_dibeli.item_price
                totalqty += item_dibeli.qty;
                //total_qty_description.push(`${item_dibeli.qty} ${item_dibeli.item_name}`);
            });

            // HITUNG TOTAL INVOICE
            netto = subtotal - discval;
            total = netto ;

            this.frmdata.totalitem = `${this.lineorder.length}  ${this.lineorder.length > 1 ? 'items' : 'item'}` ;
            this.frmdata.totalqty = `${totalqty} Qty`;

            this.frmdata.subtotal = subtotal;
            this.frmdata.netto = netto;
            this.frmdata.sales_total = total;

            if (this.frmdata.paid_amount){
                this.frmdata.change_amount = parseFloat(this.frmdata.paid_amount)-parseFloat(this.frmdata.sales_total);
            }
            this.$forceUpdate();
    },
    saveOrder: async function(debug) {
        // if (this.modeViewOnly==true) {
        //     toastr.error('View Only, No Data Change allowed');
        //     return;
        // } 
        try {
            this.hitungTotal();
            const data = {};
            const keys = ['sales_id','sales_no','sales_total','sales_paym','totalitem', 'paid_amount', 'change_amount'];
            for (var key in this.frmdata) {
                if (keys.indexOf(key) >= 0 && this.frmdata[key]) {
                    data[key] = this.frmdata[key];
                }
            }
            const keysLine = ['sales_id','sales_line_id','item_id','item_price','qty', 'subtotal','item_name'];
            data.lines =  this.lineorder.reduce((newArr, item) => {
                                const newitem={}
                                for (var key in item) {
                                    if (keysLine.indexOf(key) >= 0 && item[key]) {
                                        newitem[key] = item[key];
                                    }
                                }
                                newArr.push(newitem);
                                    return newArr;
                            }, []);
            let baru=false;
            if (!(this.frmdata.sales_id)) {
                baru=true;
            }       

            sales.printStruk(data).then(()=>{
                console.log(`DONE calling ${process.env.VUE_APP_BASE_API}/print-struk`);
            })

            if (debug==true) {
                await sales.saveDebug(data);

            } else {
                const result = await sales.save(data);
                // console.log('result : ', result);
                this.frmdata.sales_id=result.data.sales_id;
                this.frmdata.sales_no=result.data.sales_no;
                // this.frmdata.sales_time=result.data.sales_time;
                data.sales_id=result.data.sales_id;
                data.sales_no=result.data.sales_no;
                // data.sales_time=result.data.sales_time;

                if (baru==true){
                    toastr.success(`Order Saved, Number.${this.frmdata.sales_no}`);
                } else {
                    toastr.success(`Order Change Saved`);
                }

            }

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
    openZoomImage: function(gambar) {
        this.zoomImage=gambar
        this.showZoomGambar=true;
    },

    clearForm: function() {
        // clear frmdata
        for(const key in this.frmdata){
            this.frmdata[key] = '';
        }
        this.frmdata.totalitem='';
        this.frmdata.totalqty='';
        this.frmdata.sales_no='';
        this.frmdata.sales_id='';
        this.lineorder = [];
        this.hitungTotal()
    },

  },
};
</script>